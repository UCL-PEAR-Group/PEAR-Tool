# Design 1: Piston Pump — living model

**Current design direction: enforced valve states in both architectures.**
[Valve control and routing](research/VALVE_CONTROL_AND_ROUTING.md) records the
user-confirmed port assignments and separates commands, effective opening and
hydraulic flow.

[Derivation 04: retained-air storage and valve events](research/DERIVATION_04_RETAINED_AIR_AND_VALVE_EVENTS.md)
derives reusable chamber/gas/load balances. Its passive switch law is superseded
for the design and retained as a comparator. The enforced command and closure
transient law remain to be derived; the two numerical implementations below
remain separate and unchanged.
No new cycle waveform, completed MATLAB port or force rating is claimed. The
interactive application follows completion and numerical verification of the
necessary coupled derivation.

[Derivation 03: pressure histories and the heart reference](research/DERIVATION_03_PRESSURE_AND_HEART_REFERENCE.md)
adds a separate, prescribed-flow arterial-load study in Python and the spreadsheet.
It compares systemic and pulmonary load pressures with published functional human
arterial waveforms, preserving their original 6.6 L/min condition. The pump trial
remains at 5 L/min and 75/min. Chamber pressure and force are conditional phase
calculations; pressure transitions remain unresolved. The systemic phase-only
peak is 32.6 N at the illustrative 50 mm bore; the pulmonary 15.5 N result fails
the previous passive closed-valve test. That test does not establish an
inconsistency for enforced closure. Neither result is a force rating.

The exploratory gas solver documented in sections 1–7 below uses passive checks
and is unchanged. It is not an enforced-valve simulation. Its
imposed pressure boundaries and archived force values must not be mixed with the
new periodic-load inputs or interpreted as a verification of the new cycle.

[Derivation 02: waveform joining](research/DERIVATION_02_WAVEFORM_JOINING.md)
now adds selectable, volume-normalised kinematic commands and endpoint smoothing.
The formula workbook evaluates those commands independently of its earlier local
pressure example. A 5% endpoint-window trial preserves volume and removes
acceleration jumps, but raises the finite peak acceleration by about 77–78%.
No smoothing width, actuator trajectory or new maximum force has been selected.
These commands have not been connected to the exploratory hydraulic solver below.

The staged, literature-led derivation now starts with
[Derivation 01: full-liquid chamber and pressure force](research/DERIVATION_01_FULL_LIQUID.md).
It establishes sign conventions, phase-specific pressure/force expressions and
limits of the incompressible approximation. It does not alter the exploratory
solver documented below or constitute a new numerical result.

This document is the maintained explanation of the model. The executable
calculation entry point is [Pump_Model.ipynb](python/Pump_Model.ipynb), with
[run_model.py](python/run_model.py) for command-line use. See the complete
[variable register](VARIABLES.md) for roles, types, units and implementation status.
The first numerical results are preserved in the [reference archive](archive/).
Update this document and [DECISIONS.md](DECISIONS.md) when a modelling decision
changes; retain previous numerical snapshots so changes can be traced.

The [goal and concept comparison](GOAL_AND_CONCEPT_MATRIX.md) and
[operating-case matrix](OPERATING_MATRIX.md) now distinguish the proposed
shared chamber (1A) and two dedicated chambers (1B). They do not extend the
current hydraulic solver to either complete architecture.

## 1. Purpose and current status

Estimate geometric displacement, delivered liquid volume, pressure history
and peak hydraulic force for a plunger piston with no wetted rod. The actuator
and rotary-to-linear converter are outside this stage. The exploratory dynamic
model below represents one ventricular pump chamber and imposed pressure loads.
The separate Derivation 03 implements a periodic Windkessel load driven by
prescribed flow; neither implementation solves both recirculating loops.

The archived Python sweep contains 118 attempted dynamic cases: 117 periodic
solutions and one stopped by a low-pressure guard. Python is the active implementation. The earlier MATLAB translation is
superseded and remains unexecuted. The Python model is not calibrated or
independently validated against a physical pump.

## 2. Inputs, assumptions and units

| Quantity | Current value or range | Status / provenance |
| --- | --- | --- |
| Nominal mean circuit flow | 5 L/min | User-prescribed |
| Nominal per-circuit pulse frequency h | 75 beats/min | User-prescribed; overrides the earlier PDS nominal rate; distinct from physical chamber frequency f in concept 1A |
| Archived physical chamber frequency f | 40–180 cycles/min | Previous one-chamber sweep; PDS per-circuit range is h = 40–180 bpm, implying f = 2h for 1A |
| Mean-flow range | 2–7 L/min | PDS; compatible combinations remain to be chosen |
| Geometric swept volume | 66.6667 mL | Ideal 5 L/min ÷ 75/min reference; not actual delivered volume |
| Face diameter / travel | 50 mm / 33.95 mm | Illustrative; both remain design variables |
| Wetted rod area | None | User's flat-face plunger concept |
| Inlet / outlet boundaries | 10 / 90 mmHg gauge, constant | PDS reference levels; constant-boundary treatment is an assumption |
| Outlet sensitivities | 120 and 200 mmHg gauge, constant | Additional loads, not reproduced physiological waveforms |
| Pressure behind piston | Atmospheric | Assumption |
| Gas reference volume | 1, 10 or 20 mL; baseline 10 mL | Deliberately retained sealed air; values assumed |
| Gas reference pressure | 10 mmHg gauge | Assumption; absolute pressure used in gas law |
| Atmospheric pressure | 760 mmHg | Assumption |
| Polytropic exponent | 1.2; sensitivities 1 and 1.4 | Assumption; gas heat transfer not solved |
| Inlet and outlet valve bores | Both 8, 12, 16 or 20 mm | Assumed effective clear bores; varied together |
| Discharge coefficient | 0.7; sensitivities 0.6 and 0.8 | Uncalibrated |
| Fluid density | 1000 kg/m³ | Water-like assumption; not BMF characterisation |
| Each hydraulic leg | 20 mm bore, 0.2 m effective inertial length, K = 1 | Assumed lumped line model |
| Advance fraction | 0.4; sensitivities 0.3 and 0.5 | Smooth prescribed motion; no mechanism selected |
| Minimum chamber volume | 40 mL | Assumed residual volume; includes gas plus residual liquid |
| Leakage | Zero | Initial simplification |

The current scripts contain no viscosity-dependent BMF loss calibration. The
coefficient K is a lumped quadratic loss assumption, not a derived pipe-friction
factor. A selected cylinder's total length must also accommodate the piston,
residual volume, ports and end clearance; travel is not automatically total
cylinder length minus plunger thickness.

## 3. Displacement, flow and frequency

Define A as piston-face area, D as face diameter and S as piston travel.

- A = π D² / 4.
- Geometric swept volume Vₛ = A S.
- With D and S in mm, Vₛ [mL] = π D² S / 4000.
- For one dedicated chamber, with f in delivery cycles/min and Vnet in mL/cycle, Qmean [L/min] = f Vnet / 1000.
- Therefore Vnet,required [mL/beat] = 1000 Qtarget / f.

The last two relations are cycle-volume accounting, not empirical pump laws.
For ideal fully filled liquid displacement with one delivery per beat and no
diversion, Vnet = Vₛ. With retained gas and valve transients, Vnet is obtained
by integrating the outlet flow. A delivery ratio Vnet/Vₛ is an output of the
hydraulic model; it is not an independently adjustable controller input.

For our 66.6667 mL ideal reference:

| Frequency | Ideal full-stroke flow | Net volume needed for 5 L/min | Ideal diverted fraction to retain 5 L/min |
| --- | --- | --- | --- |
| 40/min | 2.667 L/min | 125.00 mL/beat | Not attainable by diversion of this stroke |
| 75/min | 5.000 L/min | 66.67 mL/beat | 0% |
| 120/min | 8.000 L/min | 41.67 mL/beat | 37.5% |
| 180/min | 12.000 L/min | 27.78 mL/beat | 58.33% |

At 180/min, ideal diversion would return 38.89 mL per beat, or 7 L/min,
while 5 L/min enters the test circuit. These are volume budgets, not an
implemented valve design. The actual baseline simulation at 75/min delivers
about 4.945 L/min because its net delivery differs from the ideal swept volume.

**A fixed stroke supports a prescribed compatible flow/bpm pair. It does not
provide independent control of arbitrary flow and bpm pairs by itself.**

For two ventricular chambers in series, each chamber must support the circuit
flow; do not sum left and right flow to claim doubled cardiac output. In a
single time-multiplexed chamber, distinguish mechanical delivery frequency
from deliveries per minute to each circuit before applying these equations.

## 4. How independent control could be obtained

| Alternative | Fixed mechanical travel retained? | What changes | Consequences to assess |
| --- | --- | --- | --- |
| Controlled bypass or diversion to a reservoir | Yes | Fraction of expelled volume reaching the circuit | Additional valves/path and flow measurement; timing and pressure load must be modelled |
| Controlled spill through an actively operated inlet during early advance | Yes | Effective delivery portion of each stroke | Requires active valve timing; passive checks alone cannot command this behaviour |
| Variable effective piston travel | No | Geometric displacement per beat | Direct volume control, but conflicts with the current fixed-travel assumption |
| Change bore or exchange cylinder | Fixed within each selected configuration | Displacement per beat | Discrete hardware choices, not continuous run-time control |
| Skip delivery events | Travel may remain fixed | Number of delivered pulses | Changes actual delivery frequency; does not preserve a pulse every requested beat |

Changing only the speed profile within each beat changes instantaneous flow,
pressure and filling time. With ideal full filling and the same stroke, it does
not change the integrated delivered volume. Throttling a fully filled,
incompressible, leak-free displacement pump primarily changes pressure demand;
it does not by itself create independent mean-flow control. Incomplete filling
can change actual delivery, but deliberately relying on starvation introduces
load-dependent behaviour rather than a prescribed volume command.

A sealed air pocket provides compliance. Its volume and pressure change during
the cycle and must return to the same state in periodic operation. It can alter
the net delivery by delaying valve opening and expanding during return, but it
cannot accumulate excess liquid indefinitely or serve as an independently
commanded flow setting merely because its initial amount is known. Similarly,
a Windkessel stores and releases volume within a cycle; at periodic steady
state its net stored volume per cycle is zero. A separate control degree of
freedom is still needed for independent flow/bpm selection.

Keep both strategies open: (A) fixed stroke with flow allowed to rise with bpm,
and (B) prescribed circuit flow with an added means of varying net delivery.
No bypass or spill strategy has been selected or added to the hydraulic solver.

## 5. Current hydraulic equations

Use SI units for this section: p in Pa, volume in m³, flow in m³/s, time in s,
area in m². The scripts convert to mmHg/mL/s internally using
1 mmHg = 133.322387415 Pa and 1 mL = 10⁻⁶ m³.

Let u(t) = A x(t) be piston displacement volume, positive on advance. Let pc
be chamber pressure, pi upstream pressure, po downstream pressure and pb rear
pressure. Qi and Qo are positive forward inlet/outlet flows. With a rigid
chamber, incompressible liquid and a sealed polytropic gas pocket:

- Gas law: Vg = Vg0 (pg0,abs / pc,abs)^(1/n).
- Gas compliance: Cg = Vg / (n pc,abs), in m³/Pa.
- Chamber balance: Cg dpc/dt = Qi − Qo + du/dt.
- Open inlet: Ii dQi/dt = pi − pc − Bi Qi |Qi|.
- Open outlet: Io dQo/dt = pc − po − Bo Qo |Qo|.
- Each leg: I = ρ ℓ / At, in Pa·s²/m³.
- Each leg: B = (ρ/2) [1/(Cd Av)² + K/At²], in Pa·s²/m⁶.
- Valve area Av = π dv²/4; line area At = π dt²/4.
- Liquid inventory: Vl = Vmin + Vₛ − u − Vg.

Ideal check valves open when their forward pressure difference becomes positive
and close when their forward flow reaches zero. Fluid inertia can temporarily
maintain forward flow after the pressure gradient reverses. The ideal model can
also permit brief simultaneous forward inlet/outlet flow and net-delivery
ratios slightly above one. This behaviour requires physical valve validation;
the ratio should not be interpreted as a calibrated conventional efficiency.

Let h(z) = 10z³ − 15z⁴ + 6z⁵, T = 60/f seconds and γ be the advance fraction.
During advance, u = Vₛ h[t/(γT)]. During return,
u = Vₛ {1 − h[(t−γT)/((1−γ)T)]}. Velocity and acceleration are zero at the
phase boundaries. Equal travel is used on advance and return; their durations
can differ. Unequal net travel over a repeated closed cycle would cause drift.

The gas-free reference is a separate imposed-full-fill calculation with flow
equal to piston displacement rate. Its pressure is calculated from the same
loss and inertance terms and screened for impossible low-pressure conditions.
It is not a zero-gas ODE run, because Cg = 0 makes that formulation singular.

## 6. Force and what the reported maximum means

Hydraulic pressure load: Fp(t) = A [pc(t) − pb].
Reported maximum: max |Fp(t)| over the final periodic cycle.

The sign denotes the required balancing force along the piston advance axis.
With an atmospheric rear, gauge chamber pressure can be used directly. This
is not A(po−pi): inlet pressure is not the pressure acting on the rear face.
Chamber pressure includes valve losses and fluid acceleration, so it can be
much greater than the imposed outlet pressure.

Seal friction, moving-solid inertia, converter forces, start/stop transients
and blocked-path cases are excluded. There is no universal maximum force until
the admissible pressure boundaries, motion profiles and flow paths are defined.

| Valve bores | Peak hydraulic force at 75/min | At 180/min |
| --- | --- | --- |
| 8 mm | 145 N | 724 N |
| 12 mm | 50 N | 175 N |
| 16 mm | 41 N | 94 N |
| 20 mm | 41 N | 88 N |

These rows use the baseline inputs in section 2. The largest sensitivity case
was approximately 1275 N (180/min, 8 mm valves, γ = 0.3), implying about
4870 mmHg gauge chamber pressure. This is an extreme demanded load under
assumed perfect motion tracking, not an endorsed operating condition.

![Hydraulic parameter trends](archive/pump_hydraulic_sweep/Hydraulic_force_trends.png)

![Force waveforms and gas sensitivity](archive/pump_hydraulic_sweep/Hydraulic_force_waveforms.png)

## 7. Verification and model limits

The executed Python reference used event-driven SciPy Radau integration,
relative tolerance 2×10⁻⁷ and maximum step T/120. Three cases were refined with
relative tolerance 2×10⁻⁹, maximum step T/360 and denser peak sampling. Checked
force changes were below 0.001%. Across completed cases the largest volume
balance residual was 3.14×10⁻⁶ mL and periodic inlet/outlet volume mismatch was
4.77×10⁻⁷ mL. Full records are in the archive.

The low-pressure guard is 50 mmHg absolute (6.67 kPa), an exploratory validity
floor, not a measured cavitation threshold. Passing this check does not rule
out local valve cavitation. A separate liquid-inventory guard is 0.1 mL.
One case stopped: 180/min, 8 mm valves, 1 mL reference air. No periodic force
result is fabricated for it.

The active Python entry point `python/run_model.py check` has been executed.
It reproduces three archived cases within 1e-6 relative error in peak force,
mean flow and minimum pressure, and checks conservation, endpoint kinematics
and the expected low-pressure guard. The hydraulic equations and default
parameters are unchanged. The optional notebook code cells also ran in an in-process IPython shell;
Jupyter frontend rendering remains unchecked;
see `python/verification_status.json`. No MATLAB execution is required for
the active workflow. The old port remains an unexecuted historical alternative.

Constant reservoirs exclude reservoir depletion and recirculation shortages.
Actual Windkessel pressure histories, finite valve motion, compressibility of
the liquid, wall elasticity, gas heat transfer/dissolution and BMF rheology
remain outside this implementation. Numerical verification is distinct from
calibration and from independent validation; none establishes clinical
prediction accuracy.

## 8. Evidence and archived derivations

- [Hydraulic sweep report](archive/pump_hydraulic_sweep/Hydraulic_force_sweep.pdf)
  and [LaTeX source](archive/pump_hydraulic_sweep/Hydraulic_force_sweep.tex).
- [Earlier coupled-model derivation](archive/pump_coupled_model/Pump_coupled_model.pdf)
  and [LaTeX source](archive/pump_coupled_model/Pump_coupled_model.tex).
- [Initial displacement/geometry plots](archive/pump_tradeoffs/Pump_parameter_tradeoffs.pdf).
- Broomé et al. (2013), cardiovascular nonlinear valve-loss/inertance model:
  https://doi.org/10.1186/1475-925X-12-69. Model-structure precedent; its
  parameters and validation are not inherited by this pump.
- Iannetti et al. (2015), reciprocating-pump cavitation/compressibility study:
  https://doi.org/10.17265/2332-8215/2015.01.005. Explains regimes excluded here;
  it does not validate the present lumped model.
- The earlier MATLAB files cite MathWorks format documentation; that port is
  superseded. The current notebook and scripts use the executed Python solver.

## 9. Architecture accounting added on 21 November 2026

For a per-circuit pulse rate h, concept 1A needs two sequential physical chamber
cycles per heart period: f = 2h. Concept 1B needs f_R = f_L = h in two separate
chambers. Thus a 180 bpm per-circuit target requires 360 cycles/min for 1A,
beyond the existing 180 cycles/min sweep. Even at lower rates, alternating
pressure boundaries and gas-state carry-over remain unimplemented.

For both concepts, net volume per circuit pulse is 1000 Qtarget/h. At 5 L/min
and 75 bpm this is 66.67 mL; at 180 bpm it is 27.78 mL. With the illustrative
66.67 mL stroke, keeping 5 L/min at 180 bpm needs an ideal 58.33% reduction
in net delivery. It is not achieved just by switching between R and L.

The new matrix is accounting only. Periodicity for 1A must be checked over the
complete R+L sequence, retaining chamber/gas state across switches. For both
concepts, finite reservoirs and distinct pulmonary/systemic loads are needed
to assess stable recirculation. Current constant-boundary tests cannot do so.

The current PDS explicitly lists pulmonary mean arterial cases 15/25/35 mmHg.
Right-atrial preload, pulmonary peak and complete arterial waveforms remain
open. Systemic constant-load sensitivities must not be reused as pulmonary
requirements or treated as reproduced physiological waveforms.

## 10. Next staged decisions

First complete the commanded valve schedule, routing transition and effective
opening law in [the valve decision note](research/VALVE_CONTROL_AND_ROUTING.md).
The following wider parameter decisions remain open.

1. Review the operating-case matrix for both architectures, then the variable
   register, and agree which remaining inputs become measured
   quantities, selected component properties or prescribed operating conditions.
2. Agree compatible flow/frequency combinations and whether net-delivery control
   must retain fixed mechanical travel.
3. Compare the additional flow-control paths before selecting one.
4. Replace assumed valve/line data and boundary pressures with selected-component
   data or measurements; then repeat the force sweep.
5. Choose geometry using feasible operating cases before sizing the converter.
