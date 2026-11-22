# Derivation 04 — retained-air storage and passive valve events

22 November 2026. Analytical development for review. No new coupled simulation,
MATLAB execution, waveform result or force rating is claimed by this document.
The interactive application follows completion and numerical verification of the
necessary derivation, as clarified by the user.

This step combines the chamber storage idea already present in the exploratory
Python solver with the arterial-load interface developed in Derivation 03.
The existing implementations remain separate and unchanged in this update.

## 1. Model boundary, assumptions and variables

Use one flat-face plunger chamber as the building block. An upstream reservoir
feeds an inlet valve/path; an outlet valve/path connects to the arterial load.
Gas is deliberately retained within the chamber, with fixed mass. No gas enters
or leaves through either liquid port, and dissolution is neglected over a run.

Assume incompressible liquid, a rigid cylinder, negligible leakage, approximately
uniform piston-face/chamber pressure, and gas pressure equal to chamber liquid
pressure. The latter omits hydrostatic, capillary and interface-motion pressure
differences. If a retaining membrane is introduced, its pressure–volume law must
be added; gas pressure cannot automatically be equated to liquid pressure.

| Symbol | Meaning | SI unit |
| --- | --- | --- |
| x, S | Piston advance from full retraction; total travel | m |
| Ap | Wetted flat-face area, with no rod subtraction | m² |
| Vc, Vc0 | Total chamber volume; value at full retraction | m³ |
| Vl, Vg | Liquid volume; retained-gas volume | m³ |
| Qi, Qo | Forward inlet and outlet liquid flows | m³/s |
| Qp | Piston displaced-volume rate, positive on advance | m³/s |
| pc, pi, pa, pb | Chamber, inlet, arterial and dry rear-face gauge pressures | Pa |
| patm, pg | Atmospheric pressure; absolute gas pressure | Pa |
| Vg,ref, pg,ref | Known gas volume at a declared reference absolute pressure | m³; Pa |
| n | Constant trial polytropic exponent | dimensionless |
| Cg | Differential chamber gas compliance | m³/Pa |
| Rj, Bj, Ij | Linear resistance, quadratic loss coefficient and fluid inertance, j = i or o | Pa s/m³; Pa s²/m⁶; Pa s²/m³ |
| pw, pr | Arterial compliance-node pressure; terminal return pressure | Pa gauge |
| R1, R2, Cw | Proximal/distal load resistance and arterial compliance | Pa s/m³; m³/Pa |

All pressure differences use a common reference. Gas thermodynamics uses
absolute pressure, pg = patm + pc, with patm constant in this first model.
The chamber gas compliance Cg is distinct from the external Windkessel Cw.

The initial valve model is an ideal passive check valve with zero cracking
pressure and no reverse leakage. It includes fluid inertia but no moving-leaflet
state. Actual linked or actively commanded valves will require their own state
law; this baseline does not select a final valve mechanism.

## 2. Derive the chamber storage balance

With positive x pointing into the fluid chamber,

$$
A_p=\frac{\pi D_p^2}{4},\qquad
V_c=V_{c0}-A_px=V_\ell+V_g,\qquad
Q_p=A_p\dot x.
$$

Conservation of the incompressible liquid gives

$$
\dot V_\ell=Q_i-Q_o.
$$

Differentiating the geometric volume relation therefore gives

$$
\dot V_g=-Q_p-Q_i+Q_o. \tag{1}
$$

This is the new storage term. The gas amount is fixed, but its instantaneous
volume is not. A known amount of retained air does not specify its pressure
without a reference state and a thermodynamic closure.

For the first approximation, assume a constant-n polytropic relation,

$$
p_gV_g^n=p_{g,\mathrm{ref}}V_{g,\mathrm{ref}}^n,
\qquad
V_g(p_c)=V_{g,\mathrm{ref}}
\left(\frac{p_{g,\mathrm{ref}}}{p_{\mathrm{atm}}+p_c}\right)^{1/n}.
\tag{2}
$$

Polytropic gas closures are used in accumulator research, including Zhao et al.
[1, Eq. 7]. This is a provisional constitutive assumption here, not a calibrated
thermal model for our air–liquid chamber. A constant n does not capture thermal
hysteresis or establish the correct behaviour at every bpm. n = 1 is the
isothermal ideal-gas limit; an energy equation and heat transfer may be needed
if the fixed-exponent approximation is inadequate. Do not transfer the nitrogen
accumulator's chosen exponent or operating pressures to this rig.

Differentiate (2), with fixed n and fixed atmospheric pressure:

$$
\dot p_c=-\frac{n p_g}{V_g}\dot V_g,
\qquad
C_g\equiv-\frac{\partial V_g}{\partial p_c}
=\frac{V_g}{n(p_{\mathrm{atm}}+p_c)}>0. \tag{3}
$$

Substitute (1):

$$
\boxed{C_g(p_c)\dot p_c=Q_i-Q_o+A_p\dot x.} \tag{4}
$$

Every term has units m³/s. Positive volume input from the piston/inlet raises
pressure if it exceeds outlet flow. Gas expansion has the opposite effect.
In the electrical analogy, the pocket acts as a pressure-dependent capacitor;
the piston supplies a prescribed volume-flow input to that node.

This equation changes how the earlier waveforms are used: their prescribed
volume-rate curve becomes Qp, the piston command. Actual Qi and Qo are solved
from the coupled model; Qo is no longer imposed equal to Qp on every advance.
At fixed geometry, changing bpm does not silently resize the stroke to enforce
5 L/min.

## 3. What happens through reversal

With both valves closed, Qi = Qo = 0, so

$$
\dot p_c=\frac{A_p\dot x}{C_g(p_c)}. \tag{5}
$$

Advance compresses gas and raises pressure; retraction expands it and lowers
pressure. If the piston is stationary and both valves are closed, pressure stays
at its current value in this constant-n model. It is not reset to inlet or
arterial pressure. If either flow remains nonzero at reversal, pressure can
continue to change even when piston velocity is zero.

Between two positions while both valves remain closed,

$$
V_{g2}=V_{g1}-A_p(x_2-x_1),\qquad
p_{g2}=p_{g1}\left[\frac{V_{g1}}{V_{g1}-A_p(x_2-x_1)}\right]^n.
\tag{6}
$$

The denominator must be positive. With finite positive Cg and bounded flows and
motion, pressure remains continuous through reversal. Its time derivative, and
flow derivatives, can change with valve state. The model still needs numerical
verification; it does not guarantee a physiological waveform or remove every
high-frequency load omitted by lumped assumptions.

A useful closed-valve opening budget follows if arterial pressure is temporarily
constant, the outlet has zero cracking pressure and both valves remain closed
until opening. Starting with pc1 below pa,

$$
\Delta V_{p,\mathrm{open}}=
V_{g1}\left[1-\left(\frac{p_{\mathrm{atm}}+p_{c1}}
{p_{\mathrm{atm}}+p_a}\right)^{1/n}\right],\qquad
\Delta x_{\mathrm{open}}=\frac{\Delta V_{p,\mathrm{open}}}{A_p}.
\tag{7}
$$

For illustration only, reuse the earlier trial values: Vg1 = 10 mL at pc1 =
10 mmHg gauge, pa = 90 mmHg gauge, patm = 760 mmHg, n = 1.2 and Dp = 50 mm.
Equation (7) gives 0.7907 mL piston displacement, or 0.4027 mm advance, before
the outlet opening threshold. Gas volume then equals 9.2093 mL. These numbers
were calculated from (7) and substituted back into (6), recovering 90 mmHg gauge.
They are an analytical illustration, not a selected design or simulated beat.
This compression displacement is not automatically the net volume lost per beat:
gas can release stored volume later, and both valve histories matter.

In the coupled load, pa changes while the outlet is closed, so opening time is
found from pc(t) = pa(t), rather than by assuming a constant 90 mmHg threshold.

## 4. Derive valve opening and closure rules

Define the forward pressure differences

$$
\Delta p_i=p_i-p_c,\qquad \Delta p_o=p_c-p_a.
$$

For an open branch j with forward Qj > 0, the lumped momentum equation is

$$
I_j\dot Q_j=\Delta p_j-R_jQ_j-B_jQ_j|Q_j|. \tag{8}
$$

The passive one-way constraint is Qj >= 0. With Ij > 0 the entire ideal branch
law can be written on that domain as

$$
\dot Q_j=
\begin{cases}
[\Delta p_j-R_jQ_j-B_jQ_j|Q_j|]/I_j, & Q_j>0,\\
\max(\Delta p_j/I_j,0), & Q_j=0.
\end{cases} \tag{9}
$$

| Current state | Event or condition | Model action |
| --- | --- | --- |
| Closed, Qj = 0 | Forward pressure difference becomes positive | Open and start accelerating flow from zero |
| Open, Qj > 0 | Forward pressure difference becomes negative | Continue solving momentum; positive flow may decelerate |
| Open, Qj approaches zero from above | Forward gradient is non-positive | Close at zero flow and prevent negative flow |
| Closed, Qj = 0 | Forward pressure difference remains non-positive | Hold Qj = 0 |

This implements the pressure-opening/flow-closure principle discussed by Paeme
et al. [2]. Their paper also investigates progressive valve-area dynamics. Our
ideal branch is a baseline, not their full valve model or a measured hardware
response. We do not copy the paper's Heaviside expression by adding a dimensional
pressure directly to a dimensional flow; (9) states the conditions separately.

A pressure sign reversal alone is not sufficient reason to set an already
positive flow to zero. Doing so would discard the branch's fluid momentum.
Likewise, neither valve is forced to switch solely because the piston reverses.
Both-closed and, where the model permits it, simultaneous-forward-flow intervals
must be allowed rather than hard-coding two mutually exclusive piston phases.

Implement opening/closure as events or equivalent constrained integration.
Carry chamber/load pressure and all other continuous states through the event.
Only set the closing branch's flow to zero at its located zero-flow event.
Evaluate simultaneous events consistently; numerical event tolerances are not
physical cracking pressures or calibration parameters. Test their sensitivity.

Nonzero cracking pressure, leakage, hysteresis, finite opening area and real
closure timing are later refinements using selected-valve data. Commanded
closure while flow is nonzero requires additional transient treatment; it is
not represented by the passive zero-flow closure law above.

## 5. Couple the arterial load without prescribing outlet flow

Retain the three-element external load from Derivation 03:

$$
p_a=p_w+R_1Q_o,\qquad
C_w\dot p_w=Q_o-\frac{p_w-p_r}{R_2}. \tag{10}
$$

For the phases where both branch momentum equations are active, the combined
system is

$$
\begin{aligned}
\dot p_c&=\frac{Q_i-Q_o+A_p\dot x}{C_g(p_c)},\\
\dot Q_i&=\frac{p_i-p_c-R_iQ_i-B_iQ_i|Q_i|}{I_i},\\
\dot Q_o&=\frac{p_c-p_w-(R_o+R_1)Q_o-B_oQ_o|Q_o|}{I_o},\\
\dot p_w&=\frac{Q_o-(p_w-p_r)/R_2}{C_w}.
\end{aligned} \tag{11}
$$

For a closed branch, replace that branch's derivative by (9) and enforce Qj = 0
until its opening condition holds. Ro and R1 represent different physical
segments; their sum in (11) must not double-count an already fitted loss.

The continuous state vector is y = [pc, Qi, Qo, pw]. There are also discrete valve
states. These four hydraulic states are not four mechanical degrees of freedom.
Piston motion is prescribed at this stage. Gas volume, chamber liquid inventory,
arterial pressure and force follow from these states; volume integrals can be
added as accounting variables.

The earlier gas solver uses constant outlet pressure and has not been replaced
by (11). The prescribed-flow load solver has not been turned into a gas solver
by this derivation. Implementing and verifying their coupled form is the next
numerical task, after review of these assumptions.

Keep load coefficients fixed when comparing rates unless a deliberate change
is documented. The periodic mean relation remains

$$
\overline p_a=p_r+(R_1+R_2)\overline Q_o,
$$

but now actual mean flow is an output. Resistance previously chosen to yield
90 mmHg at an imposed 5 L/min will not necessarily yield 90 mmHg if net delivery
changes with gas storage and valve events.

## 6. Inventory, periodicity and force

The liquid inventory is

$$
V_\ell(t)=V_{c0}-A_px(t)-V_g[p_c(t)]. \tag{12}
$$

Track it explicitly. The model requires positive absolute gas pressure, positive
gas volume and enough liquid to keep the assumed liquid ports supplied. The
minimum wetted inventory depends on port geometry; arbitrary numerical guards
must not be presented as physical filling limits. Negative gauge pressure alone
does not establish cavitation; an applicable fluid-temperature pressure limit
is a separate physical check. Stop outside the declared validity domain rather
than extrapolating the single-pocket equations through loss of liquid inventory.

Over any interval, conservation gives

$$
\int(Q_o-Q_i)\,\mathrm dt=A_p\Delta x+\Delta V_g. \tag{13}
$$

For a periodic dedicated-chamber cycle, piston position and hydraulic states
return to their start values, so integrated inlet and outlet volumes match.
They are not required to equal the geometric swept volume. Actual net delivery
is the outlet-flow integral; mean flow follows from delivery and frequency.
For concept 1A, periodicity must instead be assessed over the full R+L routing
sequence, with gas and both external-load states carried through the duties.

Hydraulic plunger force follows from chamber pressure relative to the dry rear:

$$
F_h(t)=A_p[p_c(t)-p_b(t)],\qquad
F_{h,\max}=\max_{t\in\mathcal T}|F_h(t)|. \tag{14}
$$

Declare the interval Tcal: a complete periodic operating cycle or a specified
start-up/rate-change transient. The largest value can occur away from full
retraction or peak arterial pressure. It remains a hydraulic load, excluding
seal friction, moving-solid inertia and converter forces. Fluid inertia already
included in pc must not be added again.

## 7. What has been established, and what remains open

Established analytically in this step:

- A pressure-dependent gas compliance and a continuous chamber state equation.
- Valve-opening/closure conditions compatible with lumped fluid inertia.
- The four-state coupled chamber/load equations and inventory constraint.
- A closed-valve pressure/displacement relation and an illustrative opening budget.
- Dimensional/sign checks, the zero-motion/closed-valve limit and the integrated
  volume-balance identity. The small numerical example was evaluated and reversed.

Still required before interpreting a new complete-cycle force:

- Review the passive-check approximation against the eventual linked/active valve
  arrangement; keep actual gas reference state and n as declared inputs.
- Implement the coupled model, locate events accurately and check conservation,
  periodicity and solver/event sensitivity across the relevant operating cases.
- Reassess negative filling pressures and net delivery rather than assume that
  adding gas automatically cures the earlier discrepancies.
- Compare predicted ventricular and arterial waveforms at their corresponding
  locations with reference conditions identified. Gas compliance represents rig
  storage; it does not model active myocardial contraction.

No full pressure/flow waveform has been newly simulated here. Continuity of the
analytical pressure state enables a meaningful subsequent comparison; it does
not establish numerical convergence, hardware accuracy or clinical validity.

The full-liquid model remains a separate limit: Cg tends to zero as gas volume
vanishes, and (4) becomes an algebraic flow constraint. Do not implement that
limit by dividing by zero compliance. Finite liquid/wall compliance may need to
be retained in that branch; neither has been quantified in the present step.

## References and source scope

1. Zhao D, Ge W, Mo X, Liu B, Dong D. Design of A New Hydraulic Accumulator for
   Transient Large Flow Compensation. Energies. 2019;12(16):3104.
   [DOI: 10.3390/en12163104](https://doi.org/10.3390/en12163104).
   Publisher PDF pp. 6–7, Eqs. 7–10 inspected. Supports use of a polytropic gas
   closure in a hydraulic model. Its nitrogen charge, high pressures, cam mechanism
   and selected exponent are not adopted or treated as rig validation.
2. Paeme S, Moorhead KT, Chase JG, et al. Mathematical multi-scale model of the
   cardiovascular system including mitral valve dynamics. Application to ischemic
   mitral insufficiency. BioMedical Engineering OnLine. 2011;10:86.
   [DOI: 10.1186/1475-925X-10-86](https://doi.org/10.1186/1475-925X-10-86).
   Publisher full text, overall model and mitral-valve model sections inspected.
   Supports the pressure-opening/flow-closure distinction and identifies limits
   of instantaneous valve-area assumptions. No physiological parameter values or
   validation claims are transferred to this pump.

Equations (1)–(14) are our re-derivation for the declared pump boundary and
assumptions. They are not a verbatim transfer of either paper's full system.
