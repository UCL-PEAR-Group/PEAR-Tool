# Cardiovascular piston pumps: literature review and pressure-model starting point

21 November 2026 · MECH0073 · working review, not a completed or validated pump design

**Recommendation:** use Franzetti's 2019 article and 2020 thesis as the initial hydraulic modelling framework. Separate the piston motion, chamber storage, valve/line impedance and external circulatory load. Keep the single chamber alternating between right/left duties (1A) and two dedicated chambers (1B) open. The spreadsheet begins with transparent algebra; a full dynamic circuit remains a subsequent derivation and verification task.

## Goal and operating point

Our goal is a controllable benchtop source for EVAR-related vascular experiments, coupled to the rig's reservoirs, Windkessels, phantom and sensors. Physiological resemblance is useful when it improves the pressure, flow and deformation boundary conditions being investigated. Reproducing every property of a biological ventricle is a separate, more demanding objective.

User-prescribed baseline: **5 L/min and 75 pulses/min per circuit**. Consequently, net delivered volume is 5000/75 = **66.67 mL per pulse**, and the circuit pulse period is **0.8 s**. These values do not determine pressure. In a closed two-circuit arrangement, each circuit carries 5 L/min on average; adding their flows does not give a 10 L/min systemic cardiac output.

For ideal full filling, no leakage and no compressible storage, net delivery equals swept volume. A 50 mm flat plunger would then need **33.95 mm travel**. That bore is an illustration, not a selected component. For 1A, one right and one left duty per circuit period require **150 physical delivery cycles/min**; 1B requires **75 cycles/min for each chamber**. Routing time, gas state and the different loads must subsequently be included.

## Scope and method

This is a **targeted literature review**, not a systematic search or a claim to exhaustive coverage. The supplied Mazhar review (M24) was used to find pump families, followed by primary publisher, PubMed and author-repository content. Search concepts included piston mock ventricle, pulsatile volumetric pump, aortic flow pump, mock circulatory loop, Frank–Starling piston control, and chamber motion/force design. Search and reading date: 21 November 2026.

The register contains twelve primary journal papers, one thesis and the seed review. Access is recorded individually. Full methods were inspected where available; abstract-only papers support purpose/architecture screening, not extraction of unseen equations. Shaikh and Kizilski remain provisional piston classifications because the accessible primary abstracts do not establish their complete hardware. Vignali's partial abstract is supplemented by Bardi's accessible use of that platform. Franzetti's paper/thesis are one platform family, as are the related Vignali/Bardi papers; they are not independent confirmations.

The comparison follows the seed review's emphasis on generation principle, flow characteristics and application, and adds **pump role, mathematical usefulness, access level and transfer limitations**. A programmable centrifugal system, Herwald et al. (2024), DOI [10.1016/j.ohx.2024.e00561](https://doi.org/10.1016/j.ohx.2024.e00561), was screened out of the piston set after its primary methods identified the mechanism. It remains a credible alternative waveform source.

## Purpose-based comparison

| Source | Role in the experiment | What we can take forward |
|---|---|---|
| F19 + T20, Franzetti | Supply patient-specific aortic flow and tune a physical afterload | Closest initial pressure/flow/force framework; details below |
| L09, Lanzarone | Mock ventricular source for circulatory device tests | Relevant predecessor and valve-characterisation precedent |
| TS10, Tsai & Savaş | Add pulsation to a gear pump's mean flow | Separate oscillatory displacement from net delivery |
| C16, Chaudhury | Drive aortic-model flow experiments | Waveform and hydraulic-load performance comparator |
| V22, Vignali; B24, Bardi | Aortic and compliant AAA phantom experiments | Connect pump output, phantom measurements and controlled afterload |
| R13, Ruiz | Whole-circulation emulator around support-device tests | Chamber roles and timing; the test rig is distinct from the LVAD under test |
| SI18, Shi | Reproduce chamber motion through hydraulic actuation of sacs | Motion-to-travel/velocity/acceleration design |
| G15, Gwak | Reproduce filling-dependent ventricular response | Future pressure/volume control objective |
| K23, Kizilski | Paediatric pulmonary-valve evaluation | Right-side metrics; scale and hardware need separate review |
| SH10, Shaikh; SO12, Song | Pressure conditioning or perfusion of engineered tissue | Useful component ideas; a different pump duty |

See the workbook's filterable **Literature** sheet and [source register](literature_register.json) for the title, DOI, accessible content, numerical conditions and reading location for every entry. The reported operating conditions are examples from those studies, not a common capability envelope.

## What the two supplied sources contribute

**Franzetti 2019:** §2.1 connects the required flow and stroke to the piston, then obtains the chamber pressure from the connected hydraulic circuit and converts it to pressure force. The article separates pressure load, translating-mass inertia and friction before sizing the ball screw and motor. Its three-element Windkessel supplies the downstream relationship between flow and pressure. This is directly suited to our need to understand parameter changes before choosing hardware.

The abstract reports flow-generation tests at 2–5 L/min and 40–70 bpm. The waveform-generation routine was separately tested over 1–6 L/min and 40–80 bpm. Those are different kinds of evidence; neither proves our proposed 5 L/min, 75 bpm assembly. The paper also measures valve backflow: approximately 6% of stroke volume at 70 bpm and 4 L/min in the reported case. This supports keeping leakage/backflow assumptions explicit rather than treating geometric sweep as measured delivery.

Its worked example uses a 50 mm piston diameter and obtains approximately 65.41 N pressure force at 250 mmHg chamber pressure. The total estimate is approximately 183 N after adding inertia and friction. In particular, the **115 N friction term was borrowed from an earlier apparatus**. It is not an estimate for our seals, guide or mechanism. The paper's `A = 50 mm` notation in the worked discussion is dimensionally a diameter, whereas force calculations require area.

**Franzetti thesis, chapter 2:** pp 91–100 provide the most useful extra detail. Figure 2.3 includes the inlet passage, changes in cross-section, mitral valve, ventricular chamber, aortic valve and external load. Equations 2.1–2.6 model nonlinear valve losses, viscous pipe resistance, fluid inertance and local passage effects. Equations 2.7–2.11 connect pressure and flow to piston force and drive sizing; Eq 2.12 describes the load.

The thesis should be read critically:

- Printed Eq 2.5 on p 96 appears to omit a factor of **1/3** in the viscous resistance of a linearly tapered circular passage. Integrating the local Poiseuille expression gives `R = 128 mu L / [3 pi (Din - Dout)] × (Dout^-3 - Din^-3)`. Its equal-diameter limit is the ordinary straight-pipe expression. The printed version gives three times that limit. Direct numerical integration agrees with the corrected expression; see [algebra checks](algebra_verification.json). This identifies a printed-equation issue, not an established error in the original simulation code.
- A Bernoulli pressure-recovery term for an expansion is not a dissipative resistance. Keep reversible changes of kinetic energy separate from irreversible losses.
- `v / screw lead` is revolutions per second; angular speed in rad/s needs the factor `2 pi`. Units must be checked before transferring the drive expressions.
- The air in its afterload compliance chamber is in a different location from our proposed sealed ventricular pocket. The latter needs an additional chamber storage equation.

## How pressure enters our model

The following is a proposed model structure, synthesised from the supplied hydraulic framework and conservation. It is not a claim that one cited paper implements all our proposed features. Use SI internally: pressure Pa, volume m³, flow m³/s, length m, force N. Display conversions are 1 L/min = 1/60000 m³/s, 1 mL = 10^-6 m³, and approximately 1 mmHg = 133.322 Pa.

**1. Motion and displacement.** Let `Ap` be the flat piston area, `x` advance into the fluid, and `S` the stroke. Then `Vs = Ap S` and `Qp = Ap dx/dt`. Only in the negligible-storage, closed-inlet, open-outlet limit does `Qout = Qp`. Full extension/retraction over a repeating cycle must have equal net travel; unequal durations and speeds are possible.

**2. Open-valve hydraulic path.** A useful lumped expression is `pc - po = R Qout + B Qout abs(Qout) + I dQout/dt`, where `pc` is chamber pressure and `po` the pressure beyond the outlet path. `R` represents an applicable linear loss, `B` the quadratic loss coefficient, and `I` fluid inertance. Their SI units are respectively Pa s/m³, Pa s²/m⁶ and Pa s²/m³. Inlet flow needs its own analogous equation and upstream pressure.

For a simple orifice, `Bvalve = rho / [2 (Cd Av)^2]`; for a line's lumped local losses, `Bline = rho K / (2 At²)`. `rho` is density, `Av` and `At` are valve and tube areas, and `Cd` and `K` are calibrated dimensionless coefficients. The nominal valve bore is not automatically its effective open area. At a fixed instantaneous flow and fixed Cd, the idealised valve pressure loss varies as bore^-4. This does not mean a real valve's loss always obeys that scaling as its opening changes.

The straight-pipe reference `Rlam = 128 mu L / (pi Dt^4)` assumes fully developed laminar flow. The provisional inertance is `I = rho L / At`. Do not silently use steady Poiseuille friction as an accurate pulsatile, transitional or turbulent law. Select or calibrate the appropriate impedance. A closed check valve requires a different state; the open-path equation alone cannot represent closure, reverse leakage or pressure transients.

**3. Hydraulic force.** `Fh(t) = Ap [pc(t) - prear(t)]`. Rear pressure and chamber pressure must use the same reference. The desired maximum is `max(abs(Fh(t)))` over the complete periodic cycle. Full retraction does not generally coincide with maximum pressure or force. Fluid inertia included in `pc` must not be added again as a second hydraulic force. Later actuator sizing adds translating-mass inertia, friction and mechanism effects separately.

**4. Sealed-air and incomplete-fill branch.** With fixed gas mass, a preliminary polytropic law is `pg,abs Vg^n = constant`, giving `Cg = Vg/(n pg,abs)`. Here `Vg` is gas volume, `n` is the assumed polytropic exponent, and `Cg` is compliance. With rigid walls and incompressible liquid, continuity gives `Cg dpc/dt = Qin - Qout + Ap dx/dt`. Gas-law pressure must be absolute. The liquid-only limit is an algebraic continuity constraint, not a numerical division by zero compliance.

In a sealed chamber, missing liquid cannot be replaced by arbitrary new air on each cycle: gas mass is fixed and its volume changes with pressure. A filling deficit therefore changes pressure/gas volume and the next cycle's initial state. Sustainable periodic operation also requires mean inlet and outlet liquid flows to balance. Neither an efficiency scalar nor resetting the gas state after each duty captures that evolution. Our gas law, thermal assumptions and air retention need explicit later examination.

**5. External load and reservoirs.** A three-element load can be written `Cw dpw/dt = Qout - (pw - pret)/R2` and `po = pw + R1 Qout`. Here `pw` is the compliance-node pressure, `pret` the return reference and `R1`, `R2`, `Cw` the supplied load parameters. This specifies the pump interface without redesigning the Windkessels. In periodic operation with constant parameters, the mean relation is `mean(po) - pret = (R1 + R2) mean(Qout)`. Transient pressure also depends on compliance and waveform. Flow and pressure cannot be independently imposed on an unchanged passive load.

Reservoir continuity is `dVres/dt = Qreturn - Qin`, with pressure determined by reservoir height or compliance. Two dedicated chambers require two chamber/valve models and reservoir balances. A shared chamber additionally needs an explicit routing state, isolation of different pressure circuits, and continuity of gas and liquid states across the right-to-left transition.

## What the spreadsheet does now

[Pump_pressure_literature_starter.xlsx](../spreadsheet/Pump_pressure_literature_starter.xlsx) contains editable baseline inputs, volume/travel calculations, a **local open-outlet pressure/force calculation**, diameter sensitivities, a literature register and the equation map. Amber cells are assumptions or prescribed inputs; formula cells remain visible and editable. Pressure at the external outlet is an input to this local calculation, not a solved Windkessel output.

The default illustrative point assumes 40% ejection duration and uses the resulting average flow during ejection, 12.5 L/min, as a chosen instantaneous flow. It is **not a peak**. A separate multiplier lets the reader examine other local flows without pretending a complete waveform has been specified. The outlet pressure is held at an illustrative 90 mmHg gauge, rear pressure is zero gauge, and the acceleration is zero for that chosen point. The default calibrated linear resistance is zero because none has been established; the separate assumed quadratic line loss is included. These defaults must not be read as a pressure trace or as a complete friction model.

The spreadsheet intentionally does not calculate maximum force, filling dynamics, gas compression over time, valve switching or a full closed loop. The existing exploratory Python solver is preserved, but is not treated as the completed, literature-verified derivation. Spreadsheet formula results are checked against independent calculations and selected input perturbations; desktop Excel/LibreOffice execution and physical validation remain unperformed.

## Next derivation, with user input

1. Agree the first one-chamber control volume and sensor locations: reservoir → inlet valve → chamber → outlet valve → supplied load.
2. Choose the first pressure-law fidelity: measured component curves versus provisional linear/quadratic losses and inertance. Record fluid temperature, viscosity, density and passage geometry.
3. Define a flow/displacement waveform with the correct 66.67 mL integral, then solve chamber and boundary pressure histories. A selected mean pressure is not a peak-pressure history.
4. Verify a full-liquid case, then add retained gas and finite filling. Test conservation, time-step convergence, coefficient sensitivity and uncertainty before comparing measurements.
5. Apply the same verified chamber model to 1A routing and 1B coupling. Only then compare maximum hydraulic load and component feasibility over agreed operating cases.

No architecture is selected and no new physical performance claim is made by this review.
