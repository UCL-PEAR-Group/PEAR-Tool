# Decision record

## Waveform and timing flexibility — 22 November 2026

- User wants to compare different waveform shapes and different ejection/filling
  ratios. Keep both configurable; no universal waveform has been selected.
- User's 60:40 fallback is explicitly interpreted as filling:ejection, consistent
  with the preceding 40% ejection example. This interpretation is stated to the
  user and can be changed; r = ejection/filling therefore remains 2/3.
- Use published analytical waveforms as candidates. Compare their shape at equal
  phase volume and duration before changing timing or adding hydraulic dynamics.
- Render mathematics in chat using mathematical environments, following the
  user's latest explicit instruction.

## Literature and pressure starting point — 21 November 2026

- User baseline: 5 L/min at 75 pulses/min per circuit (66.67 mL net delivery).
- Use a spreadsheet for visible analytical prototyping while retaining Python
  for the existing exploratory dynamics and later numerical verification.
- Use Franzetti's accessible derivation as a starting framework, with explicit
  checks and extensions; do not adopt another rig's force or friction values.
- Distinguish waveform sources, responsive ventricular emulators, MCS test rigs,
  supplemental pulsators and tissue-conditioning pumps in the evidence register.
- The current spreadsheet is a local full-fill, open-outlet calculation. It
  neither predicts maximum force nor resolves the retained-gas dynamics.
- Both 1A and 1B remain open. The detailed derivation continues collaboratively.

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D001 | 2026-11-21 | Use a flat-face plunger with no wetted rod area deduction | User concept | Accepted |
| D002 | 2026-11-21 | Use 5 L/min and 75 deliveries/min as the nominal reference | User-prescribed targets | Accepted |
| D003 | 2026-11-21 | Retain fixed mechanical travel within each running configuration | User design assumption | Accepted for current model |
| D004 | 2026-11-21 | Model deliberately retained sealed air using a reference gas state | User clarification; actual gas volume varies | Accepted; quantity/thermal model provisional |
| D005 | 2026-11-21 | Keep flow-rising-with-frequency and independent-flow strategies open | User instruction | Open comparison |
| D006 | 2026-11-21 | Estimate hydraulic pressure load before selecting actuation | User scope | Accepted |
| D007 | 2026-11-21 | Use MATLAB as the primary development language going forward | User preference | Superseded by D011 |
| D008 | 2026-11-21 | Preserve executed Python results and previous reports as a reference archive | Reproducibility during migration | Complete |
| D009 | 2026-11-21 | Track V1 on `v1-prototype`; develop Design 1 on `v1-prototype-design-1-piston-pump` | User's prototype/design branch organisation | Implemented |
| D010 | 2026-11-21 | Maintain `MODEL.md` plus a plain-text MATLAB Live Script | Readable explanation, executable calculations and reviewable Git diffs | Superseded by D012 |

No valve bore, cylinder size, net-delivery controller or force rating has been
selected. A bypass and active spill timing are candidates, not accepted designs.
The 50 mm face, 33.95 mm travel and 66.7 mL geometric stroke remain illustrative.

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D011 | 2026-11-21 | Use Python as the primary model language | Latest explicit user instruction; simple local execution | Active; representative regression checks executed |
| D012 | 2026-11-21 | Use a Jupyter notebook and MODEL.md as the living calculation/documentation pair | Retains editable calculations and plots without MATLAB | Active; notebook code cells executed in-process |
| D013 | 2026-11-21 | Classify variables by physical role, numerical type, units and implementation status | User request for all variables and their types | Register added; future quantities explicitly marked |

D011 supersedes D007; D012 supersedes the MATLAB portion of D010. Archived
Python results and the earlier MATLAB source are preserved. No new physical
model or independent-flow controller is introduced by the language change.


## Architecture comparison — 21 November 2026

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D014 | 2026-11-21 | Retain 1A single chamber alternating R/L duties and 1B two dedicated ventricular chambers | User's latest instruction and sketch | Both active; no winner selected |
| D015 | 2026-11-21 | Distinguish per-circuit pulse rate h from physical chamber rate f | One fill/eject cycle for each ventricular duty; f=2h for 1A and f=h per chamber for 1B | Explicit accounting assumption; revisit if topology or pulse definition changes |
| D016 | 2026-11-21 | Use operating-case budgets and evidence gates before weighted scoring | Hydraulic feasibility and measurable EVAR boundary conditions must be established | Working comparison framework; no invented weights or scores |
| D017 | 2026-11-21 | Preserve the sketch unmodified and distinguish its interpretation from a dimensioned design | Right edge of supplied image is cropped | Recorded in references/ |
| D018 | 2026-11-21 | Keep pulmonary/systemic pressure loads and pump/phantom measurement planes distinct | Current PDS pp. 1/5; anatomical-plane specificity supported by Les et al. | Inputs to next model extension; no new hydraulic simulation |

The existing fixed-stroke and independent-flow options remain open. No new
stroke, valve arrangement, phase offset, gas amount or cylinder has been
selected. The matrix gives proposed cases for review, not an assertion that
all listed points must be achieved by one fixed-stroke configuration.

## Waveform joining — 22 November 2026

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D019 | 2026-11-22 | Retain published harmonic and half-sine pairs with independent shape/timing controls | User accepted continuation of waveform study | Implemented as kinematic candidates |
| D020 | 2026-11-22 | Interpret fallback 60:40 as filling:ejection, gamma = 0.4 | Stated interpretation of user fallback | Adjustable assumption |
| D021 | 2026-11-22 | Compare a normalised quintic endpoint window, trial width 5% of each phase at each end | Engineering means of removing acceleration jumps | Comparison only; peak acceleration penalty prevents treating smoothness as automatic improvement |
| D022 | 2026-11-22 | Add the waveform build to the existing spreadsheet without coupling it to the local pressure example | Staged transparent derivation | Volume, joins, derivatives, quadrature and input responses checked; hydraulic feasibility pending |


## Pressure comparison and evidence boundaries — 22 November 2026

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D023 | 2026-11-22 | Compare chamber, arterial and phantom measurements with their corresponding physiological locations | User requests heart waveform comparison; pressures differ across valves and circuit segments | Applied; quantitative reference currently arterial only |
| D024 | 2026-11-22 | Preserve Qureshi/Milnor reference at 75/min and 6.6 L/min | Published ten-harmonic functional reference; no raw clinical acquisition inspected | Reconstructed; different flow prevents a validation-error claim |
| D025 | 2026-11-22 | Add periodic three-element load as an external interface | Pressure must respond to flow and load; Windkessel hardware is outside pump scope | Implemented for prescribed flow; load parameters provisional |
| D026 | 2026-11-22 | Report phase-only forces and closed-valve conflicts explicitly | Pulmonary phase assumption fails; both sides have unresolved pressure joins | No force rating selected; gas/storage and valve events are next |
| D027 | 2026-11-22 | Treat mean-pressure agreement from chosen resistance as imposed, not independent corroboration | Periodic balance fixes mean pressure from mean flow and total resistance | No fitting or physical validation claimed |


## Interactive MATLAB model destination — 22 November 2026

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D028 | 2026-11-22 | Aim for synchronised piston motion, pressure and flow waveforms with adjustable bpm; MATLAB is the preferred likely platform | User reports MATLAB installed locally on Ubuntu | Goal recorded; installed release/toolboxes and execution unverified; qualifies D011's earlier platform direction |
| D029 | 2026-11-22 | Preserve executed Python results as the numerical reference during MATLAB development | Reproducibility and comparison during implementation change | Existing solver and results unchanged; earlier MATLAB port remains unexecuted |
| D030 | 2026-11-22 | Propose fixed-geometry bpm exploration as the first interactive mode, with sizing and independent-flow control clearly distinguished | User's fixed-stroke pump assumption; flow-frequency-volume conservation | Proposed interface behaviour; no geometry or controller selected |
| D031 | 2026-11-22 | Develop the numerical model independently of display and later hardware communication | Plot refresh must not determine integration accuracy; physical rig connection has additional requirements | Proposed architecture in LIVE_MODEL_TARGET.md; UI and hardware integration not implemented |


## Derivation before the application — 22 November 2026

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D032 | 2026-11-22 | Complete the required coupled derivation before developing the interactive MATLAB interface | User's explicit sequencing clarification | Active priority; application remains eventual deliverable |
| D033 | 2026-11-22 | Derive a fixed-mass polytropic air pocket and pressure-opening/flow-closure passive-valve baseline coupled to the external load | User's retained-air direction; continuity and inertial branch laws; passive switching was an assistant assumption | Gas/storage derivation retained; passive design assumption superseded by D034; combined solver not executed |

## Enforced valve states and assignments — 22 November 2026

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D034 | 2026-11-22 | Valve states are enforced in both architectures; a purely passive switch law does not capture the intended coordination | Explicit user correction, subsequently clarified in D037 | Confirmed; piston position/phase participates and pressure may enter the command rule; timing and closure dynamics remain open |
| D035 | 2026-11-22 | In 1A the common inlet/outlet serve right or left duty sequentially; in 1B tricuspid/mitral are dedicated ventricular inlets and pulmonic/aortic are dedicated outlets | User's assignment clarification and earlier sketch | Confirmed functional map; physical selectors, valve count and transition connections remain open |
| D036 | 2026-11-22 | Retain earlier passive simulations and diagnostics with explicit scope; do not treat inlet/outlet naming as a one-way flow constraint | Preserve provenance and distinguish commands from hydraulics | Documentation corrected; no enforced-valve numerical result or full-cycle force rating claimed |

Details: [enforced valve control and routing](research/VALVE_CONTROL_AND_ROUTING.md).

## Piston phase and pressure coordination — 22 November 2026

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D037 | 2026-11-22 | Piston position/phase participates in cardiac valve coordination; pressure may also govern enforced commands | User clarifies that cardiac valve names express intended behaviour and that pressure linkage remains possible | Confirmed intent; phase-only versus phase-plus-pressure law, thresholds and paired-command rule remain unselected |

The earlier wording excluding pressure thresholds from commands was too
restrictive. The revised [valve note](research/VALVE_CONTROL_AND_ROUTING.md)
provides a general dependency and a proposed four-phase sequence for discussion.
No numerical model or controller has been implemented in this update.

## Candidate valve sequence derivation — 22 November 2026

| ID | Date | Decision / proposal | Basis | Status |
| --- | --- | --- | --- | --- |
| D038 | 2026-11-22 | Derive selectable phase-only and phase-plus-pressure opening with latched commands and scheduled finite closure | User directs continuation of the piston/valve derivation | Candidate for review in Derivation 05; no numerical thresholds, timing values or hardware selected |
| D039 | 2026-11-22 | Preserve paired commands in 1B and separate duty routing in 1A; propose both-ready pressure guards for the pair | Earlier linked-state intent and circuit assignments | Common guard proposed; detailed closure is deferred by D041. A true switching-inclusive maximum force remains unresolved |


## Adjustable duties and ideal transitions — 22 November 2026

| ID | Date | Decision | Basis | Status |
| --- | --- | --- | --- | --- |
| D040 | 2026-11-22 | Make the shared-chamber right-duty fraction adjustable; retain 0.5 initially | Explicit user clarification that R/L duties need not occupy equal time | Budget generator exposes --right-duty-fraction; separate duty budgets verified. Coupled piecewise hydraulic model not implemented |
| D041 | 2026-11-22 | Idealise opening/closing transitions for now and refine once a valve is selected | Explicit user staging instruction | Ideal switch a=u with zero transition duration is the documented baseline; no division by zero in the finite-ramp formula, no silent removal of fluid inertia, and no switching-surge force rating |

See [duty allocation and ideal valves](research/DUTY_ALLOCATION_AND_IDEAL_VALVES.md).
