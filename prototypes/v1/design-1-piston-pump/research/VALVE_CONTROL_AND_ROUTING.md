# Enforced valve control and circuit routing

22 November 2026. User-confirmed design direction; the command-to-opening law,
transition timing and hardware are still to be derived and selected. No new
simulation, waveform, MATLAB execution or maximum-force result is claimed.

## Confirmed assignments

Both concepts use enforced valve states coordinated with piston motion. Pressure
may also enter the command rule; it is not excluded by enforcement. A purely
passive valve law is not a complete description of the intended coordination.
The labels below describe cardiac functions to emulate and their flow paths;
they do not select a valve mechanism, physical valve count or actuator.

| Concept and duty | Inlet path: into the ventricular chamber | Outlet path: out towards the circulation |
| --- | --- | --- |
| 1A shared chamber, right duty | Right-atrial reservoir to shared chamber: tricuspid function | Shared chamber to pulmonary circuit: pulmonic function |
| 1A shared chamber, left duty | Pulmonary-return/left-atrial reservoir to shared chamber: mitral function | Shared chamber to systemic/aortic circuit: aortic function |
| 1B dedicated right chamber | Right-atrial reservoir to right chamber: tricuspid | Right chamber to pulmonary circuit: pulmonic |
| 1B dedicated left chamber | Left-atrial reservoir to left chamber: mitral | Left chamber to systemic/aortic circuit: aortic |

For 1A, the physical inlet/outlet paths acquire their ventricular roles from the
routing state. A shared outlet is not simultaneously pulmonic and aortic.
Each duty includes filling and delivery; a route change is not a replacement for
either phase. Connections and the transition between duties remain to be specified.

For 1B, retain the earlier proposed inlet-pair and outlet-pair command grouping.
Linked commands do not imply identical flows or pressure drops in the two sides.
Exact inter-chamber timing and any deliberately introduced delay remain open.

## Change to the analytical model

Use prescribed or controller-generated commands to determine requested valve
states. These commands may depend on piston phase and pressure thresholds:

\[
u_i(t),u_o(t)\in\{0,1\},\qquad
0=\text{closed command},\quad 1=\text{open command}.
\]

For 1A add the selected duty

\[
\sigma(t)\in\{R,L\}.
\]

The physical transition between these routing states needs its own connection
sequence. A binary duty label does not yet resolve selector motion or temporary
isolation. Chamber pressure, gas volume and liquid inventory carry across duty
changes; they must not be reset to the next reservoir pressure. Both external
circuits also continue evolving while the chamber serves the other duty.

Distinguish command from actual opening: let a_j(t) be the effective opening
fraction, dimensionless, for j = i or o. Its relation to u_j(t), including delay,
opening duration and closure duration, remains a model decision. No actuator
response or pressure-independent ability to hold position has been demonstrated.

The chamber storage equation from Derivation 04 is unchanged:

\[
C_g\frac{dp_c}{dt}=Q_i-Q_o+A_p\dot x,
\qquad
C_g=\frac{V_g}{n(p_{\mathrm{atm}}+p_c)}.
\]

Here x is piston advance in m, A_p its wetted area in m², Q_i and Q_o signed
flows in m³/s, p_c gauge chamber pressure in Pa, p_atm atmospheric pressure in Pa,
V_g gas volume in m³, n the dimensionless polytropic exponent and C_g compliance
in m³/Pa. Fixed gas mass, incompressible liquid, rigid walls and negligible leakage
remain the stated assumptions. Positive Q_i enters and positive Q_o leaves the
chamber; an assigned direction does not by itself prohibit negative flow.

An open-path momentum model can retain the structure

\[
\Delta p_j=I_j\dot Q_j+R_j(a_j)Q_j+B_j(a_j)Q_j|Q_j|,
\qquad a_j>0,
\]

with inlet pressure difference p_i - p_c and outlet pressure difference p_c - p_a.
The pressures p_i and p_a belong to the connected upstream and downstream nodes.
I_j is lumped fluid inertance (Pa s²/m³), R_j linear resistance (Pa s/m³) and B_j
quadratic loss coefficient (Pa s²/m⁶). Treating I_j as constant is a provisional
branch approximation. Actual opening-dependent coefficients remain unselected.
The existing full-open loss coefficients do not describe partial opening.

Unless separately specified hardware provides one-way action, an open enforced
path can carry reverse flow. Do not impose Q_j >= 0 solely from the words inlet
or outlet. When fully closed, the negligible-leakage boundary is Q_j = 0, but
instantaneously resetting a nonzero inertial flow to zero is not a resolved
closure transient. The finite transition model and any additional local storage
must be assessed before calculating its pressure and force peaks.

Do not assume u_o = 1 - u_i. Both-closed intervals, overlap and their timings are
unselected. A stationary piston with both valves closed does not equalise
pressure in the current constant-exponent gas model: all three terms on the
right-hand side of the storage balance are zero.

## Piston phase and pressure may jointly determine commands

The user's subsequent clarification is that the cardiac names express the
behaviour to be emulated. Piston position participates in valve coordination,
and pressure may also participate. Enforced state does not imply a pressure-blind
schedule. A purely passive model is a comparator; a controller using measured
pressure is compatible with the intended enforced valves.

A general control-law placeholder is

\[
u_j(t)=\mathcal K_j\!\left(\phi(t),x(t),\dot x(t),
\Delta p_j(t),q(t),\sigma(t)\right),\qquad j\in\{i,o\}.
\]

Here phi is cycle phase (dimensionless, 0 to 1), x piston advance (m), x-dot
piston velocity (m/s), delta-p the forward pressure difference (Pa), q the
remembered discrete cycle/control state, and sigma the circuit assignment.
K_j is a rule returning the dimensionless open/closed command. q is not flow Q.
This is a declaration of possible dependencies, not a completed control law or
an instruction to use every input. Flow feedback could later be included if the
closure strategy requires it. A physical controller would use measured or
estimated states, with sensor/actuator dynamics accounted for when specified.

Position alone is ambiguous: an intermediate position occurs during both
advance and return. Use the commanded cycle phase or direction plus state
memory, including at reversal where velocity is zero. Piston motion changes
chamber volume and pressure; valve commands change the flow paths; the resulting
flows feed back into chamber pressure through the storage equation below.

Both of these implementations remain available:

| Candidate | Role of piston phase/position | Role of pressure |
| --- | --- | --- |
| Phase-scheduled commands | Sets the valve sequence and timing | Calculated hydraulic response, loading and performance measurement |
| Phase-scheduled commands with pressure conditions | Defines the permitted part of the cycle | May trigger, delay or otherwise modify a permitted transition |

For discussion, a four-phase sequence can express the intended cardiac roles:

| Proposed phase | Piston behaviour | Inlet target state | Outlet target state |
| --- | --- | --- | --- |
| Filling | Return while chamber volume increases | Open | Closed |
| Pressure build-up | Early advance compresses retained gas | Closed | Closed |
| Ejection | Advance with delivery to the assigned artery | Closed | Open |
| Pressure release | Early return expands retained gas | Closed | Closed |

This table is a proposed sequence, not a selected timing law. Finite closure may
begin before the nominal boundary. Actual opening durations and piston advance
or return durations need not coincide. Both-closed piston motion keeps liquid
inventory constant under the stated assumptions, but changes total chamber and
gas volume; it is not literally constant chamber volume. If a valve is closed
while the piston is stationary, the existing ideal gas model does not produce
pressure relaxation by itself.

An example opening condition for review is: allow outlet opening in the ejection
window only when chamber pressure exceeds its connected arterial pressure by a
chosen margin. An inlet condition would use reservoir minus chamber pressure.
No thresholds, hysteresis, waiting periods or closure rule have been selected.
If a pressure condition is not reached before its phase window ends, the model
must report that outcome rather than silently assuming successful delivery.
For fixed prescribed motion, adding a waiting dwell would change the waveform
and must be explicitly chosen; valve gating alone does not stop the piston.

For two chambers with strictly linked valve commands, separate right/left
pressure conditions require an explicit group rule. Independent threshold
crossings cannot be assumed to give simultaneous switching. For the shared
chamber, pressure comparisons use the currently assigned circuit and the
selector transition remains a separate event.

Physiological reference: Paeme et al. model ventricular driving together with
pressure/flow-dependent valves, and extend the mitral model to finite aperture
dynamics driven by transvalvular pressure. This supports retaining pressure and
valve dynamics in the comparison; it does not establish a piston-position
controller or validate the proposed four-phase rig sequence. Publisher full
text, Methods (CVS model; Mitral valve model; Dynamics of the mitral valve),
consulted 22 November 2026. DOI:
[10.1186/1475-925X-10-86](https://doi.org/10.1186/1475-925X-10-86).

## Consequences for pressure, flow and force

The waveform prescribes piston displacement, not independently the actual inlet
and outlet flows. Those flows and chamber pressure follow from storage, valve
opening, connected reservoir pressures and external loads. For a prescribed
motion, the hydraulic force remains

\[
F_h(t)=A_p[p_c(t)-p_b(t)],
\]

where p_b is dry rear-face gauge pressure in Pa and F_h is in N. A full-cycle
hydraulic maximum requires the commanded transition dynamics to be resolved.
Seal friction, moving-solid inertia, valve-actuator loads and converter force
transmission remain outside this hydraulic plunger-force expression.

Enforced timing adds a potential means of changing net delivery, for example
by allowing a modelled spill path during part of advance. It does not establish
independent control of mean flow and bpm without specifying that sequence and
integrating the resulting net delivered volume.

## Scope of earlier work

- Derivation 04's chamber conservation, gas compliance and external-load balance
  remain reusable. Its passive switch rules and constrained-flow state equations
  are retained as a comparator, superseded for the commanded design.
- The existing Python gas solver still uses passive checks. Its output is not a
  prediction of the newly confirmed enforced-valve system.
- Derivation 03 and the spreadsheet's closed-valve pressure-conflict diagnostics
  test a zero-cracking passive-valve assumption. A forward pressure difference
  across an enforced closed valve is not, on its own, a switching inconsistency.
  It contributes to a load that the selected valve must withstand.
- Earlier numerical data and formulas are preserved. Unresolved pressure joins
  still prevent using the conditional phase-force extrema as full-cycle ratings.

## Next collaborative decisions

1. Define the desired phase sequence and how piston phase/position participates.
   Decide whether pressure modifies transitions; if so, specify thresholds,
   hysteresis and behaviour when a condition is not reached within its window.
   Keep both-closed intervals, any overlap and the duty selector explicit.
2. For 1A, define the routing transition and carry-over states. For 1B, define
   simultaneous paired commands or the intended inter-chamber delay.
3. Select the initial effective-opening law, including transition duration, and
   state whether any separate one-way behaviour is present. This refines the
   confirmed enforced-state choice; it does not reopen passive versus enforced.
4. Complete the coupled derivation before implementing the next numerical case.

This note records the user's topology/control intent and consequences derived
from the existing conservation and momentum equations. The cited physiological
model supplies reference context; no experimental result, selected control law
or numerical timing values are added.
