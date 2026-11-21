from pathlib import Path
import json,shutil,zipfile
import pandas as pd
import numpy as np
P=Path(__file__).resolve().parent
df=pd.read_csv(P/'case_results.csv');sel=pd.read_csv(P/'selected_cases.csv')
stats=json.loads((P/'summary.json').read_text())
verify=json.loads((P/'additional_verification.json').read_text())
rows=[]
for _,r in sel.iterrows():
 rows.append(f'{r.f:.0f} & {r.valve_in_mm:.0f} & {r.pc_peak_mmhg:.0f} & {r.force_peak_N:.1f} & {abs(min(0,r.force_min_N)):.1f} & {r.Q_Lmin:.2f} \\\\')
table='\n'.join(rows)
sens=[]
for _,r in df[(df.group=='timing')&(df.valve_in_mm==16)&(df.f==180)].sort_values('ejection_fraction').iterrows():
 sens.append(f'{100*r.ejection_fraction:.0f}\\% & {r.force_absmax_N:.1f} & {r.Q_Lmin:.2f} \\\\')
mid=df[(df.group=='main')&(df.valve_in_mm==16)&(df.f==180)&(df.gas_ref_ml==10)].iloc[0]
sens.insert(1,f'40\\% & {mid.force_absmax_N:.1f} & {mid.Q_Lmin:.2f} \\\\')
sens='\n'.join(sens)
template=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=20mm,headheight=15pt]{geometry}
\usepackage{amsmath,amssymb,booktabs,tabularx,array,graphicx,xcolor,fancyhdr,hyperref,microtype}
\definecolor{navy}{HTML}{17324D}\definecolor{teal}{HTML}{007F85}
\hypersetup{colorlinks=true,urlcolor=teal,linkcolor=teal,citecolor=teal,pdftitle={Piston hydraulic force: first numerical sweep}}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small MECH0073}\fancyhead[R]{\small\nouppercase{\rightmark}}\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{.3pt}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\renewcommand{\labelitemi}{$\bullet$}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}\renewcommand{\arraystretch}{1.15}
\newcommand{\stage}[1]{\markright{#1}{\Large\bfseries\color{navy}#1}\par\medskip}
\newcommand{\topic}[1]{\par\smallskip{\bfseries\color{navy}#1}\par}
\begin{document}
\stage{Peak hydraulic force: first sweep}
\textbf{Scope.} Numerical tests of a prescribed piston-volume trajectory, ideal check valves, a retained gas pocket and fixed upstream/downstream pressure loads. These isolate hydraulic force. The actuator, converter, seal friction and translating-solid inertia are excluded. Results are conditional model predictions, not measured loads, verified component ratings or a complete motor-force requirement.

\topic{Inputs and provenance}
\begin{tabularx}{\linewidth}{@{}p{.30\linewidth}Y@{}}\toprule
\textbf{Quantity} & \textbf{Baseline and sweep}\\\midrule
Geometric swept volume & 66.667 mL, derived from the user's ideal 5 L/min at 75/min reference. Actual simulated delivery is solved, not prescribed to equal this volume.\\
Piston face / travel & Illustrative $D=50$ mm, $S=33.95$ mm. Diameter comparison: 30--70 mm with travel changed to preserve swept volume.\\
Delivery frequency & 40, 60, 75, 90, 120, 150 and 180 events/min.\\
Valve bores & Both inlet and outlet: 8, 12, 16 or 20 mm; assumed $C_d=0.7$. Selected sensitivity cases use 0.6 and 0.8.\\
Pressure boundaries & Inlet 10, outlet 90 mmHg gauge; outlet sensitivity 120 and 200. Values drawn from PDS reference levels, but holding them constant is a test assumption. Rear at atmosphere.\\
Air pocket & 1, 10 or 20 mL at 10 mmHg gauge; baseline 10 mL. Atmospheric pressure 760 mmHg; $n=1.2$, with selected $n=1$ and 1.4 tests. All assumed.\\
Fluid / connected lines & Assumed density 1000 kg/m$^3$. Each line: 20 mm bore, 0.2 m effective inertial length, lumped quadratic loss coefficient $K=1$. No calibrated viscosity-dependent friction model.\\
Motion / residual volume & Quintic advance in 40\% of cycle and return in 60\%; selected 30/70 and 50/50 tests. Minimum chamber volume 40 mL. All assumed.\\\bottomrule
\end{tabularx}

\topic{Representative periodic-cycle results}
Baseline air, motion, fluid and boundary pressures above apply to this table. Push and pull are magnitudes of the opposing signed pressure-load extrema, not total actuator loads.
\begin{center}\small
\begin{tabular}{@{}rrrrrr@{}}\toprule
$f$ (min$^{-1}$)& Valve (mm)& Peak $p_c$ (mmHg)& Push (N)& Pull (N)& $\bar Q$ (L/min)\\\midrule
@@ROWS@@
\bottomrule\end{tabular}
\end{center}
The largest reported numerical peak over all sensitivity cases is approximately \textbf{1275 N}: 180/min, 8 mm valves and a 30\% advance fraction, with the other baseline inputs. The corresponding chamber pressure is about 4870 mmHg gauge, despite the outlet being held at 90 mmHg. This is a demanded internal load under assumed perfect motion tracking; it is not an endorsed operating condition. No overall force rating should be selected from it without reviewing the admissible hydraulic cases.

\newpage\stage{Frequency, valves and geometry}
\begin{center}\includegraphics[width=\linewidth]{Hydraulic_force_trends.png}\end{center}
\textbf{Figure 1.} Parameter trends for the stated hydraulic model. Panels A and B use logarithmic force axes. The 2--7 L/min shading is the PDS flow range, not a claim that all frequency/load combinations must be selected.

\topic{What the calculations indicate}
\begin{itemize}
\item Valve enlargement gives the largest benefit when valve loss dominates. At 75/min, 8 to 12 mm reduces peak force from about 145 to 50 N; 16 to 20 mm leaves it near 41 N. The near-plateau reflects the remaining inertia/storage dynamics, not a universal optimal bore.
\item Frequency increases force substantially for unchanged travel and timing proportions. With 16 mm valves, the peak rises from about 41 N at 75/min to 94 N at 180/min for the 90 mmHg outlet test.
\item For unchanged swept-volume history and hydraulic geometry, pressure is independent of piston diameter in this lumped model, so force scales as $D^2$. Diameter scaling changes stroke length; it does not include changes to seal friction or chamber-port geometry.
\item Fixed travel gives approximately 12 L/min at 180/min in these cases. The current sweep does not impose independent 5 L/min control at that frequency.
\end{itemize}
\textbf{Pressure distinction.} The reported force uses chamber pressure, which can exceed outlet pressure because of valve/line loss and fluid acceleration. Using only 90 or 200 mmHg multiplied by piston area would miss that additional load.

\newpage\stage{Force timing and retained air}
\begin{center}\includegraphics[width=\linewidth]{Hydraulic_force_waveforms.png}\end{center}
\textbf{Figure 2.} Signed pressure load over a periodic cycle and gas-volume sensitivity. Force scales differ between waveform panels. Crosses at zero gas indicate a separate imposed-full-fill reference with no chamber storage. The 8 mm, 180/min references at zero and 1 mL fail the chosen minimum-pressure screen and are omitted from that panel.

\topic{Air does not guarantee a smaller peak}
For 16 mm valves at 75/min, the gas-free reference gives 33.7 N, while 1, 10 and 20 mL retained pockets give approximately 37.7, 40.7 and 42.4 N. Gas compliance changes the timing of fluid acceleration and valve flow. For the strongly restricted 8 mm, 180/min case, increasing reference gas volume from 10 to 20 mL reduces peak force from 724 to 671 N, but mean flow also falls from 11.92 to 11.19 L/min and the end-of-filling liquid deficit increases from 5.4 to 11.7 mL. These are model-specific trends.

\topic{Motion timing remains necessary even without choosing a mechanism}
For 16 mm valves, 180/min, 10 mL reference air and 90 mmHg constant outlet pressure:
\begin{center}\begin{tabular}{@{}rrr@{}}\toprule
Advance fraction of cycle & Peak $|F_p|$ (N)& Mean flow (L/min)\\\midrule
@@TIMING@@
\bottomrule\end{tabular}\end{center}
The same travel and frequency can therefore give markedly different force peaks. These are smooth prescribed trajectories; no crank, cam or gear mechanism has been selected.

\newpage\stage{Equations and numerical implementation}
The hydraulic equations below use SI units. Delivery frequency $f$ is specified in events/min, so $T=60/f$ is in seconds. The code converts constitutive coefficients to mmHg, mL and seconds internally. It uses $1$ mmHg $=133.322387415$ Pa.

Let $u(t)=A_p x(t)$ be piston displacement volume, positive on advance. For a rigid chamber and incompressible liquid with a retained polytropic gas pocket,
\begin{equation}
V_g=V_{g0}\left(\frac{p_{g0,\mathrm{abs}}}{p_{c,\mathrm{abs}}}\right)^{1/n},\qquad
C_g=\frac{V_g}{n p_{c,\mathrm{abs}}},\qquad
C_g\dot p_c=Q_i-Q_o+\dot u.
\end{equation}
Each open hydraulic leg follows
\begin{equation}
I_i\dot Q_i=p_i-p_c-B_iQ_i|Q_i|,\qquad
I_o\dot Q_o=p_c-p_o-B_oQ_o|Q_o|,
\end{equation}
\begin{equation}
B_j=\frac{\rho}{2}\left[\frac{1}{(C_d A_{v,j})^2}+\frac{K}{A_t^2}\right],\qquad
I_j=\frac{\rho\ell}{A_t},\qquad
A_{v,j}=\frac{\pi d_{v,j}^2}{4},\quad A_t=\frac{\pi d_t^2}{4}.
\end{equation}
The lumped quadratic $K$ is assumed, not inferred from a selected tube or fluid viscosity. This is not yet a calibrated BMF model. The nonlinear loss/inertia structure has a published cardiovascular modelling precedent \cite{broome}; numerical coefficients here are exploratory.

Valves are ideal, zero-cracking-pressure check elements: a closed valve opens for positive forward pressure gradient; an open valve closes when its forward flow reaches zero. Inertance allows flow to continue temporarily after the gradient reverses. The solver locates those events and resets the closed-leg flow to zero. Finite leaflet motion, reverse flow during closure and distributed pressure waves are not resolved.

The smooth profile uses $h(z)=10z^3-15z^4+6z^5$. With $T=60/f$ and advance fraction $\gamma$,
\begin{equation}
u(t)=\begin{cases} V_s h(t/(\gamma T)),&0\leq t<\gamma T,\\
V_s[1-h((t-\gamma T)/((1-\gamma)T))],&\gamma T\leq t<T.
\end{cases}
\end{equation}
Both velocity and acceleration vanish at the phase endpoints. The reported quantities are
\begin{equation}
F_p(t)=A_p[p_c(t)-p_b],\qquad F_{p,\max}=\max_{0\leq t<T}|F_p(t)|,\qquad
\bar Q=\frac{1}{T}\int_0^T Q_o(t)\,\mathrm dt.
\end{equation}
The piston rear is atmospheric, so $p_c$ can be used as gauge pressure in the force equation. Liquid inventory is $V_\ell=V_{\min}+V_s-u-V_g$; the end-of-filling deficit is relative to the full-retraction liquid volume at the 10 mmHg reference pressure. This inventory deficit and net delivery ratio are distinct.

\textbf{Full-fill reference.} With no gas/storage, imposed liquid flow equals the piston displacement rate. Pressure is obtained from the same quadratic loss and fluid-inertance terms. This algebraic reference is screened for low chamber pressure; an impossible fully filled solution is not treated as a feasible pump prediction.

\newpage\stage{Verification and limits of interpretation}
\topic{Numerical checks performed}
\textbf{118 dynamic cases were attempted: 117 reached periodic operation and one was stopped by a model-validity guard.} The stopped case was 180/min, 8 mm inlet/outlet valves and a 1 mL reference gas pocket. Its absolute chamber pressure reached the chosen 50 mmHg (6.67 kPa) floor. This is an explicit exploratory guard, not a measured cavitation threshold or a guarantee against local valve cavitation. No periodic force is reported for that case. A separate liquid-inventory guard would stop a case below 0.1 mL retained liquid; none triggered.

SciPy's implicit Radau solver was used with relative tolerance $2\times10^{-7}$ and maximum step $T/120$, resolving valve events. Up to 24 cycles were allowed. Periodicity required a scaled state change below $2\times10^{-7}$, with at least three cycles. Flow integrals were solver states. Peaks were sampled at 2401 times over the final cycle.

Across completed cases, maximum chamber-volume balance error was $3.14\times10^{-6}$ mL and maximum inlet/outlet cycle-volume mismatch was $4.77\times10^{-7}$ mL. These quantify numerical conservation, not physical accuracy. No negative valve flow occurred beyond numerical tolerance.

Three representative cases were refined, including the largest-force case, with relative tolerance $2\times10^{-9}$, maximum step $T/360$ and 7201 peak samples. Peak-force changes were below 0.001\%; the largest minimum-pressure change among these checks was about 0.010\%. This is limited numerical verification of the chosen model, not experimental validation or proof that all model errors are small.

\topic{Interpretation limits that affect the force estimate}
\begin{itemize}
\item The upstream and downstream pressures are constant boundary tests. Reservoir depletion, left/right volume balance and actual Windkessel pressure waveforms are not simulated. Their supplied pressure histories should replace these boundaries in a later coupled run.
\item Some net-delivery/swept-volume ratios exceed one slightly: the ideal inertial valve model permits forward flow across piston reversals and brief overlap of inlet/outlet flow. Treat this ratio as a model output, not a calibrated volumetric efficiency constrained below one. Finite valve dynamics require validation.
\item Gas heat transfer, dissolution, liquid compressibility, wall compliance and cavitation are omitted here. A reciprocating-pump CFD study demonstrates why compressibility and valve/cavitation coupling matter when those regimes are reached \cite{iannetti}. This sweep does not establish cavitation-free operation.
\item The reported maxima are periodic hydraulic-pressure forces. Start/stop shocks, blocked-path events, seal friction, moving-solid inertia and converter forces are outside the result. A manufactured pump must also satisfy internal-pressure and flow-path constraints.
\item There is no universal maximum force without specifying admissible pressure loads and motion timing. The largest stress-case result in this sweep is not a recommendation to choose that force as the pump rating.
\end{itemize}

\textbf{Next design decision.} Use the current results to narrow valve and piston geometry candidates, then replace the assumed $C_d$, line losses, gas state and inlet/outlet pressure histories with component data or measurements. Apply a scored decision matrix only after the selected operating cases are hydraulically feasible.

\newpage\stage{Files, reproduction and evidence}
\topic{Reproducibility package}
The accompanying ZIP includes the model and plot/report scripts, this LaTeX source, figures, every case summary, three representative full-cycle waveform records, and the refinement results. The main data file is \texttt{case\_results.csv}; \texttt{full\_fill\_reference.csv} contains 28 algebraic reference cases with pressure-screen flags. Stopped cases retain their parameters and status, with no fabricated force result.

Run \texttt{python hydraulic\_sweep.py --test}, then \texttt{python hydraulic\_sweep.py --sweep}; run \texttt{python make\_outputs.py} and \texttt{python make\_report.py} to regenerate the figures and report source. Compile \texttt{Hydraulic\_force\_sweep.tex} with pdfLaTeX twice. The supplied additional verification script can regenerate the maximum-case and baseline refinement checks.

\textbf{Recorded software:} Python 3.12 runtime; NumPy, pandas and Matplotlib; SciPy 1.17.0. Exact installed versions are recorded in \texttt{environment.json}. All plotted numerical results are generated by these scripts; no experimental data are presented.

\topic{Requirement provenance and model evidence}
The user's prescribed 5 L/min at 75/min sets the 66.667 mL geometric reference. The current project \texttt{PDS\_Pump.pdf}, pages 1 and 5, supplies the nominal 10/90 mmHg inlet/outlet pressure references, 2--7 L/min flow range and 40--180/min rate range. Its instantaneous outlet peak reference of 200 mmHg is used here only as an additional constant load test; that is not a physiological waveform. All other numerical inputs are stated modelling assumptions and remain uncalibrated.

\begin{thebibliography}{9}
\bibitem{broome} Broom\'e M, Maksuti E, Bj\"allmark A, Frenckner B, Janerot-Sj\"oberg B. Closed-loop real-time simulation model of hemodynamics and oxygen transport in the cardiovascular system. Biomed Eng Online. 2013;12:69. \href{https://doi.org/10.1186/1475-925X-12-69}{doi:10.1186/1475-925X-12-69}. Full text consulted for the nonlinear valve-loss and inertance model structure.
\bibitem{iannetti} Iannetti A, Stickland MT, Dempster WM. A CFD study on the mechanisms which cause cavitation in positive displacement reciprocating pumps. Journal of Hydraulic Engineering. 2015;1(1):47--59. \href{https://doi.org/10.17265/2332-8215/2015.01.005}{doi:10.17265/2332-8215/2015.01.005}. Author manuscript consulted for limits of incompressible and valve/cavitation simplifications; its CFD results are not validation of this model.
\end{thebibliography}
\end{document}
'''
(P/'Hydraulic_force_sweep.tex').write_text(template.replace('@@ROWS@@',table).replace('@@TIMING@@',sens))
import sys, scipy,matplotlib
(P/'environment.json').write_text(json.dumps({'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},indent=2))
print('Report source written.')
