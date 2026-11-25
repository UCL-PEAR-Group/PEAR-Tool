# Restart 01 — chamber geometry and variable commanded stroke

25 November 2026. This is the current staged derivation direction. It supersedes fixed-travel and retained-front-air assumptions for the new baseline. Earlier derivations, numerical examples, reports and concept scores are preserved; they have not been recalculated for this change.

## Model parts and development order

Develop a parametric model that accepts a piston-position waveform, predicts the pump/circuit response once the later blocks are added, and informs subsequent CAD choices.

| Part | Relationship to establish | Main output |
| --- | --- | --- |
| 1. Chamber geometry | Bore, cylinder length, plunger thickness and extension | Chamber volume, travel limits and geometric sweep |
| 2. Prescribed motion | Position waveform, amplitude, period, phase and advance/return allocation | Position, velocity and acceleration |
| 3. Delivery and volumetric efficiency | Sweep, net delivery and event rate | Delivered stroke volume and mean flow |
| 4. Inflow and outflow | Conservation in the moving liquid-filled chamber | Separate inlet/outlet flow histories |
| 5. Enforced valves | Commands, piston phase, opening area, overlap/dwell and reverse flow | Available flow paths and their timing |
| 6. Pressure dynamics | Viscous/local losses, fluid inertia and any liquid/wall compliance | Chamber and port pressures |
| 7. External circuit | Reservoirs, upstream/downstream pressures and Windkessel loads | Boundary conditions and inventory balance |
| 8. Temperature and fluid properties | Density, viscosity, bulk modulus and thermal dimensional changes | Property inputs and thermal corrections |
| 9. Piston load | Wet/dry pressure exposure, seal friction and moving-solid inertia | Force demand; transmission design is deferred |
| 10. Architecture | Shared sequential duties or two dedicated chambers | Right/left routing, timing and flow balance |
| 11. Measurement and control | Position/pressure/flow/temperature observations and errors | Later feedback, calibration and independent validation |

This step establishes geometry and the volume/motion interface only. No dimensions, waveform family, actuator mechanism or architecture are selected.

## Assumptions

- Straight constant circular bore and flat wetted piston face, with no wetted rod-area deduction.
- Completely liquid-filled wet chamber with no retained air pocket or bubbles.
- Rigid geometry at one reference temperature. Incompressible liquid and no leakage define the ideal hydraulic limit. Finite liquid/wall compliance can be added later without adding air.
- Prescribed piston position with ideal tracking: actual position equals commanded position for this initial model. Actuator/converter kinematics and tracking errors are deferred.
- Adjustable stroke within the user's ideal geometric limit: cylinder internal length minus plunger axial thickness.
- Volumetric efficiency remains in delivered-volume expressions; it is one in the strictly ideal, loss-free case.
- One chamber is considered first. Its event rate is not automatically the pulse rate at each circuit outlet.
- No atmospheric dry-side pressure assumption follows from the air-free wet-chamber assumption. Rear pressure remains a later boundary.

## Variables and conventions

Positive extension advances the piston into the wet chamber and reduces its volume. Lengths are in metres, volumes in cubic metres and time in seconds.

| Symbol | Definition | Role |
| --- | --- | --- |
| \(D\) | Bore / effective wetted-face diameter | CAD parameter |
| \(L_c\) | Internal cylinder axial length | CAD parameter |
| \(t_p\) | Plunger axial thickness | CAD parameter |
| \(L_w\) | Maximum geometric travel | Derived limit |
| \(A_p\) | Wetted piston-face area | Derived, m² |
| \(x(t)\) | Advance from full geometric retraction | Prescribed input |
| \(x_r\) | Chosen retracted starting position | Operating input; initially may be zero |
| \(S\) | Commanded advance excursion per cycle | Adjustable operating input |
| \(V_c(t)\) | Geometric wet-chamber volume | Derived |
| \(V_{s,g}\) | Geometric swept volume of one advance | Derived |
| \(SV\) | Net delivered outlet volume per complete fill–eject cycle | Delivery quantity |
| \(\eta_v\) | Volumetric delivery efficiency | Dimensionless assumption / later calibration |
| \(T_c\) | One chamber fill–eject cycle duration | Timing input |
| \(\psi(\phi)\) | Normalised position-waveform shape | Dimensionless input |

## 1. Area and travel boundary

For \(D>0\) and \(L_c>t_p>0\),

$$
A_p=\frac{\pi D^2}{4},\qquad
L_w=L_c-t_p,\qquad 0\leq x(t)\leq L_w.
$$

For a commanded stroke,

$$
x_{\min}=x_r,\quad x_{\max}=x_r+S,\qquad
x_r\geq0,\quad S\geq0,\quad x_r+S\leq L_w.
$$

Thus the maximum working length limits travel but does not prescribe the stroke used. At \(x_r=0\), \(0\leq S\leq L_c-t_p\). The upper endpoint is a geometric limit, not a recommendation to run against the end wall. Detailed clearances, stops and port geometry may later reduce usable travel.

## 2. Chamber volume from extension

Neglect fixed port/recess volumes in the initial cylindrical model. The remaining axial liquid length is \(L_w-x(t)\):

$$
\boxed{V_c(t)=A_p[L_w-x(t)]
=\frac{\pi D^2}{4}[L_c-t_p-x(t)].}
$$

An infinitesimal extension gives

$$
dV_c=-A_p\,dx.
$$

Integrating over one advance,

$$
V_c(x_r+S)-V_c(x_r)
=-\int_{x_r}^{x_r+S}A_p\,dx=-A_pS.
$$

Therefore the positive geometric swept volume is

$$
\boxed{V_{s,g}=V_c(x_r)-V_c(x_r+S)
=A_pS=\frac{\pi D^2}{4}S.}
$$

A later fixed port/recess volume \(V_d\) adds to \(V_c\) but cancels from this volume difference. A reduced travel limit, in contrast, changes allowable \(S\).

## 3. Delivered volume and volumetric efficiency

For one advance and one return, with outlet flow positive out of the chamber,

$$
SV=\int_{\text{complete chamber cycle}}Q_{\rm out}(t)\,dt,
\qquad
\eta_v=\frac{SV}{V_{s,g}}\quad(V_{s,g}>0).
$$

This is net delivery, including any outlet return flow, at a declared outlet measurement plane. The ordinary efficiency range \(0\leq\eta_v\leq1\) assumes isolated inlet/outlet pumping, losses and no externally driven through-flow.

$$
\boxed{SV=\eta_v A_pS=\eta_v\frac{\pi D^2}{4}S.}
$$

Absence of air alone does not establish unit efficiency: leakage or valve backflow can reduce delivery. Under the additional loss-free, correctly routed ideal conditions, set \(\eta_v=1\), so \(SV=V_{s,g}\).

Efficiency does not modify geometric chamber volume. A cycle-level efficiency does not identify when losses occur and is not an unexplained instantaneous multiplier for the flow waveform. Once leakage/backflow are modelled explicitly, derive efficiency from their results or use a clearly separated residual correction; do not count losses twice. Do not impose an independent underfilling factor while simultaneously assuming a rigid chamber completely filled with incompressible liquid.

For positive target delivery and non-zero assumed efficiency,

$$
\boxed{S_{\rm req}
=\frac{SV_{\rm target}}{\eta_v A_p}
=\frac{4SV_{\rm target}}{\eta_v\pi D^2}.}
$$

The geometric feasibility condition is

$$
\boxed{\frac{4SV_{\rm target}}{\eta_v\pi D^2}
\leq L_c-t_p-x_r.}
$$

If efficiency later depends on stroke, rate, pressure or temperature, sizing becomes an implicit coupled condition. This expression does not yet establish hydraulic or actuator feasibility.

## 4. Position waveform as the input

For one chamber cycle starting at \(t_0\),

$$
\phi=\frac{t-t_0}{T_c},\quad0\leq\phi\leq1,
\qquad
\boxed{x(t)=x_r+S\psi(\phi).}
$$

Use one monotonic advance and one monotonic return, with optional dwells:

$$
0\leq\psi\leq1,\qquad
\psi(0)=\psi(1)=0,\qquad \max\psi=1.
$$

Amplitude, duration and shape are separate inputs. No waveform family or advance/return ratio is chosen here. Different phase durations are allowed while preserving equal advance and return distances in a repeating cycle.

Substitution gives the chamber foundation:

$$
\boxed{V_c(t)=\frac{\pi D^2}{4}
\left[L_c-t_p-x_r-S\psi\!\left(\frac{t-t_0}{T_c}\right)\right].}
$$

Geometric displacement relative to the cycle's starting position is

$$
V_{\rm disp,g}(t)=A_p[x(t)-x_r]=A_pS\psi(\phi).
$$

This is not cumulative outlet delivery: it returns to zero when the piston retracts, although fluid may already have been delivered to the circuit.

For \(S,x_r,T_c\) fixed within a cycle,

$$
\dot x=\frac{S}{T_c}\psi'(\phi),\qquad
\ddot x=\frac{S}{T_c^2}\psi''(\phi),
$$

$$
\boxed{Q_p(t)\equiv-\dot V_c(t)
=A_p\dot x(t)
=\frac{\pi D^2S}{4T_c}\psi'(\phi).}
$$

This signed displacement rate is positive during advance and negative during return. Actual inlet and outlet flows require conservation and valve states.

Stroke can change between cycles if their positions and intended velocities join consistently, for example at a common stationary retracted position. If amplitude or offset varies continuously within a cycle, differentiate the complete supplied \(x(t)\); do not omit the additional derivative terms.

## Checks, limitations and next step

- Area × travel has units m³; area × speed has units m³/s.
- Extension reduces chamber volume; full return restores the starting volume.
- Zero stroke gives zero geometric sweep. The efficiency ratio is undefined at zero sweep.
- At fixed \(D,\eta_v\), delivered stroke volume is proportional to travel. At fixed target volume and efficiency, required travel varies as \(D^{-2}\).
- Geometric sweep depends on endpoints. Its rate depends on waveform derivative and cycle duration. Actual delivery may become shape/rate dependent when losses and valves are resolved.
- A rigid, fully filled, incompressible, leak-free chamber cannot change volume while all flow paths are closed. Later valve timing must permit flow during motion or include justified compliance. This step does not predict a closed-valve pressure transient.

**Next:** derive moving-chamber continuity with explicit signs, then separate inlet and outlet flows using the enforced valve states. Link the outlet integral to stroke volume and event rate before adding pressure dynamics.

## Provenance

These are direct geometric derivations and stated modelling definitions, not fitted performance claims. Revised assumptions are from the user's 25 November 2026 instruction. No new simulation, MATLAB execution, hardware test, dimension selection or matrix re-scoring was performed.

The project handbook is unavailable in the current workspace. The supplied essential project instructions and inspected repository records are used; no unavailable handbook is claimed to have been read.
