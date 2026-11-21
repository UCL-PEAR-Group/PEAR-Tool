# Derivation 01 — full-liquid chamber, open-path pressure and piston force

21 November 2026 · MECH0073 · analytical stage, not a new simulation

The purpose of this step is to connect the prescribed delivery and piston motion to the required chamber pressure and hydraulic piston load. Keep the bore and travel as design variables. Use one chamber first; this is the common building block for concepts 1A and 1B.

## 1. System boundary and assumptions

The atrial reservoir feeds an inlet valve and passage. The liquid-filled chamber ejects through its outlet valve and passage into the external load. Define the pressure measurement stations before assigning resistance or inertance to a component:

- `pi(t)`: upstream inlet-path pressure.
- `pc(t)`: approximately uniform chamber pressure, taken to represent the piston-face pressure.
- `po(t)`: pressure at the downstream end of the modelled outlet path, where the external load begins.
- `pb(t)`: pressure on the dry rear face of the piston.

All pressures share a reference; use Pa internally and mmHg for display. Pressure at an outlet sensor is not automatically piston-face pressure. Passage elements between the chamber and that sensor must be included once, and components beyond it belong to the external load.

Assume constant liquid density, negligible liquid compressibility and wall compliance, no trapped gas, no leakage, constant flat piston area, and negligible distributed chamber pressure variation. Treat valves as ideal one-way devices with losses while open. These are modelling assumptions, not verified rig properties. Initially take the pressure stations at the same elevation and omit unresolved velocity-head differences. If real stations differ in elevation or velocity, add the corresponding hydrostatic and reversible kinetic-pressure terms separately; do not label pressure recovery as dissipation.

The phase-specific results below apply only while the stated valve arrangement is consistent with the pressure and flow solution. Switching transients are not solved here.

## 2. Define motion and geometry

Let `Dp` be face diameter (m), `Ap` face area (m²), `x(t)` piston advance into the liquid (m), `v = dx/dt` (m/s) and `a = dv/dt` (m/s²). Set `x = 0` at full retraction and `x = S` at full advance. Let `Vc,0` be chamber volume at full retraction (m³), including residual volume.

**(1) Ap = pi Dp² / 4; Vc(t) = Vc,0 − Ap x(t)**

Here `pi` in the area expression means the mathematical constant; use `p_i` in code for inlet pressure to avoid a naming collision. There is no wetted rod-area correction.

Differentiating the volume expression gives:

**(2) dVc/dt = −Ap v**

Cylinder length, end clearance and minimum chamber volume constrain usable stroke separately. No cylinder length is selected by this derivation.

## 3. Derive the liquid-volume balance

Let `Qi` and `Qo` be positive forward inlet and outlet flows (m³/s). For the moving control volume, conservation of mass is:

`d(rho Vc)/dt = rho Qi − rho Qo`

Constant density cancels, so `dVc/dt = Qi − Qo`. Combining with (2):

**(3) Qo − Qi = Ap v**

This is the fundamental coupling. It does not say outlet flow equals piston displacement rate in every valve state.

| Assumed phase | Valve-flow condition | Consequence |
|---|---|---|
| Ejection | Inlet closed: Qi = 0; outlet open | Qo = Ap v, with v > 0 |
| Filling | Outlet closed: Qo = 0; inlet open | Qi = −Ap v, with v < 0 |
| Both closed | Qi = Qo = 0 | v must equal zero in this incompressible, rigid limit |

Integrating ejection from `x = 0` to `x = S` gives `Vdel = integral(Qo dt) = Ap S`. At 5 L/min and 75 deliveries/min per circuit, the required ideal net delivery is **66.67 mL**, giving `Ap S = 66.67 × 10^-6 m³`. This is a full-fill, separated-phase result. It is not a general delivery law for gas, backflow, bypass or simultaneous forward flow through both valves.

The dedicated-chamber period is 60/75 = **0.8 s**. The mean-flow specification fixes the integral of Qo, not its peak or time derivative. For shared-chamber concept 1A, 75 deliveries/min to each circuit means 150 physical delivery cycles/min; the single-chamber equations still apply to each duty, but its timing and boundary pressures change.

## 4. Derive an open-path pressure law

For a uniform line of area `At` (m²), length `L` (m), density `rho` (kg/m³), mean velocity `u = Q/At` and liquid mass `m = rho At L`, the lumped axial acceleration force is:

`m du/dt = rho At L × (1/At) dQ/dt = rho L dQ/dt`

Dividing by line area converts force into pressure:

**(4) Δp_inertia = I dQ/dt, where I = rho L / At**

This is a lumped inertance approximation. It stores and returns kinetic energy; its pressure contribution can be negative during deceleration. It is not an always-positive friction loss.

Represent the dissipative contributions provisionally as a linear term `R Q` and a quadratic term `B Q abs(Q)`. With the pressure-station assumptions in section 1:

**(5) p_up − p_down = R Q + B Q abs(Q) + I dQ/dt**

| Coefficient | SI unit | Possible initial expression | Qualification |
|---|---|---|---|
| R | Pa s/m³ | 128 mu L / (pi Dt^4) | Fully developed laminar circular-pipe reference; not an established law for every pulsatile BMF case |
| B, valve | Pa s²/m⁶ | rho / [2 (Cd Av)²] | Constant effective area Av and discharge coefficient Cd; calibrate against the selected valve |
| B, local line loss | Pa s²/m⁶ | rho K / (2 At²) | Geometry-specific coefficient K; not automatically a pipe-friction factor |
| I | Pa s²/m³ | rho L / At | Uniform-line approximation; include each accelerating fluid region once |

Here `mu` is dynamic viscosity (Pa s), `Dt` is tube bore (m), `Av` is valve effective area (m²), and `Cd` and `K` are dimensionless. The valve formula follows by rearranging the assumed orifice law `Q = Cd Av sqrt(2 Δp/rho)` for forward flow. Each term in (5) has units Pa. R and B must represent distinct contributions, or a fitted combined law, to avoid counting the same loss twice.

## 5. Apply the law to ejection and filling

Use separate coefficients for the inlet and outlet paths. While both branches are open, their general forward-flow equations are:

`pi − pc = Ri Qi + Bi Qi abs(Qi) + Ii dQi/dt`

`pc − po = Ro Qo + Bo Qo abs(Qo) + Io dQo/dt`

For **ejection with the inlet closed**, substitute `Qo = Ap v` and `dQo/dt = Ap a`. Since forward Qo is positive:

**(6) pc = po + Ro Ap v + Bo (Ap v)² + Io Ap a**

For **filling with the outlet closed**, use `Qi = −Ap v` and calculate:

**(7) pc = pi − [Ri Qi + Bi Qi² + Ii dQi/dt]**

Equation (7) explains why filling can depress chamber pressure below the upstream reservoir pressure while flow is accelerating. During deceleration the inertial contribution changes sign, so the chamber need not remain below the reservoir throughout the phase.

Prescribing v cannot guarantee that either assumed valve state is feasible. For example, a closed inlet with zero cracking pressure requires `pi ≤ pc`; otherwise inlet flow can start. A closed outlet requires `pc ≤ po`. An already-open valve can maintain forward flow against an adverse pressure gradient while that flow decelerates. Ideal closure occurs when forward flow reaches zero, not automatically when pressure difference changes sign. If the assumed phase fails these checks, a valve-event model or another operating trajectory is needed.

## 6. Convert chamber pressure to hydraulic force

For the approximately uniform chamber pressure and flat face:

**(8) Fh = Ap (pc − pb)**

Fh is the signed balancing force required against the fluid pressure, positive in the piston-advance direction. For nonuniform face pressure, the pressure difference must instead be integrated over the face. With an atmospheric rear face, gauge chamber pressure may be used directly. Inlet reservoir pressure is not the rear-face pressure.

Combining (6) and (8) gives the ejection-phase result:

**(9) Fh = Ap (po − pb) + Ro Ap² v + Bo Ap³ v² + Io Ap² a**

This expression joins geometry, displacement speed, acceleration, passage properties and external load. Its separate terms are the downstream pressure load, linear-loss load, quadratic-loss load and hydraulic inertia load. Dimensions are N throughout.

The required hydraulic-force envelope is `Fh,max = max over the cycle of abs(Fh(t))`. The largest load need not occur at full retraction, maximum speed or peak outlet pressure: their timings may differ. Equation (9) alone is an ejection-phase expression; use (7) and (8) for filling and address transitions before claiming a cycle maximum. Solid-moving-mass inertia, seals and the converter remain outside this hydraulic load. Fluid inertia already included in pc must not be added a second time.

## 7. Keep the external load as an interface

`po(t)` is a boundary input to the chamber calculation until the supplied load is coupled. If that load is a three-element Windkessel, its interface is:

`po = pw + R1 Qo`

`Cw dpw/dt = Qo − (pw − pret)/R2`

`pw` is compliance-node pressure (Pa), `pret` is return pressure (Pa), `R1` and `R2` are resistances (Pa s/m³), and `Cw` is compliance (m³/Pa). These equations explain how the outlet waveform would be calculated without designing the Windkessel hardware here. Do not also prescribe an independent po waveform when these equations already determine it.

Pressure cannot be uniquely calculated from 5 L/min and 75/min without the connected load, the motion/flow waveform and the initial or periodic state. The present spreadsheet holds po at a chosen local value; it has not solved these load equations.

## 8. Design consequences and limits

At the same required delivery and the same chosen flow waveform, increasing piston diameter reduces travel, speed and acceleration in inverse proportion to area. If the fluid paths and boundary pressures are unchanged, chamber pressure is unchanged in this lumped limit, while hydraulic force grows with piston area. Thus doubling bore quarters travel and quadruples hydraulic force. This comparison is different from increasing bore while holding travel fixed, which would change the delivered volume.

At fixed forward flow and constant Cd, reducing valve effective bore increases the simple-orifice pressure loss in inverse proportion to bore^4. Inlet changes affect filling pressure; outlet changes affect ejection pressure. Both may affect whether the assumed full-liquid state is sustainable. Real valve area, Cd and fluid impedance can depend on operating conditions.

The rigid, incompressible model cannot describe a pressure-building interval with both valves closed and a moving piston. If both valves are closed and the piston is stationary, continuity alone also does not determine chamber pressure. Finite liquid/wall compliance or the retained-gas branch is needed to resolve those transitions; full liquid filling does not mean a real chamber has exactly zero compliance. This is a known limitation of the present analytical limit, not evidence that the real mechanism can move against a locked incompressible volume.

No new dimensions, fluid coefficients, waveform or maximum force are selected here. The next collaborative step is to specify the ejection/filling timing and a smooth displacement or flow waveform with the correct volume integral, then check the phase assumptions before evaluating pressure histories. The 40% timing fraction in the starter workbook remains an illustration.

## Provenance and verification status

This derivation uses conservation and a lumped momentum approximation, informed by the supplied **Franzetti thesis (2020), chapter 2, Fig 2.3 and Eqs 2.1–2.9, pp 94–97**, and **Franzetti et al. (2019), §2.1–2.2**, DOI [10.1115/1.4044488](https://doi.org/10.1115/1.4044488). It is a re-derivation with explicit sign conventions and limits, not a verbatim transfer of their complete apparatus model. The original attachment filenames are `PhD_Thesis_Franzetti_final.pdf` and `jesmdt_002_04_041004.pdf`.

Checks in this step: moving-volume sign, inlet/outlet phase signs, dimensional consistency of pressure and force terms, and zero-loss/zero-acceleration limits. No new dynamic simulation, spreadsheet modification, component calibration or physical validation has been performed. Existing exploratory results remain separate.
