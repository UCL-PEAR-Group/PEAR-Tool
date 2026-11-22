# Adjustable ventricular duties and ideal-valve baseline

22 November 2026. User-confirmed scope: allow unequal right/left duty durations,
retain equal allocation initially, and idealise valve transition times until a
valve is selected. Detailed closure transients are deferred. This update changes
the architecture-budget generator and model specification, not the hydraulic
solver or its existing numerical results.

## Shared-chamber timing is an allocation, not a physiological half-cycle

Let h be the required pulse rate at each arterial outlet, in min^-1, and TH the
period between successive pulses at that same outlet. Define the adjustable
right-duty fraction lambda_R:

$$
T_H=\frac{60}{h},\qquad
0<\lambda_R<1,\qquad
T_R=\lambda_R T_H,\qquad
T_L=(1-\lambda_R)T_H. \tag{1}
$$

TR and TL are whole fill/eject duty budgets, in seconds. They include any time
reserved inside each slot for routing or dwell. Default lambda_R = 0.5 is the
user-approved starting assumption, not a fixed requirement.

| h | lambda_R | Right duty TR | Left duty TL | Status |
| --- | --- | --- | --- | --- |
| 75/min | 0.50 | 0.400 s | 0.400 s | Current default |
| 75/min | 0.60 | 0.480 s | 0.320 s | Illustrative unequal allocation |
| 75/min | 0.40 | 0.320 s | 0.480 s | Illustrative unequal allocation |

All three schedules deliver one right and one left event per TH. Their mean
physical delivery-event count is still 2h = 150/min, but unequal duty durations
cannot be represented by a single uniform T = 60/(2h). TH/2 is only the mean
available time per event. It does not specify either unequal slot.

For a shared piston with unchanged stroke S, let s = (t-t0) mod TH. A general
piecewise motion is

$$
x(t)=\begin{cases}
S X_R(s/T_R),&0\le s<T_R,\\
S X_L((s-T_R)/T_L),&T_R\le s<T_H.
\end{cases} \tag{2}
$$

Each dimensionless X_d is a complete advance/return waveform, returning the piston
to its starting position. Compatible endpoint derivatives are needed at the
joins. In duty d, speed scales as S/T_d and acceleration as S/T_d² for unchanged
normalised shape. The shorter duty therefore demands faster displacement;
actual pressure, filling and net delivery must still be solved.

Within each duty, retain a separate advance fraction gamma_d:

$$
t_{\mathrm{advance},d}=\gamma_d T_d,\qquad
t_{\mathrm{return},d}=(1-\gamma_d)T_d,\qquad d\in\{R,L\}. \tag{3}
$$

Default gamma_R = gamma_L = 0.4 continues the existing illustrative motion split.
Lambda_R allocates time between ventricular duties; gamma_d allocates advance
versus return within a duty. Neither is automatically an actual blood-ejection
ratio. With lambda_R = 0.6 at 75/min, the corresponding advance budgets at gamma
0.4 would be 0.192 s right and 0.128 s left.

At the unchanged target 5 L/min and 75 pulses/min per outlet, each circuit still
requires 66.667 mL net delivery per pulse. Changing lambda_R does not change that
requirement or guarantee its achievement. It redistributes the available time.

## Two dedicated chambers and the heart reference

For 1B, each chamber has the whole TH and their cycles may overlap. Independent
advance/filling allocations and any relative phase offset are separate parameters,
subject to the earlier linked-valve command constraints. Do not impose TR+TL=TH
on the two dedicated chambers.

Physiological ventricular ejection durations need not be identical. Leighton et
al. [1] compared simultaneous right/left systolic intervals in 27 normal subjects
and reported different responses to heart rate and respiration. Hirschfeld et
al. [2] reported longer right than left ejection in their 11 normal children,
with a different relationship in transposition. These observations support
adjustable timing, not a universal ratio for our rig. The ventricles' events
occupy overlapping portions of a heartbeat; sequential duty partitioning is a
constraint of our shared-piston architecture, not a literal cardiac timing map.

Access limitation: accessible publisher/indexed abstracts were inspected; full
texts were not retrieved. No patient timings or normal-population ratio are used
to calibrate lambda_R. The 50:50 and 60:40 examples above are design assumptions.

## Ideal valve transition model for this stage

Keep the command logic from Derivation 05, with pressure-conditioned opening
optional, but replace the proposed finite aperture ramp by ideal transitions:

$$
a_j(t)=u_j(t)\in\{0,1\},\qquad
\tau_{\mathrm{open},j}=\tau_{\mathrm{close},j}=0
\quad\text{in the ideal model}. \tag{4}
$$

This is a separate ideal-switch case, not substitution of tau = 0 into the
quintic ramp's division by tau. It means no transition delay and negligible
closed-valve leakage. It does not imply zero full-open hydraulic loss, guarantee
one-way action, or remove fluid inertia from an existing equation. Hardware
transition data and the finite-area model remain a later refinement.

A finite pressure build-up or release interval can still occur with ideal valves:
pressure eligibility depends on retained-air compression/expansion and circuit
loading. Zero transition time does not require an immediate command at piston
reversal, and it does not make inlet and outlet commands complementary.

## What flow during closure changes

For a real valve taking tau_close to shut, signed transition volume is

$$
V_{\mathrm{transition}}=
\int_{t_c}^{t_c+\tau_{\mathrm{close}}}Q(t)\,dt. \tag{5}
$$

It contributes to the complete net delivery integral; it must not be added twice.
A positive value indicates forward delivery during closure; a negative value
indicates reverse volume. The difference from an instantaneous-switch model
also depends on how the pressure/flow solution changes elsewhere in the cycle.

| Quantity | Relevance of finite closure | Treatment now |
| --- | --- | --- |
| Net delivered volume and mean flow | Forward tail or reverse volume changes the signed cycle integral | No resolved finite transition interval in the ideal baseline |
| Pressure waveform near switching | Decelerating fluid and a narrowing path change pressure differences | Detailed switching transient deferred |
| Hydraulic plunger-force peak | Chamber pressure acts over piston face area | Report only loads supported by the stated pressure model; no surge-inclusive rating |
| Valve actuation, wear and local flow field | Depend on valve mechanism and actual aperture motion | Component-specific work after selection |

The open-branch momentum balance contains I dQ/dt. If a nonzero Q is forced to
zero in zero time with finite fluid inertance, an ordinary finite transient
pressure peak is not defined by that idealisation. It is therefore incorrect to
reset Q numerically and label the resulting sampled maximum a verified physical
closure load. This update neither removes fluid inertia silently nor supplies
an impulse/surge model. Numerical switching treatment must be declared when the
ideal coupled model is implemented; a quasi-steady reduced comparison would be
a separate explicit approximation, not the unchanged inertial model.

## Immediate purpose and next step

Detailed closure research is not a prerequisite for continuing the current
geometry and whole-cycle pump derivation. Continue with the ideal-valve baseline:
connect piston motion, chamber storage, full-open losses and external loads, and
calculate net delivery and bulk pressure/loading trends under explicit assumptions.
Preserve the distinction between bulk hydraulic load and a true maximum including
switching transients. Once a valve is shortlisted, use measured/manufacturer
opening and closing behaviour to assess whether those omitted effects materially
change delivery, waveform or design loads.

The aim remains a model that helps choose geometry and timing to meet the flow
and pressure requirements, followed by the MATLAB visualisation. This step does
not choose a valve, build a controller or establish a full-cycle force rating.

## Reproduce the adjustable budget

Default equal allocation:

```bash
python python/build_operating_matrix.py
```

An unequal comparison, rewriting the generated budget documents:

```bash
python python/build_operating_matrix.py --right-duty-fraction 0.6
```

The generator validates 0 < lambda_R < 1, records separate R/L budgets and leaves
all circuit flow targets and pulse counts unchanged. It does not implement the
piecewise motion or coupled hydraulic model. The saved matrix retains 0.5.

## References and scope

1. Leighton RF, Weissler AM, Weinstein PB, Wooley CF. Right and left ventricular
   systolic time intervals: effects of heart rate, respiration and atrial pacing.
   Am J Cardiol. 1971;27(1):66–72.
   [DOI: 10.1016/0002-9149(71)90084-1](https://doi.org/10.1016/0002-9149(71)90084-1).
   Publisher abstract accessible through search; direct publisher retrieval denied.
2. Hirschfeld S, Meyer R, Schwartz DC, Korfhagen J, Kaplan S. Measurement of right
   and left ventricular systolic time intervals by echocardiography.
   Circulation. 1975;51(2):304–309.
   [DOI: 10.1161/01.CIR.51.2.304](https://doi.org/10.1161/01.CIR.51.2.304).
   Indexed primary-paper abstract inspected; full text not retrieved.

Equations (1)–(5) are schedule definitions, kinematic scaling and conservation
expressions for the proposed rig. The physiological papers do not prescribe them.
