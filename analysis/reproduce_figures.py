#!/usr/bin/env python3
"""Regenerate the public NMI figure package from frozen the frozen public figure data.

No provider/model calls. No empirical refitting. Figure 4 uses only frozen CIs.
Outputs: SVG, PDF and 300-dpi PNG for Figures 1–4.
Dependencies: numpy, pandas, matplotlib.
"""
from pathlib import Path
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "figure_data"
OUT = ROOT / "figures"
FORMATS = ("svg", "pdf", "png")

def save(fig, stem):
    for ext in FORMATS:
        kw = {"bbox_inches": "tight"}
        if ext == "png":
            kw["dpi"] = 300
        fig.savefig(OUT / f"{stem}.{ext}", **kw)
    plt.close(fig)

def box(ax, x, y, w, h, text, fs=9, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                       facecolor="white", edgecolor="black",
                       linewidth=1.0, linestyle=ls)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs, wrap=True)

def figure1():
    fig = plt.figure(figsize=(12, 7.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[0.82, 1.18], width_ratios=[1.7, 1.0])
    a = fig.add_subplot(gs[0,0]); b = fig.add_subplot(gs[0,1])
    c = fig.add_subplot(gs[1,0]); d = fig.add_subplot(gs[1,1])
    for ax, letter, title in [(a,"a","Matched provenance intervention"),
                              (b,"b","Computational necessity"),
                              (c,"c","Measurement chain"),
                              (d,"d","Identification versus detection")]:
        ax.set_axis_off()
        ax.set_title(f"{letter}  {title}", loc="left", fontweight="bold", fontsize=11)

    a.set_xlim(0,1); a.set_ylim(0,1)
    a.text(.02,.76,"z=0",fontweight="bold"); a.text(.02,.38,"z=1",fontweight="bold")
    box(a,.15,.68,.34,.18,"A: same alias/value\nprovenance role 0")
    box(a,.55,.68,.34,.18,"B: same alias/value\nprovenance role 1")
    box(a,.15,.30,.34,.18,"A: same alias/value\nprovenance role 1")
    box(a,.55,.30,.34,.18,"B: same alias/value\nprovenance role 0")
    a.text(.02,.08,"Fixed: prompt, semantic values, record count/order,\nrole multiset, model/settings/resources.",fontsize=8)

    b.set_xlim(0,1); b.set_ylim(0,1)
    box(b,.05,.65,.28,.16,"World w\nA=v"); box(b,.67,.65,.28,.16,"oracle=g")
    box(b,.05,.33,.28,.16,"World w′\nA=v′"); box(b,.67,.33,.28,.16,"oracle=g′")
    b.annotate("",(.66,.73),(.34,.73),arrowprops=dict(arrowstyle="->"))
    b.annotate("",(.66,.41),(.34,.41),arrowprops=dict(arrowstyle="->"))
    b.text(.04,.07,"Same prompt + nondesignated information.\nTask/oracle necessity ≠ internal neural mechanism.",fontsize=8)

    # Panel c: compact two-row pipeline; detailed definitions remain in the legend/Methods.
    c.set_xlim(0,1); c.set_ylim(0,1)
    top=[("Independent\ninstance",.08),
         ("Matched pair\nz=0 / z=1",.28),
         ("Worker\nresponse",.48),
         ("Completion /\nreadability",.68),
         ("Raw-response\ncustody",.88)]
    bottom=[("Instance-level\ninference",.28),
            ("Within-instance\naggregation",.48),
            ("Frozen\nscore",.68),
            ("Deterministic\nextraction",.88)]
    bw=.145; bh=.12; yt=.69; yb=.37
    for label,x in top:
        box(c,x-bw/2,yt-bh/2,bw,bh,label,fs=7.2)
    for label,x in bottom:
        box(c,x-bw/2,yb-bh/2,bw,bh,label,fs=7.2)

    def arr(x0,y0,x1,y1,ls="-"):
        c.annotate("",xy=(x1,y1),xytext=(x0,y0),
                   arrowprops=dict(arrowstyle="->",linewidth=.9,linestyle=ls,
                                   shrinkA=18,shrinkB=18))
    for x0,x1 in zip([.08,.28,.48,.68],[.28,.48,.68,.88]):
        arr(x0,yt,x1,yt)
    arr(.88,yt,.88,yb)
    for x0,x1 in zip([.88,.68,.48],[.68,.48,.28]):
        arr(x0,yb,x1,yb)

    # Integrity failure is a side branch from the completion gate.
    box(c,.59,.08,.18,.12,"Integrity failure:\nplanned observation absent",fs=6.7,ls="--")
    arr(.68,yt,.68,.20,"--")
    # Completed/readable nonexact behavior is retained by the score rather than dropped.
    c.text(.68,.24,"nonexact → score 0\n(retained in denominator)",
           ha="center",va="center",fontsize=6.6)
    c.text(.02,.95,"Solid: intended measurement path   ·   dashed: integrity branch",
           fontsize=7.2)

    d.set_xlim(0,1); d.set_ylim(0,1)
    box(d,.12,.63,.76,.18,"Identification\nWhat intervention is isolated under assumptions",fs=9)
    box(d,.12,.31,.76,.18,"Detection\nWhat observed data support statistically",fs=9)
    d.text(.5,.08,"An identified estimand can yield a non-detection.",
           ha="center",fontweight="bold",fontsize=8)

    fig.suptitle("Identification and measurement pipeline for contextual provenance experiments",
                 fontsize=14, fontweight="bold")
    fig.tight_layout()
    save(fig, "Figure1")

def pivot(path, index, columns, value):
    d = pd.read_csv(DATA / path)
    p = d.pivot(index=index, columns=columns, values=value).sort_index().sort_index(axis=1)
    return d, p.index.to_numpy(), p.columns.to_numpy(), p.to_numpy()

def heat(ax, path, index, columns, value, title, xlabel, ylabel, sequential=False):
    d,y,x,z = pivot(path,index,columns,value)
    if sequential:
        im=ax.imshow(z,origin="lower",aspect="auto",extent=[x.min(),x.max(),y.min(),y.max()],
                     cmap="viridis",vmin=np.nanmin(z),vmax=np.nanmax(z))
    else:
        m=np.nanmax(np.abs(z))
        im=ax.imshow(z,origin="lower",aspect="auto",extent=[x.min(),x.max(),y.min(),y.max()],
                     cmap="coolwarm",vmin=-m,vmax=m)
        if np.nanmin(z) <= 0 <= np.nanmax(z):
            ax.contour(x,y,z,levels=[0],linewidths=.8,colors="black")
    ax.set_title(title,loc="left",fontweight="bold",fontsize=9)
    ax.set_xlabel(xlabel,fontsize=7); ax.set_ylabel(ylabel,fontsize=7)
    ax.tick_params(labelsize=6)
    return im

def figure2():
    fig,axs=plt.subplots(3,3,figsize=(12.5,10.6))
    ims=[]
    ims.append(heat(axs[0,0],"fig2_scorer_censoring_surface.csv",
                    "treatment_correct_retention","treatment_incorrect_retention",
                    "apparent_effect_treatment_minus_control","a  Scorer retention",
                    "incorrect-output retention","correct-output retention"))
    ims.append(heat(axs[0,1],"fig2_missingness_surface.csv",
                    "treatment_observation_intercept","treatment_observation_slope_on_difficulty",
                    "complete_case_apparent_effect","b  Observation selection",
                    "difficulty slope γ","intercept α"))
    ims.append(heat(axs[0,2],"fig2_retry_acceptance_surface.csv",
                    "treatment_pass_if_correct","treatment_pass_if_incorrect",
                    "accepted_effect","c  Acceptance weighting",
                    "pass if incorrect","pass if correct"))
    ims.append(heat(axs[1,0],"fig2_finalizer_surface.csv",
                    "treatment_sensitivity","treatment_false_positive_probability",
                    "measured_effect","d  Finalizer channel",
                    "false-positive probability","sensitivity"))
    ims.append(heat(axs[1,1],"fig2_resource_surface.csv",
                    "treatment_log_demand_shift","log2_output_cap",
                    "complete_case_distortion","e  Resource truncation",
                    "log2(output cap)","treatment log-demand shift"))
    axs[1,1].text(.02,.02,"Synthetic demand model; not calibrated to OMI",
                  transform=axs[1,1].transAxes,fontsize=6,
                  bbox=dict(facecolor="white",alpha=.8,edgecolor="none"))
    ims.append(heat(axs[1,2],"fig2_pseudorep_surface.csv",
                    "icc_rho","calls_per_instance_K",
                    "normal_approx_actual_alpha_if_calls_treated_independent",
                    "f  Pseudo-replication","calls per instance K","ICC ρ",sequential=True))

    g=pd.read_csv(DATA/"fig2_bank_completion_surface.csv")
    g["log10_h"]=np.log10(g["per_call_hazard_h"])
    gp=g.pivot(index="log10_h",columns="bank_size_B",values="full_bank_probability").sort_index().sort_index(axis=1)
    y=gp.index.to_numpy(); x=gp.columns.to_numpy(); z=gp.to_numpy()
    im=axs[2,0].imshow(z,origin="lower",aspect="auto",
                       extent=[x.min(),x.max(),y.min(),y.max()],cmap="viridis",vmin=0,vmax=1)
    axs[2,0].contour(x,y,z,levels=[.5,.8,.9,.95,.99],linewidths=.7,colors="black")
    axs[2,0].set_title("g  Full-bank completion",loc="left",fontweight="bold",fontsize=9)
    axs[2,0].set_xlabel("bank size B",fontsize=7); axs[2,0].set_ylabel("log10(per-call hazard)",fontsize=7)
    axs[2,0].tick_params(labelsize=6); ims.append(im)

    ims.append(heat(axs[2,1],"fig2_extraction_zero_map_surface.csv",
                    "control_extraction_success_random_within_arm",
                    "treatment_extraction_success_random_within_arm",
                    "derived_effect","h  Extraction mapped to zero",
                    "treatment extraction success","control extraction success"))
    ims.append(heat(axs[2,2],"fig2_extraction_outcome_dependent_row_loss_surface.csv",
                    "treatment_correct_extraction_retention",
                    "treatment_incorrect_extraction_retention",
                    "complete_case_apparent_effect","i  Outcome-dependent extraction",
                    "incorrect-row retention","correct-row retention"))
    for ax,im in zip(axs.flat,ims):
        fig.colorbar(im,ax=ax,shrink=.72,pad=.02).ax.tick_params(labelsize=5.5)
    fig.suptitle("Evaluation infrastructure can alter an apparent treatment effect\n"
                 "Analytic/deterministic synthetic surfaces — not OMI empirical estimates",
                 fontsize=13,fontweight="bold")
    fig.tight_layout(rect=(0,0,1,.95))
    save(fig,"Figure2")

def figure3():
    d=pd.read_csv(DATA/"fig3_empirical_ladder.csv")
    fig,ax=plt.subplots(figsize=(13,8.3)); ax.axis("off")
    cols=[.01,.18,.43,.71]; widths=[22,34,38,40]
    headers=["Observed failure","Scientific threat","Prospective safeguard","Empirical anchor"]
    for x,h in zip(cols,headers):
        ax.text(x,.97,h,transform=ax.transAxes,fontweight="bold",fontsize=10,va="top")
    top=.91; step=.125
    for k,(_,r) in enumerate(d.iterrows()):
        y=top-k*step
        if k%2==0:
            ax.add_patch(plt.Rectangle((0,y-.10),1,.11,transform=ax.transAxes,
                                       facecolor=".96",edgecolor=".85"))
        vals=[f"{int(r.order)}. {r.incident}",r.scientific_threat,r.prospective_safeguard,
              str(r.omi_empirical_example)]
        for x,val,w in zip(cols,vals,widths):
            ax.text(x,y,"\n".join(textwrap.wrap(str(val),w)),transform=ax.transAxes,
                    fontsize=8.2,va="top",fontweight="bold" if x==cols[0] else "normal")
    ax.set_title("Measurement failures and prospective safeguards in OMI",
                 loc="left",fontweight="bold",fontsize=13)
    ax.text(.01,.015,
            "Historical states were preserved; the sequence represents measurement hardening, not accumulation of positive evidence.",
            transform=ax.transAxes,fontsize=8.8,fontweight="bold")
    save(fig,"Figure3")

def figure4():
    d=pd.read_csv(DATA/"fig4_effect_estimates.csv")
    labels=["Corrected overall confirmatory","Exploratory stage S","Exploratory stage T",
            "Exploratory stage U","Post-hoc depth slope","Fresh N=124 depth primary",
            "Fresh stage S secondary","Fresh stage T secondary","Fresh stage U secondary"]
    fig,ax=plt.subplots(figsize=(10.2,6.8))
    y=np.arange(len(d))[::-1]
    ax.axvline(0,linewidth=1,linestyle="--",color="black")
    for yi,(_,r),lab in zip(y,d.iterrows(),labels):
        x=float(r.effect)
        if str(r.ci_available).lower()=="yes":
            lo,hi=float(r.ci_low),float(r.ci_high)
            ax.errorbar(x,yi,xerr=[[x-lo],[hi-x]],fmt="s",capsize=3,color="black")
        else:
            ax.plot(x,yi,"o",markerfacecolor="white",markeredgecolor="black")
    ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=8)
    ax.set_xlim(-.10,.18)
    ax.set_xlabel("LOCAL − CROSS effect / frozen depth contrast")
    ax.set_title("Confirmatory and exploratory provenance contrasts in OMI",
                 loc="left",fontweight="bold",pad=12)
    ax.grid(axis="x",linewidth=.4,alpha=.4)
    fig.tight_layout()
    save(fig,"Figure4")

if __name__=="__main__":
    figure1(); figure2(); figure3(); figure4()
    print(f"Wrote Figures 1–4 as SVG/PDF/PNG to {OUT}")
