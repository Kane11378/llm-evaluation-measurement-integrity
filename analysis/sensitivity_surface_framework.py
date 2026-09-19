#!/usr/bin/env python3
"""OMI-3079 analytic sensitivity-surface framework.

Zero behavioral/model/provider calls. Synthetic deterministic math/simulation only.
Frozen empirical rows are copied from accepted OMI adjudications and are not re-fit.

Run:
    python SENSITIVITY_SURFACE_FRAMEWORK.py

Dependencies: numpy, scipy
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.stats import norm, t

BASE_SEED=3079
ALPHA=.05
N_VALIDATION=124
VALIDATION_REPS=20_000
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/"figure_data"
RESULT_JSON=ROOT/"analysis"/"SENSITIVITY_SURFACE_RESULTS_REPRODUCED.json"

# Frozen OMI-3078 synthetic models.
LATENT_INTERCEPT=1.25
LATENT_DIFFICULTY_SLOPE=-.85
RESOURCE_MEDIAN_BASE=350.0
RESOURCE_DIFFICULTY_SLOPE=.5
RESOURCE_LOG_SD=.7

# Deterministic Simpson quadrature for D~N(0,1), matching the committed surface package.
NQ=4000
D=np.linspace(-8.0,8.0,NQ+1)
H=16.0/NQ
C=np.where((np.arange(NQ+1)==0)|(np.arange(NQ+1)==NQ),1.0,
           np.where(np.arange(NQ+1)%2==1,4.0,2.0))
W=C*H/3.0*np.exp(-.5*D*D)/math.sqrt(2*math.pi)
W=W/W.sum()

def E(x): return float(np.sum(W*np.asarray(x)))
def p_d(beta=0.0): return expit(LATENT_INTERCEPT+LATENT_DIFFICULTY_SLOPE*D+beta)
def marginal(beta=0.0): return E(p_d(beta))
def odds(x): return x/(1-x)

# Same deterministic erf approximation used to generate the committed resource CSV.
def erf_approx(x):
    x=np.asarray(x,dtype=float); sign=np.where(x<0,-1.0,1.0); a=np.abs(x)
    p=.3275911; a1=.254829592; a2=-.284496736; a3=1.421413741; a4=-1.453152027; a5=1.061405429
    tt=1/(1+p*a)
    y=1-(((((a5*tt+a4)*tt+a3)*tt+a2)*tt+a1)*tt)*np.exp(-a*a)
    return sign*y
def Phi_approx(x): return .5*(1+erf_approx(np.asarray(x)/math.sqrt(2)))

def write_csv(name, rows):
    path=DATA/name; path.parent.mkdir(parents=True,exist_ok=True)
    if not rows: raise ValueError(name)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

def retained(p,a,b):
    den=a*p+b*(1-p)
    return a*p/den

def scorer():
    p=marginal(0); a0,b0=1.0,.9; q0=retained(p,a0,b0); rows=[]
    for a1 in np.arange(.05,1.0001,.05):
        for b1 in np.arange(.05,1.0001,.05):
            q1=retained(p,float(a1),float(b1)); eff=q1-q0; margin=a1*b0-a0*b1
            rows.append(dict(treatment_correct_retention=float(a1),treatment_incorrect_retention=float(b1),
                delta_correct_retention_vs_control=float(a1-a0),delta_incorrect_retention_vs_control=float(b1-b0),
                latent_accuracy_both_arms=p,control_retained_accuracy=q0,treatment_retained_accuracy=q1,
                apparent_effect_treatment_minus_control=eff,boundary_margin_a1b0_minus_a0b1=float(margin),
                sign="zero" if abs(eff)<1e-12 else ("positive" if eff>0 else "negative")))
    summary=dict(latent_null_accuracy=p,control_reference=dict(correct_retention=a0,incorrect_retention=b0),
        exact_null_effect_numerator="p(1-p)(a1*b0-a0*b1)",positive_condition="a1*b0 > a0*b1",
        negative_condition="a1*b0 < a0*b1",zero_boundary="a1*b0 = a0*b1",
        analytic_exemplar_at_treatment_1_0_60=retained(p,1,.6)-q0)
    return rows,summary

def missingness():
    p=p_d(0); mu=E(p); r0=float(expit(3.5)); miss0=1-r0; rows=[]
    for alpha in np.arange(0,4.0001,.2):
        for gamma in np.arange(-2,2.0001,.2):
            r=expit(alpha+gamma*D); er=E(r); epr=E(p*r); acc=epr/er; eff=acc-mu; cov=epr-mu*er
            rows.append(dict(treatment_observation_intercept=float(alpha),
                treatment_observation_slope_on_difficulty=float(gamma),
                control_observation_probability_constant=r0,control_missing_fraction=miss0,
                treatment_missing_fraction=1-er,missing_rate_asymmetry_treatment_minus_control=(1-er)-miss0,
                latent_accuracy_both_arms=mu,control_complete_case_accuracy=mu,treatment_complete_case_accuracy=acc,
                complete_case_apparent_effect=eff,cov_accuracy_observation=cov,
                sign="zero" if abs(eff)<1e-12 else ("positive" if eff>0 else "negative")))
    def pt(alpha,gamma):
        r=expit(alpha+gamma*D); er=E(r); acc=E(p*r)/er
        return dict(gamma=gamma,missing_fraction=1-er,complete_case_accuracy=acc,complete_case_effect_vs_latent=acc-mu)
    summary=dict(latent_null_accuracy=mu,control_observation="logit^-1(3.5), constant in difficulty",
        treatment_observation="logit^-1(alpha + gamma*difficulty)",
        identity="mu1_CC-mu = Cov[p(D),q1(D)]/E[q1(D)]",
        sign_result="p(D) decreases strictly in D: bias >0 for gamma<0, =0 for gamma=0, <0 for gamma>0",
        equal_missing_counterexample=dict(alpha=2.2,gamma_negative=pt(2.2,-1.3),gamma_positive=pt(2.2,1.3)),
        different_missing_zero_bias_counterexample=dict(alpha=2.2,**pt(2.2,0.0)))
    return rows,summary

def accepted(p,c1,c0): return p*c1/(p*c1+(1-p)*c0)

def retry():
    p0,p1=marginal(0),marginal(.3); c01,c00=.98,.90; q0=accepted(p0,c01,c00); raw=p1-p0
    lam0=c01/c00; star=lam0*odds(p0)/odds(p1); rows=[]
    for c11 in np.arange(.05,1.0001,.05):
        for c10 in np.arange(.05,1.0001,.05):
            q1=accepted(p1,float(c11),float(c10)); eff=q1-q0
            rows.append(dict(treatment_pass_if_correct=float(c11),treatment_pass_if_incorrect=float(c10),
                control_pass_if_correct=c01,control_pass_if_incorrect=c00,latent_control_accuracy=p0,
                latent_treatment_accuracy=p1,latent_effect=raw,accepted_control_accuracy=q0,
                accepted_treatment_accuracy=q1,accepted_effect=eff,distortion=eff-raw,
                treatment_acceptance_odds_multiplier=float(c11/c10),zero_effect_boundary_lambda1=star,
                sign_reversed_relative_to_latent=bool(eff*raw<0)))
    summary=dict(latent_accuracy=dict(control=p0,treatment=p1),latent_effect=raw,
        control_acceptance=dict(correct=c01,incorrect=c00,odds_multiplier=lam0),
        exact_odds_identity="odds(p_accepted,z)=odds(p_z)*(c_z1/c_z0)",
        positive_latent_effect_reversal_condition="(c11/c10)/(c01/c00) < odds(p0)/odds(p1)",
        zero_effect_treatment_odds_multiplier=star,analytic_exemplar_0_80_0_99=accepted(p1,.8,.99)-q0,
        estimand_boundary="Acceptance weighting applies to replacement/resampled outcome-relevant attempt state. A frozen same-unit retrying system is a different target system/estimand.")
    return rows,summary

def finalizer():
    p0,p1=marginal(0),marginal(.3); raw=p1-p0; s0,f0=.96,.02; m0=s0*p0+f0*(1-p0); rows=[]
    for s1 in np.arange(0,1.0001,.05):
        for f1 in np.arange(0,1.0001,.05):
            m1=s1*p1+f1*(1-p1); eff=m1-m0
            rows.append(dict(treatment_sensitivity=float(s1),treatment_false_positive_probability=float(f1),
                control_sensitivity=s0,control_false_positive_probability=f0,worker_control_accuracy=p0,
                worker_treatment_accuracy=p1,worker_effect=raw,measured_control_accuracy=m0,
                measured_treatment_accuracy=float(m1),measured_effect=float(eff),distortion=float(eff-raw),
                zero_boundary_residual_m1_minus_m0=float(eff),sign_reversed_relative_to_worker=bool(eff*raw<0)))
    summary=dict(worker_accuracy=dict(control=p0,treatment=p1),worker_effect=raw,
        control_channel=dict(sensitivity=s0,false_positive=f0),treatment_invariant_identity="Delta_m=(s-f)*Delta_p",
        treatment_invariant_attenuation_condition="0 <= s-f <= 1; strict attenuation for 0 < s-f < 1, erasure at s=f, reversal if s-f<0",
        symmetric_flip_identity="s=1-epsilon,f=epsilon => Delta_m=(1-2epsilon)Delta_p",
        treatment_dependent_zero_boundary="s1*p1 + f1*(1-p1) = s0*p0 + f0*(1-p0)",
        zero_boundary_s1_at_f1_0_02=(m0-.02*(1-p1))/p1,
        analytic_exemplar_s1_0_80_f1_0_02=(.8*p1+.02*(1-p1))-m0)
    return rows,summary

def resource():
    p0d,p1d=p_d(0),p_d(.25); p0,p1=E(p0d),E(p1d); raw=p1-p0
    caps=sorted(set(round(2**(9+5*i/30)) for i in range(31))); rows=[]
    for cap in caps:
        lc=math.log(cap)
        for delta in np.arange(-.6,.6001,.06):
            o0=Phi_approx((lc-math.log(350)-.5*D)/.7)
            o1=Phi_approx((lc-math.log(350)-.5*D-delta)/.7)
            eo0,eo1=E(o0),E(o1); epy0,epy1=E(p0d*o0),E(p1d*o1)
            cc=epy1/eo1-epy0/eo0; err=epy1-epy0
            rows.append(dict(output_cap=cap,log2_output_cap=math.log2(cap),treatment_log_demand_shift=float(delta),
                treatment_median_demand_ratio_exp_shift=math.exp(delta),control_truncation_fraction=1-eo0,
                treatment_truncation_fraction=1-eo1,truncation_asymmetry_treatment_minus_control=(1-eo1)-(1-eo0),
                latent_control_accuracy=p0,latent_treatment_accuracy=p1,latent_effect=raw,
                complete_case_effect=cc,complete_case_distortion=cc-raw,
                truncation_as_error_effect=err,truncation_as_error_distortion=err-raw))
    def ref(cap,delta):
        lc=math.log(cap); o0=Phi_approx((lc-math.log(350)-.5*D)/.7); o1=Phi_approx((lc-math.log(350)-.5*D-delta)/.7)
        eo0,eo1=E(o0),E(o1); epy0,epy1=E(p0d*o0),E(p1d*o1); cc=epy1/eo1-epy0/eo0; err=epy1-epy0
        return dict(control_truncation_fraction=1-eo0,treatment_truncation_fraction=1-eo1,
            truncation_asymmetry=(1-eo1)-(1-eo0),complete_case_effect=cc,complete_case_distortion=cc-raw,
            truncation_as_error_effect=err,truncation_as_error_distortion=err-raw)
    summary=dict(model="log Q=log(350)+0.5*difficulty+delta*z+Normal(0,0.7^2); latent logit shift beta=0.25",
        latent_effect=raw,cap_range=[512,16384],shift_range=[-.6,.6],
        explicit_scope="synthetic only; not calibrated to OMI token/resource demand",
        analytic_reference_points={"2048_delta_0.30":ref(2048,.3),"8192_delta_0.30":ref(8192,.3)})
    return rows,summary

def validate_pseudorep(k,rho):
    seed=BASE_SEED+10_000+100*k+int(round(rho*1000)); rng=np.random.default_rng(seed)
    rn=ri=0; ratio=0.0; processed=0; batch=500
    critn=float(t.ppf(.975,N_VALIDATION*k-1)); criti=float(t.ppf(.975,N_VALIDATION-1))
    while processed<VALIDATION_REPS:
        b=min(batch,VALIDATION_REPS-processed)
        u=rng.normal(size=(b,N_VALIDATION,1)); e=rng.normal(size=(b,N_VALIDATION,k))
        x=math.sqrt(rho)*u+math.sqrt(1-rho)*e; means=x.mean(axis=(1,2))
        nse=x.reshape(b,-1).std(axis=1,ddof=1)/math.sqrt(N_VALIDATION*k)
        im=x.mean(axis=2); ise=im.std(axis=1,ddof=1)/math.sqrt(N_VALIDATION)
        rn+=int(np.sum(np.abs(means/nse)>critn)); ri+=int(np.sum(np.abs(means/ise)>criti)); ratio+=float(np.sum(nse/ise))
        processed+=b
    de=1+(k-1)*rho; approx=2*(1-norm.cdf(norm.ppf(.975)/math.sqrt(de)))
    return dict(K=k,rho=rho,N_instances=N_VALIDATION,replications=VALIDATION_REPS,design_effect=de,
        normal_approx_actual_alpha=approx,empirical_naive_call_level_rejection=rn/VALIDATION_REPS,
        empirical_instance_level_rejection=ri/VALIDATION_REPS,mean_naive_to_instance_se_ratio=ratio/VALIDATION_REPS,
        theoretical_naive_to_correct_se_ratio=1/math.sqrt(de),seed=seed)

def pseudorep():
    rows=[]
    z=float(norm.ppf(.975))
    for k in range(1,21):
        for rho in np.arange(0,.9001,.05):
            de=1+(k-1)*rho; aa=2*(1-norm.cdf(z/math.sqrt(de)))
            rows.append(dict(calls_per_instance_K=k,icc_rho=float(rho),design_effect=float(de),
                naive_to_correct_se_ratio=1/math.sqrt(de),nominal_alpha=.05,
                normal_approx_actual_alpha_if_calls_treated_independent=float(aa),alpha_inflation_ratio=float(aa/.05),
                omi_K6_scale_marker=bool(k==6)))
    vals=[validate_pseudorep(k,r) for k,r in [(1,0),(2,.1),(6,.4),(10,.6),(20,.8)]]
    return rows,dict(design_effect="DE=1+(K-1)rho",naive_to_correct_se_ratio="1/sqrt(DE)",
        nominal_alpha_approximation="alpha_actual≈2[1-Phi(z_(1-alpha/2)/sqrt(DE))]",
        grid=dict(K=[1,20],rho=[0,.9]),validation=vals,
        omi_scale_note="K=6 is only a design-scale marker; ICC=.40 is synthetic and not estimated from OMI.")

def bank():
    rows=[]
    for B in sorted(set(list(range(100,5001,100))+[1488])):
        for h in np.logspace(-6,-2,41):
            pf=(1-float(h))**B
            rows.append(dict(bank_size_B=B,per_call_hazard_h=float(h),expected_failures_Bh=B*float(h),
                full_bank_probability=pf,stop_probability=1-pf,omi_B1488_scale_marker=bool(B==1488)))
    summary=dict(exact_identity="P(full)=(1-h)^B",hazard_range=[1e-6,.01],bank_size_range=[100,5000],
        thresholds={"1488":{"h_for_95pct_full":1-.95**(1/1488),"h_for_50pct_full":1-.50**(1/1488)}},
        omi_note="B=1488 is a scale marker only. No OMI per-call hazard is inferred or estimated.")
    return rows,summary

def extraction():
    pnull=marginal(0); p0,p1=pnull,marginal(.3); raw=p1-p0; zr=[]; rr=[]
    for r0 in np.arange(0,1.0001,.05):
        for r1 in np.arange(0,1.0001,.05):
            eff=r1*p1-r0*p0
            zr.append(dict(control_extraction_success_random_within_arm=float(r0),
                treatment_extraction_success_random_within_arm=float(r1),raw_control_accuracy=p0,raw_treatment_accuracy=p1,
                raw_effect=raw,derived_control_accuracy_failure_to_zero=float(r0*p0),
                derived_treatment_accuracy_failure_to_zero=float(r1*p1),derived_effect=float(eff),
                distortion=float(eff-raw),sign_reversed_relative_to_raw=bool(eff*raw<0),
                true_null_apparent_effect_if_p0_equals_p1=float(pnull*(r1-r0)),
                zero_effect_boundary_residual_r1p1_minus_r0p0=float(eff)))
    for a1 in np.arange(.05,1.0001,.05):
        for b1 in np.arange(.05,1.0001,.05):
            q1=retained(pnull,float(a1),float(b1)); eff=q1-pnull
            rr.append(dict(treatment_correct_extraction_retention=float(a1),treatment_incorrect_extraction_retention=float(b1),
                control_correct_extraction_retention=1.0,control_incorrect_extraction_retention=1.0,
                latent_accuracy_both_arms=pnull,complete_case_control_accuracy=pnull,complete_case_treatment_accuracy=q1,
                complete_case_apparent_effect=eff,boundary_margin_correct_minus_incorrect_retention=float(a1-b1),
                sign="zero" if abs(eff)<1e-12 else ("positive" if eff>0 else "negative")))
    summary=dict(all_empty_extreme=dict(r0=0,r1=0,derived_effect=0),
        partial_random_common_loss="if r0=r1=r and failure maps to zero, Delta_derived=r*Delta_raw",
        treatment_correlated_random_loss_under_true_null="if p0=p1=p, Delta_derived=p*(r1-r0)",
        positive_raw_effect_sign_reversal_boundary="r1/r0=p0/p1 for r0>0; reversal below",
        boundary_ratio_p0_over_p1=p0/p1,
        outcome_dependent_row_loss_true_null="complete-case sign follows a1-b1 when control extraction is faithful")
    return zr,rr,summary

def write_static_data():
    write_csv("fig1_pipeline_nodes.csv",[
      dict(id="unit",label="Independent instance i",layer="design",kind="unit"),
      dict(id="c0",label="Matched condition z=0",layer="design",kind="condition"),
      dict(id="c1",label="Matched condition z=1",layer="design",kind="condition"),
      dict(id="worker",label="Stochastic worker response",layer="behavior",kind="response"),
      dict(id="complete",label="Completion / readability",layer="integrity",kind="gate"),
      dict(id="raw",label="Raw-response custody",layer="measurement",kind="artifact"),
      dict(id="extract",label="Deterministic extraction",layer="measurement",kind="map"),
      dict(id="score",label="Frozen deterministic score",layer="measurement",kind="map"),
      dict(id="aggregate",label="Within-instance aggregation",layer="inference",kind="map"),
      dict(id="infer",label="Independent-instance inference",layer="inference",kind="endpoint"),
      dict(id="berr",label="Behavioral error: completed/readable nonexact",layer="behavior",kind="classification"),
      dict(id="ifail",label="Integrity failure: planned observation absent",layer="integrity",kind="classification")])
    write_csv("fig1_pipeline_edges.csv",[
      dict(source="unit",target="c0",label="matched assignment",path_type="intended"),
      dict(source="unit",target="c1",label="matched assignment",path_type="intended"),
      dict(source="c0",target="worker",label="frozen operating point",path_type="intended"),
      dict(source="c1",target="worker",label="frozen operating point",path_type="intended"),
      dict(source="worker",target="complete",label="planned observation exists?",path_type="intended"),
      dict(source="complete",target="raw",label="yes",path_type="intended"),
      dict(source="complete",target="ifail",label="no",path_type="failure"),
      dict(source="raw",target="extract",label="custody before parse",path_type="intended"),
      dict(source="extract",target="score",label="faithful derived map",path_type="intended"),
      dict(source="score",target="aggregate",label="node score",path_type="intended"),
      dict(source="aggregate",target="infer",label="instance endpoint",path_type="intended"),
      dict(source="worker",target="berr",label="completed/readable but nonexact",path_type="classification"),
      dict(source="berr",target="score",label="score 0; retain denominator",path_type="intended")])
    write_csv("fig3_empirical_ladder.csv",[
      dict(order=1,incident="Parent-value leakage",failure_class="Identification",scientific_threat="Designated context not computationally necessary",prospective_safeguard="Remove parent value from current prompt; verify prompt-alone closure",historical_result_preserved="yes",omi_empirical_example="Earlier R2/MCAL S/T prompts reprinted parent values",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §2; anchor commit c97bd74d1146c52ef336328fd957cedcf6db5329"),
      dict(order=2,incident="Scorer censoring",failure_class="Measurement",scientific_threat="Completed/readable model errors could leave denominator",prospective_safeguard="Exact deterministic scorer; retain all completed/readable nonexact outputs as errors",historical_result_preserved="yes",omi_empirical_example="Prospective scorer repair after OMI-3057 audit",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §3"),
      dict(order=3,incident="Stochastic finalizer",failure_class="Measurement",scientific_threat="Second model call could change worker measurement",prospective_safeguard="Remove unnecessary stochastic finalizer",historical_result_preserved="yes",omi_empirical_example="Finalizer removed prospectively",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §4"),
      dict(order=4,incident="False all-zero derived ledger",failure_class="Derived-data integrity",scientific_threat="Extraction erased completed raw behavior",prospective_safeguard="Persist raw custody; reconstruct deterministically with frozen oracle/scorer/analyzer",historical_result_preserved="yes",omi_empirical_example="336 raw responses preserved; corrected 138/168 LOCAL vs 131/168 CROSS; p=.29398",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §5; projects/omi/research/OMI_3067_CORRECTED_PRIMARY_ADJUDICATION_20260918.md"),
      dict(order=5,incident="2048 resource truncation",failure_class="Integrity",scientific_threat="Planned response absent because output cap exhausted",prospective_safeguard="Classify integrity failure and stop; no replay/resume of exposed bank",historical_result_preserved="yes",omi_empirical_example="Ordinal 335 incomplete max_output_tokens; no confirmatory prefix",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §8"),
      dict(order=6,incident="8192 prospective requalification",failure_class="Operating point",scientific_threat="Resource change after exposure could become outcome-driven tuning",prospective_safeguard="Fresh LOCAL-only non-confirmatory qualification before new bank",historical_result_preserved="yes",omi_empirical_example="32/32 complete/readable; zero integrity failures",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §9"),
      dict(order=7,incident="Fresh fixed-bank confirmation",failure_class="Replication discipline",scientific_threat="Outcome-informed exploratory signal could be mistaken for confirmation",prospective_safeguard="Wholly fresh N=124 bank; frozen L=(D_U-D_S)/2; no retry/replacement",historical_result_preserved="yes",omi_empirical_example="1,488/1,488 complete; depth primary +0.016129, p=.5368; escalation stopped",source="projects/omi/research/OMI_3077_FRESH_DEPTH_CONFIRMATION_NULL_ADJUDICATION_20260919.md")])
    write_csv("fig4_effect_estimates.csv",[
      dict(panel="A",estimate="Corrected overall confirmatory LOCAL-CROSS",classification="confirmatory",N_independent_instances=28,effect=.0416667,ci_low=-.03821,ci_high=.12155,p_raw=.29398,p_adjusted="",ci_available="yes",interpretation="non-detection; not equivalence",source="projects/omi/research/OMI_3067_CORRECTED_PRIMARY_ADJUDICATION_20260918.md"),
      dict(panel="B",estimate="Exploratory stage S",classification="secondary/exploratory after multiplicity",N_independent_instances=28,effect=-.07143,ci_low="",ci_high="",p_raw=.38073,p_adjusted=.76146,ci_available="no",interpretation="point estimate only in this frozen figure package",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §6"),
      dict(panel="B",estimate="Exploratory stage T",classification="secondary/exploratory after multiplicity",N_independent_instances=28,effect=.05357,ci_low="",ci_high="",p_raw=.44861,p_adjusted=.76146,ci_available="no",interpretation="point estimate only in this frozen figure package",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §6"),
      dict(panel="B",estimate="Exploratory stage U",classification="secondary/exploratory after multiplicity",N_independent_instances=28,effect=.14286,ci_low="",ci_high="",p_raw=.01793,p_adjusted=.05380,ci_available="no",interpretation="Holm-adjusted p=.05380; not confirmatory",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §6"),
      dict(panel="B",estimate="Post-hoc linear depth slope (D_U-D_S)/2",classification="post-hoc exploratory",N_independent_instances=28,effect=.10714,ci_low="",ci_high="",p_raw=.037,p_adjusted="",ci_available="no",interpretation="approximate unadjusted p; hypothesis-generating only",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §6"),
      dict(panel="C",estimate="Fresh N=124 depth primary L=(D_U-D_S)/2",classification="prospective confirmatory",N_independent_instances=124,effect=.016129,ci_low=-.0354171,ci_high=.0676752,p_raw=.5368147,p_adjusted="",ci_available="yes",interpretation="pre-specified positive depth contrast not confirmed; not equivalence",source="projects/omi/research/OMI_3077_FRESH_DEPTH_CONFIRMATION_NULL_ADJUDICATION_20260919.md"),
      dict(panel="D",estimate="Fresh stage S secondary",classification="formal secondary after closed primary gate",N_independent_instances=124,effect=.0080645,ci_low="",ci_high="",p_raw=.821897,p_adjusted=1,ci_available="no",interpretation="no stage-specific confirmatory claim",source="projects/omi/research/OMI_3077_FRESH_DEPTH_CONFIRMATION_NULL_ADJUDICATION_20260919.md"),
      dict(panel="D",estimate="Fresh stage T secondary",classification="formal secondary after closed primary gate",N_independent_instances=124,effect=0,ci_low="",ci_high="",p_raw=1,p_adjusted=1,ci_available="no",interpretation="no stage-specific confirmatory claim",source="projects/omi/research/OMI_3077_FRESH_DEPTH_CONFIRMATION_NULL_ADJUDICATION_20260919.md"),
      dict(panel="D",estimate="Fresh stage U secondary",classification="formal secondary after closed primary gate",N_independent_instances=124,effect=.0403226,ci_low="",ci_high="",p_raw=.226692,p_adjusted=.680075,ci_available="no",interpretation="no stage-specific confirmatory claim",source="projects/omi/research/OMI_3077_FRESH_DEPTH_CONFIRMATION_NULL_ADJUDICATION_20260919.md")])
    write_csv("table1_protocol.csv",[
      dict(threat="Semantic confounding",measurement_failure="Treatment changes target-relevant information",safeguard="Task-relative semantic-information equivalence",omi_empirical_example="LOCAL/CROSS required alias/value matched; companion swap preserves role multiset",source="work/results/OMI-3078/IDENTIFICATION_FRAMEWORK.md §§3,5"),
      dict(threat="Computational redundancy",measurement_failure="Designated record is not needed to determine target",safeguard="Constructive oracle-necessity audit",omi_empirical_example="Earlier parent-value leakage removed before mature R4 instrument",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §2"),
      dict(threat="Scorer censoring",measurement_failure="Completed/readable errors leave denominator",safeguard="Freeze exact scorer; retain all completed/readable nonexact outputs as errors",omi_empirical_example="OMI-3057 prospective scorer repair",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §3"),
      dict(threat="Stochastic post-processing",measurement_failure="Downstream model changes worker measurement",safeguard="Deterministic readout when worker response is target",omi_empirical_example="Unnecessary stochastic finalizer removed prospectively",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §4"),
      dict(threat="Derived-data corruption",measurement_failure="Extracted ledger is not faithful to raw response",safeguard="Persist raw bytes before parse; second-pass raw/derived reconciliation",omi_empirical_example="False all-zero ledger corrected from 336 raw responses without replay",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §5"),
      dict(threat="Resource censoring",measurement_failure="Cap prevents planned response from existing",safeguard="Prospective resource qualification; integrity classification",omi_empirical_example="2048 stop at ordinal 335; fresh 8192 qualification before new bank",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §§8-9"),
      dict(threat="Selected continuation",measurement_failure="Retry/replacement reweights accepted outcomes",safeguard="One planned attempt for first-attempt estimand; stop on integrity failure",omi_empirical_example="Final N=124 bank used no retry/replay/replacement/imputation",source="work/results/OMI-3078/REPRODUCIBILITY_PROTOCOL.md §§E3-E4"),
      dict(threat="Pseudo-replication",measurement_failure="Calls nested in one instance treated as independent",safeguard="Aggregate/test at independent instance or justify cluster model",omi_empirical_example="Frozen N=124 analysis used instance-level endpoint",source="work/results/OMI-3078/IDENTIFICATION_FRAMEWORK.md §7"),
      dict(threat="Outcome-informed confirmation",measurement_failure="Exploratory pattern reused as confirmatory evidence",safeguard="Wholly fresh prospective bank and frozen primary",omi_empirical_example="Post-hoc +0.10714 depth slope tested on fresh N=124; not confirmed",source="work/results/OMI-3078/EMPIRICAL_EVIDENCE_SYNTHESIS.md §§6-11"),
      dict(threat="Fixed-bank incompleteness",measurement_failure="Exposed prefix promoted after failure",safeguard="First integrity failure stops confirmatory bank; no prefix confirmation",omi_empirical_example="Partially exposed R4DP bank never resumed or used as confirmation",source="work/results/OMI-3078/REPRODUCIBILITY_PROTOCOL.md")])

def main():
    DATA.mkdir(parents=True,exist_ok=True); write_static_data()
    sr,ss=scorer(); mr,ms=missingness(); rr,rs=retry(); fr,fs=finalizer(); qr,qs=resource()
    pr,ps=pseudorep(); br,bs=bank(); ez,er,es=extraction()
    for name,rows in [
      ("fig2_scorer_censoring_surface.csv",sr),("fig2_missingness_surface.csv",mr),
      ("fig2_retry_acceptance_surface.csv",rr),("fig2_finalizer_surface.csv",fr),
      ("fig2_resource_surface.csv",qr),("fig2_pseudorep_surface.csv",pr),
      ("fig2_pseudorep_validation.csv",ps["validation"]),("fig2_bank_completion_surface.csv",br),
      ("fig2_extraction_zero_map_surface.csv",ez),("fig2_extraction_outcome_dependent_row_loss_surface.csv",er)]:
        write_csv(name,rows)
    result=dict(task="OMI-3079",version="1.0",seed=BASE_SEED,behavioral_provider_calls=0,scientific_spend=0,
      computation=dict(analytic_expectations="deterministic numerical integration under frozen D~N(0,1); reference landmarks cross-checked by Gauss-Hermite quadrature",
                       validation_simulation=f"deterministic Gaussian exchangeable-cluster Monte Carlo, {VALIDATION_REPS} reps per selected point"),
      frozen_synthetic_model=dict(latent_accuracy="logit^-1(1.25 - 0.85*difficulty + beta*z)",difficulty="N(0,1)",
                                  resource_demand="log Q=log(350)+0.5*difficulty+delta*z+Normal(0,0.7^2)"),
      marginal_accuracy_landmarks={"beta_0":marginal(0),"beta_0.25":marginal(.25),"beta_0.30":marginal(.3)},
      surfaces=dict(scorer_censoring=ss,treatment_correlated_missingness=ms,retry_replacement=rs,
                    stochastic_finalizer=fs,resource_truncation=qs,pseudo_replication=ps,
                    fixed_bank_integrity=bs,derived_ledger_extraction=es),
      parameter_range_principle="Ranges fixed from probability-domain support or symmetric/model-scale extensions around the frozen OMI-3078 examples before inspecting surfaces; none selected to maximize visual effect.",
      scope=["Exact algebraic boundaries are exact only under stated measurement models.",
             "Numerical surfaces are deterministic consequences of the frozen synthetic latent/demand models.",
             "Monte Carlo is used only to validate pseudo-replication alpha behavior at representative points.",
             "No synthetic magnitude is calibrated to or asserted as the historical OMI bias.",
             "B=1488 and K=6 are scale markers only where stated."])
    RESULT_JSON.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    package=dict(schema="OMI-3079 figure data package",version="1.0",generated_by="SENSITIVITY_SURFACE_FRAMEWORK.py",
                 surface_results=result,empirical_files=["figure_data/fig3_empirical_ladder.csv","figure_data/fig4_effect_estimates.csv","figure_data/table1_protocol.csv"],
                 figure1_files=["figure_data/fig1_pipeline_nodes.csv","figure_data/fig1_pipeline_edges.csv"])
    (DATA/"figure_data_package.json").write_text(json.dumps(package,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
