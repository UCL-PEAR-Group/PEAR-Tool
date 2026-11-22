# Derivation 05 — piston-phase windows and pressure-conditioned valve commands

22 November 2026. A candidate analytical sequence for review, following the
user's direction to proceed. The confirmed design uses enforced valves,
coordinates them with piston motion and may use pressure to govern transitions.
This document keeps pressure-conditioned and phase-only operation selectable.
No numerical thresholds, valve response times, hardware or final controller are
selected. No new coupled simulation, MATLAB run or maximum-force rating is
claimed. Derive and review these rules before implementing the next simulation.

## 1. Separate three quantities

1. **Motion:** prescribed piston position x(t), with positive x into the chamber.
2. **Command:** desired open/closed valve state u_j, for inlet j = i and outlet j = o.
3. **Opening:** physical effective-area fraction a_j between zero and one.

A commanded state is not a measured opening, and an open path does not prescribe
its flow. The flow follows from pressure, fluid inertia and valve/path losses.
The cardiac names identify the intended functional roles. The physical actuator
may be mechanical or electronic; this step does not select it.

Paeme et al. [1] provide a physiological modelling reference for pressure/flow
coupling and finite mitral-aperture dynamics. The command sequence and smooth
opening approximation below are engineering proposals, not laws taken from that
paper and not a validated reproduction of cardiac valve behaviour.

## 2. Tie valve eligibility to the existing motion

For a constant-rate case, let f be physical chamber cycles per minute, T the
period in seconds, t0 a cycle origin and phi dimensionless cycle phase:

$$
T=\frac{60}{f},\qquad
\phi(t)=\frac{(t-t_0)\bmod T}{T},\qquad
x(t)=S X(\phi),\qquad
\dot x=\frac{S}{T}X'(\phi). \tag{1}
$$

Here S is travel in m and X is the chosen dimensionless displacement waveform.
For this candidate, X rises monotonically from zero to one over 0 <= phi <= gamma,
then falls to zero over gamma <= phi <= 1. Gamma is the advance fraction, and is
not automatically the fraction during which fluid is actually ejected.
The same intermediate x occurs in both directions, so use phase/direction and
cycle state; position alone does not identify filling versus delivery. A varying
rate case needs a continuous phase accumulator and is outside this constant-rate
step.

The current trial interprets the earlier 60:40 filling:ejection allocation as
60% return and 40% advance, gamma = 0.4. Valve-open durations will generally be
shorter or shifted. If the specification instead requires a 60:40 ratio of actual
flow durations, that needs a different constraint on the completed solution.

| Per-circuit rate h | Architecture | Physical chamber rate f | T | Advance gamma T | Return (1-gamma) T |
| --- | --- | --- | --- | --- | --- |
| 75/min | 1B: each dedicated chamber | 75/min | 0.800 s | 0.320 s | 0.480 s |
| 75/min | 1A: equal right/left duty slots | 150/min | 0.400 s | 0.160 s | 0.240 s |
| 180/min | 1B: each dedicated chamber | 180/min | 0.333 s | 0.133 s | 0.200 s |
| 180/min | 1A: equal right/left duty slots | 360/min | 0.167 s | 0.0667 s | 0.100 s |

These are kinematic budgets, not demonstrations of achievable operation. For 1A,
selector movement and any isolation interval must fit into the two duty slots,
or the motion allocation must be revised. No additional dwell is silently added.

Define permitted command intervals using four free phase parameters:

$$
W_o=[\phi_{o,s},\phi_{o,c}),\qquad
W_i=[\phi_{i,s},\phi_{i,c}),\qquad
0\le\phi_{o,s}<\phi_{o,c}\le\gamma
\le\phi_{i,s}<\phi_{i,c}\le1. \tag{2}
$$

Subscript s means earliest permitted opening command; c means scheduled closing
command. These windows are a proposed non-overlapping baseline. Deliberate spill
or overlap would require a separately declared sequence.

## 3. Optional pressure condition for initiating opening

Use forward pressure differences, with all pressures sharing a gauge reference:

$$
\Delta p_i=p_i-p_c,\qquad
\Delta p_o=p_c-p_a. \tag{3}
$$

The inlet reservoir, chamber and connected arterial-node pressures are p_i, p_c
and p_a, in Pa. In the shared chamber, the selected right/left routing state
identifies which reservoir and arterial node are used.

Let delta-p-open,j >= 0 be an adjustable pressure margin, in Pa. It is a controller
threshold, not an assumed physical cracking pressure. Let chi select the mode:

$$
G_j(t)=
\begin{cases}
1, & \chi=0 \quad\text{phase-only mode},\\
\mathbf{1}\{\Delta p_j(t)\ge\delta p_{\mathrm{open},j}\},
& \chi=1 \quad\text{phase plus pressure mode}.
\end{cases} \tag{4}
$$

The first mode still calculates pressure and loading; it simply does not use
pressure to initiate the command. The second may delay opening within its window.
Neither mode guarantees a particular mean flow or prevents reverse flow after
opening. Actual one-way hardware, if used, needs its own declared behaviour.

Define b_j = 1 when the opposite path is physically closed, the required routing
connection has settled, and the sequence permits this valve to open. This is a
proposed interlock for the first comparison. Its simulated value comes from the
opening/routing model; using actual hardware would require position information
or a justified response model, not assuming a command has already completed.

If the opening duration is tau-open,j, require enough time for opening before
the scheduled closing command in this candidate:

$$
t_{j,\mathrm{on}}
=\inf\left\{t:\phi(t)\in W_j,\ G_j(t)=1,\ b_j(t)=1,
\ t+\tau_{\mathrm{open},j}\le t_{j,c}\right\}, \tag{5}
$$

where t_j,c is the closing-command time in the current cycle. Evaluate (5) only
for a valve that is closed and has not yet opened in that cycle. If the set is
empty, record a missed opening and the resulting flow/inventory response. Do not
assume that a target volume was delivered. Excluding an incomplete opening is a
candidate modelling choice, not a general physical restriction on real valves.

Once triggered, latch the command open until the scheduled closing event:

$$
u_j(t)=
\begin{cases}
1,&t_{j,\mathrm{on}}\le t<t_{j,c},\\
0,&\text{otherwise}.
\end{cases} \tag{6}
$$

There is at most one opening command per path per duty in this baseline. A later
pressure-gradient reversal does not instantly flip the command. This makes the
proposed closure rule explicit rather than importing passive check-valve logic.
It does not guarantee no reverse flow and does not resolve measurement noise:
filtering, trigger persistence or hysteresis need specification for hardware.

A failed pressure condition does not pause the prescribed piston. Adding a dwell,
slowing the piston or aborting a cycle changes the motion/control problem and must
be declared. Gas volume, absolute pressure and liquid inventory must remain within
the domain of the constitutive model; an invalid trajectory has no valid force
rating even if the phase schedule is well defined.

## 4. Give opening and closure a finite duration

For a commanded transition at t_cmd, one provisional effective-area response is

$$
a_j(t)=a_{j,0}+(a_{j,\mathrm{target}}-a_{j,0})
H\!\left(\frac{t-t_{\mathrm{cmd}}}{\tau_j}\right), \tag{7}
$$

$$
H(s)=\begin{cases}
0,&s\le0,\\
10s^3-15s^4+6s^5,&0<s<1,\\
1,&s\ge1.
\end{cases} \tag{8}
$$

The initial and target fractions are a_j,0 and a_j,target; tau_j is the positive
transition duration in s, chosen separately for opening and closing. H has zero
first and second derivatives at both endpoints and is monotonic because
H'(s) = 30 s²(1-s)² inside the interval. It is a transparent prescribed aperture
approximation. It is not a measured actuator response, and actuator travel need
not be proportional to effective flow area. The candidate schedule avoids
interrupting an opening transition; changed commands mid-transition need a
separate response law. Command/sensing delays are omitted in this initial law.

To complete physical outlet closure before return and inlet closure before the
next advance, the candidate must satisfy

$$
\phi_{o,c}+\frac{\tau_{\mathrm{close},o}}{T}\le\gamma,
\qquad
\phi_{i,c}+\frac{\tau_{\mathrm{close},i}}{T}\le1. \tag{9}
$$

If command or actuator delay is later included, add it to the appropriate closure
budget. The maximum fully open duration in a duty is

$$
t_{\mathrm{fully\ open},j}=
\max\!\left(0,t_{j,c}-t_{j,\mathrm{on}}-\tau_{\mathrm{open},j}\right). \tag{10}
$$

Flow can also occur while a valve is partially open; (10) is not the ejected-volume
integration interval. Opening/closing time is a component property for a given
operating condition, not a duration that automatically shrinks in proportion to T.
Thus a fixed response time takes a larger phase fraction at higher bpm. Preserve
that distinction in a rate study.

The intended sequence, after accounting for the two transition intervals, is:

| Stage | Motion | Inlet command | Outlet command | Event or consequence |
| --- | --- | --- | --- | --- |
| Pressure build-up | Early advance | Closed | Closed | Gas compression raises chamber pressure; await outlet eligibility |
| Delivery | Advance | Closed | Open, then scheduled closure | Actual flow follows pressure and effective area |
| Pressure release | Early return | Closed | Closed | Gas expansion lowers chamber pressure; await inlet eligibility |
| Filling | Return | Open, then scheduled closure | Closed | Actual inlet volume is integrated, not assumed equal to swept volume |

These are rig phase names. Both-closed motion preserves liquid inventory under
our assumptions while changing gas and total chamber volume. A stationary piston
with both valves closed gives no pressure relaxation in the constant-n model.

## 5. Derive opening position from retained-air compression

This gives a concrete link between piston position and pressure eligibility.
Consider a both-closed interval starting at x0 with gas volume Vg0 and absolute
pressure Pg0. Until a valve starts opening,

$$
V_g=V_{g0}-A_p(x-x_0),\qquad
P_g(x)=P_{g0}\left[\frac{V_{g0}}{V_{g0}-A_p(x-x_0)}\right]^n. \tag{11}
$$

A_p = pi D_p²/4 is wetted face area in m², Vg0 is in m³ and n is the assumed
constant polytropic exponent. All gas pressures are absolute. If the outlet
pressure is temporarily constant, its pressure-eligibility threshold is

$$
P_\star=p_{\mathrm{atm}}+p_a+\delta p_{\mathrm{open},o}. \tag{12}
$$

For Pstar > Pg0, solving (11) for displacement gives

$$
\Delta x_\star=\frac{V_{g0}}{A_p}
\left[1-\left(\frac{P_{g0}}{P_\star}\right)^{1/n}\right],
\qquad
\frac{\Delta x_\star}{S}=\frac{V_{g0}}{V_s}
\left[1-\left(\frac{P_{g0}}{P_\star}\right)^{1/n}\right],\quad V_s=A_pS.
\tag{13}
$$

If Pstar <= Pg0 the pressure condition is already satisfied at the start, so its
required additional compression is zero. A later phase-window start can still
delay opening. If the required displacement is beyond the permitted opening
window, the opening is missed for that duty. For a varying arterial pressure,
solve the time-dependent event p_c(t) - p_a(t) - delta-p-open,o = 0 subject to the
other eligibility conditions; do not substitute the mean arterial pressure as
if it were the instantaneous value.

Using the earlier illustrative inputs only (not selected hardware or a simulated
cardiac cycle): Dp = 50 mm, Vg0 = 10 mL, initial chamber pressure 10 mmHg gauge,
constant outlet 90 mmHg gauge, atmospheric pressure 760 mmHg, n = 1.2 and zero
opening margin, the calculated pressure-eligibility point is

$$
A_p\Delta x_\star=0.7907\ \mathrm{mL},\qquad
\Delta x_\star=0.4027\ \mathrm{mm}.
$$

This is about 1.19% of the illustrative 66.667 mL geometric stroke. Substitution
back into (11) returns 90 mmHg gauge to floating-point precision. It is a pressure
eligibility position, not a guaranteed opening event, fixed fraction of elapsed
time or net stroke loss. The phase/interlock rules and finite aperture response
still apply, and stored gas volume can be released later.

During a both-closed return from Pg0 to a lower inlet-opening absolute threshold
Pstar = patm + pi - delta-p-open,i > 0, the required retraction magnitude is

$$
r_\star=\frac{V_{g0}}{A_p}
\left[\left(\frac{P_{g0}}{P_\star}\right)^{1/n}-1\right],\qquad
P_{g0}>P_\star. \tag{14}
$$

If the pressure condition is already satisfied, rstar is zero. The analogous
window, changing reservoir pressure and inventory constraints still apply.
Gas volume and pressure at the beginning of each closed interval must come from
the preceding solution, not be reset to the initial reference charge.

## 6. Apply the law to the two architectures

**1B, dedicated chambers:** preserve the intended linked inlet commands and
linked outlet commands:

$$
u_{i,R}=u_{i,L}=u_{i,\mathrm{pair}},\qquad
u_{o,R}=u_{o,L}=u_{o,\mathrm{pair}}. \tag{15}
$$

For pressure-conditioned opening, a proposed group rule is to require both sides
to be eligible at the same instant:

$$
G_{j,\mathrm{pair}}=G_{j,R}\land G_{j,L},\qquad
b_{j,\mathrm{pair}}=b_{j,R}\land b_{j,L}. \tag{16}
$$

The common permitted window is the intersection of the two phase windows. Use
the first instant satisfying all current conditions, not the maximum of two
historical first-crossing times: a pressure condition can become false again.
A non-overlapping window intersection means the chosen phase offset is infeasible
for this strictly linked schedule. The slower permitted transition must fit both
chambers' timing budgets. This AND rule is a candidate for review, not a confirmed
requirement. Selecting it can delay one side while the other develops the needed
pressure, changing force, filling and delivery.

For an ideal linked physical-state model, a common area fraction can additionally
be imposed: a_j,R = a_j,L = a_j,pair. This is an explicit ideal kinematic
constraint, not evidence of matched hardware response. Identical command bits
alone do not establish that constraint in the rig; a mechanism or feedback must
achieve the intended state matching. Different pressure loads remain present.
Individual per-side pressure-triggered openings would be a different linking
arrangement, not something silently substituted into (15).

**1A, shared chamber:** use the same sequence in each assigned right or left duty.
Only one duty's inlet and outlet connections are active. Route selection occurs
through an explicitly modelled transition; this first comparison proposes
isolating the chamber during that transition. Preserve chamber pressure, gas and
liquid inventory, and both external circuit states. A route change does not
instantaneously equalise pressures. Selector timing and displaced/dead volumes
remain unselected and are not resolved by equations (4)–(8).

## 7. How this connects to pressure, flow and maximum force

The previously derived chamber balance remains

$$
C_g(p_c)\dot p_c=Q_i-Q_o+A_p\dot x,
\qquad C_g=\frac{V_g}{n(p_{\mathrm{atm}}+p_c)}. \tag{17}
$$

C_g has units m³/Pa and all flows are in m³/s. Q_i and Q_o are signed; positive
means into and out of the chamber respectively. The momentum/loss law must use
the actual effective opening a_j(t), not just u_j. For a declared constant lumped
inertance approximation on an open path, its structure is

$$
I_j\dot Q_j=\Delta p_j-R_j(a_j)Q_j-B_j(a_j)Q_j|Q_j|,
\qquad a_j>0. \tag{18}
$$

The coefficient units are Pa s²/m³ for I_j, Pa s/m³ for R_j, and Pa s²/m⁶ for B_j.
Partial-opening loss and inertance laws are still unselected. The previous
full-open coefficients do not supply these laws automatically. The external
Windkessel equations from Derivation 04 continue to evolve with actual outlet
flow; they must not use prescribed piston displaced-volume rate in its place.

Crucially, a smooth aperture trace does not by itself complete the closure
hydraulics. A branch with nonzero fluid momentum cannot simply have Q reset to
zero without treating the transient. Resolve the near-closure pressure/flow law
and the necessary compliance/inertance representation before using peak loads.
The endpoint a = 0 also requires an appropriate closed-boundary formulation;
this derivation does not validate dividing by zero area or arbitrary leakage
regularisation. Abrupt surge resolution may exceed a lumped model's bandwidth.

Once those missing hydraulic constitutive details are resolved, calculate

$$
V_{\mathrm{net},o}=\int_0^T Q_o(t)\,dt,\qquad
\overline Q_o=\frac{V_{\mathrm{net},o}}{T},\qquad
F_h(t)=A_p[p_c(t)-p_b(t)],\qquad
F_{h,\max}=\max_{\mathrm{declared\ cycle}}|F_h(t)|. \tag{19}
$$

Here pb is rear-face gauge pressure, and Fh is the hydraulic plunger force in N.
For 1A, integrate each outlet assignment over the full right/left supercycle to
obtain each circuit's mean flow. Do not count the sum of both duties as cardiac
output. Moving-solid inertia, seals, converter loading and valve-actuator forces
are outside this hydraulic force expression.

## 8. What this step establishes and leaves open

Established for review: explicit phase windows, optional opening-pressure guards,
latched commands, a finite aperture candidate, closure timing inequalities,
closed-gas opening positions and architecture-specific coordination requirements.
These are a useful control specification but not a complete numerical pump model.

| Decision still needed | Candidate for the first comparison | Why it matters |
| --- | --- | --- |
| Opening command policy | Compare phase-only with phase plus pressure using chi | Separates predetermined timing from load-dependent opening |
| Closure command policy | Schedule a finite closure before each reversal | Provides a defined baseline; does not guarantee zero regurgitation or physiological timing |
| Linked-pair pressure policy | Require both chambers ready simultaneously | Preserves linked commands but can penalise the earlier-ready chamber |
| Timing/threshold values | Keep phase limits, margins and transition durations free | Must fit the rate envelope and eventual component/sensor behaviour |
| Effective opening and near-closure hydraulics | Derive from candidate valve geometry/data next | Required for pressure peaks, reverse flow, delivery and force |

No optimal timing or pressure margin is implied. The immediate next analytical
step is opening-dependent hydraulic coefficients and closure behaviour. After
that, numerical verification should check conservation, event order, missed
openings, periodicity and sensitivity before physical calibration/validation.

## Reference and provenance

1. Paeme S, Moorhead KT, Chase JG, et al. Mathematical multi-scale model of the
   cardiovascular system including mitral valve dynamics. Application to ischemic
   mitral insufficiency. BioMedical Engineering OnLine. 2011;10:86.
   DOI: [10.1186/1475-925X-10-86](https://doi.org/10.1186/1475-925X-10-86).
   Publisher full text inspected: Methods, CVS model and mitral-valve dynamics.
   Supports the physiological reference and finite-aperture modelling distinction;
   does not supply our phase windows, thresholds, quintic actuator law or pair rule.

The gas balance and polytropic assumption are carried forward from
[Derivation 04](DERIVATION_04_RETAINED_AIR_AND_VALVE_EVENTS.md), with its source
scope and limitations. Functional assignments follow the user-confirmed
[valve-control record](VALVE_CONTROL_AND_ROUTING.md). All new controller rules
above are declared proposals; numerical timing budgets and gas positions are
calculations from explicitly stated inputs, not literature measurements.
