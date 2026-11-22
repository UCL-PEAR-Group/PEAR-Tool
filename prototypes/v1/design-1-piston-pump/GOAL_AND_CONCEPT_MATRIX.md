# Pump goal and concept comparison

Working record · updated 22 November 2026 · both concepts remain under consideration.

Both concepts use **enforced valve states coordinated with piston position/phase**.
Pressure may also participate in the command rule; that choice remains open. See
[valve control and routing](research/VALVE_CONTROL_AND_ROUTING.md) for the port
assignments, command/state distinction and unresolved transition timing.

## Goal and scope

**Develop a controllable, repeatable pump that supplies the specified flow and
pressure waveforms to the EVAR benchtop circuit, so physical measurements can
be compared with a digital model under known loading conditions.**

The immediate modelling goal is to identify feasible combinations of chamber
geometry, net delivered volume, pulse frequency, valve dimensions and pressure
loading, and estimate the associated peak hydraulic plunger force. This should
support cylinder and flow-path selection before designing the converter.

We are comparing two ways to provide the right- and left-ventricular pumping
functions. Anatomical resemblance is useful where it improves the required
hydraulic behaviour; it is not a substitute for measured performance. The
Windkessels, reservoirs, phantom, fluid and sensors form the load and measurement
interfaces. Their detailed design remains outside this pump workstream.

The wider project concerns EVAR outcomes, but this stage establishes hydraulic
boundary conditions and pump capability. It does not yet predict graft sealing,
deployment geometry or clinical outcomes. Bench agreement must not be presented
as clinical predictive validity.

## Interactive model destination — 22 November 2026

The user now aims for a live model showing piston motion and pressure/flow
waveforms at different bpm, most likely in MATLAB following local installation
on Ubuntu. [LIVE_MODEL_TARGET.md](LIVE_MODEL_TARGET.md) defines the proposed
outputs, operating modes and development sequence. The fixed-pump mode holds
diameter and stroke constant while calculating the resulting flow and pressure.
A separate sizing mode can vary travel to meet a flow target.

This is a software destination alongside the pump design goal above. MATLAB
execution, a complete coupled pressure cycle and the interactive interface have
not yet been demonstrated. The earlier Python work remains the numerical
reference. Both physical architectures remain open.

## Interpretation of the supplied sketch

- **1A — single chamber, alternating ventricular duties:** one flat-face
  plunger chamber fills from the right-atrial reservoir and ejects towards the
  pulmonary circuit in state R. In state L it fills from the pulmonary-return /
  left-atrial reservoir and ejects towards the systemic circuit. Each duty has
  its own filling and ejection event. Selectors connect the appropriate paths;
  the physical valve arrangement and switching sequence remain to be designed.
- **1B — two ventricular chambers:** the two distinct chambers in the lower
  drawing represent the right and left ventricles, each with an inlet and an
  outlet. The reservoir/circuit connections remain dedicated. Their motion may
  be synchronised or given a selected phase offset; no mechanism is selected.
- The uploaded image is cropped at the right edge. No dimensions or topology
  are inferred from its unseen portions. In particular, 1B is not interpreted
  as a single moving separator forcing two opposing spaces to alternate.
- Both concepts retain the flat wetted face, fixed travel within a selected
  configuration and negligible leakage assumption. Both the fully liquid-filled
  reference and retained-gas model remain relevant.

Source: [unaltered user sketch](references/concept_sketch_2026-11-21.jpeg).

## What success means

These are project requirements or proposed comparison metrics, not results.
The numerical targets below are transcribed from `PDS_Pump.pdf`, pp. 1 and 5,
last modified 19 November 2026. The user's 75 bpm nominal point overrides the
PDS's earlier nominal 70 bpm. The PDS requires compatible combinations, not
every possible point in a rectangular flow/rate/load range.

| Objective | Target / comparison metric | Measurement or model output | Status |
| --- | --- | --- | --- |
| Mean circulation flow | 5 L/min nominal; selected points within 2–7 L/min; ±2% tracking | Signed outlet-flow integral over complete cycles, at declared ports | PDS requirement; hardware unverified |
| Pulse rate and delivery volume | 75 bpm nominal; selected points from 40–180 bpm, including 100 and 120 | Pulses per minute at each circuit outlet; mL delivered per pulse | PDS range; nominal from user |
| Systemic loading | Mean inlet 4–20 mmHg; mean outlet 60–120; nominal 10/90; selected outlet peaks approximately 120/160, intended upper peak 200 | Pressure at the specified inlet/outlet and phantom planes | All gauge; instantaneous traces still required |
| Pulmonary loading | Mean arterial cases 15, 25 and 35 mmHg | Pulmonary arterial pressure and flow | PDS cases; right-atrial preload and pulmonary peak still to be specified |
| Waveform fidelity | Shape, amplitude, phase, time to peak and intended reversal | Synchronous pressure and signed-flow histories at both arterial outlets and phantom inlet | Reference traces and numerical waveform tolerances remain open |
| Pressure tracking / repeatability | ±2% non-zero mean inlet; ±3% systemic systolic, diastolic and mean; between-run systolic/diastolic CV ≤3%; within-duty CV ≤1.5% is an aim | Errors plus expanded measurement uncertainty; repeated independent runs | PDS allocations, not demonstrated capabilities |
| Stable circulation | No continuing drift of chamber/gas/reservoir states; balanced long-term delivery through both series limbs | Per-cycle volume balances and reservoir inventories | Conservation requirement; physical tolerances depend on measurement uncertainty |
| Hydraulic force demand | Peak positive/negative force and max absolute force for every admissible case | Chamber pressure relative to piston rear × face area | Calculated response; no force rating chosen |
| Practical implementation | Component availability, footprint, sealing, instrumentation, serviceability and cost | Evidence from actual candidate parts and layouts | Comparison criteria; no scores assigned |

Pump output and abdominal-phantom inlet flow must remain separate quantities.
Les et al. measured different flow magnitudes at supraceliac and infrarenal
planes in AAA patients [2]. Our implication is to specify the phantom's actual
anatomical plane and any branch-flow split before applying the whole-circuit
5 L/min reference directly to it. If all pump flow is deliberately routed through
an isolated phantom, record that as a bench configuration rather than assuming
it is a physiological infrarenal boundary condition.

## Concept comparison matrix

This is an evidence matrix, without arbitrary numerical weights or a declared
winner. Performance requirements act as gates before convenience or cost scores
can justify a selection. Both architectures need to be compared at the same
per-circuit pulse rate, flow target and load, not the same physical piston rate.

| Criterion | 1A: one chamber, alternating R/L | 1B: two dedicated ventricular chambers | Evidence needed for selection |
| --- | --- | --- | --- |
| Physical delivery-cycle rate | 2h cycles/min for h pulses/min in each circuit | h cycles/min per chamber; 2h events/min across both | Timing budget including filling, ejection, dwell and switching |
| Available time | R and L duties share each heart period | Each chamber has the whole heart period | Feasible motion and valve schedule under load |
| Right/left ejection phase | Direct chamber ejections cannot overlap; outlet buffering could modify observed pulse timing | Concurrent or offset motion possible, subject to mechanism/control | Required outlet-waveform phase and achievable flow histories |
| Unequal pulmonary/systemic loads | Same chamber experiences successive different boundaries; gas and residual liquid carry state between duties | Separate chamber states and pressure demands | Full-cycle pressure, volume and force histories |
| Valve routing | Enforced common inlet/outlet with sequential right/left circuit assignment; selectors and physical valve count unresolved | Enforced dedicated inlets: tricuspid/mitral; outlets: pulmonic/aortic | Port map and transition sequence; leakage, reverse flow and cross-connection behaviour |
| Valve linking | R/L duties are sequential; route selection is separate from inlet/outlet commands | Proposed paired inlet commands and paired outlet commands; precise inter-chamber timing remains open | Command sequence, effective opening/closure duration and loads; linked state does not imply equal flow |
| Filling and recirculation | Shorter allocated filling time per duty; shared residual inventory | More scheduling freedom; reservoir balance still necessary | Finite reservoir, inlet-loss and gas-state histories |
| Fixed-stroke mean-flow control | Routing between circuits does not itself set independently selectable mean flow | Two chambers do not themselves decouple flow from pulse rate | Chosen net-delivery method and calibrated volume per event |
| Hydraulic force | Determine maximum across R, L and switching transitions; cannot reuse a 180/min result for 360/min operation | Determine maximum for each chamber; a common drive can experience combined loads | Admissible-case simulations and measured pressure; converter mapping deferred |
| Manufacturing and maintenance | One chamber/seal, but extra routing hardware and actuation may offset savings | Two chambers/seals and dedicated paths | Component list, assembly access, sealing and cost evidence |
| Current model coverage | Chamber physics only; no state-switching or whole-loop solver | Chamber physics can be reused twice; no coupled two-chamber solver yet | New topology and conservation verification, followed by calibration and validation |

If truly simultaneous right/left chamber ejection becomes a hard requirement,
unbuffered 1A does not satisfy it. If measured outlet waveforms can meet the
requirements with sequential operation, 1A remains a candidate. No such decision
has been made here.

The equal-time calculation for 1A gives half a heart period to each duty. An
unequal allocation is possible: T_R + T_L + total switching/dwell time must fit
within 60/h seconds. Each duty must still deliver its required volume.

## Parameter trade-offs to investigate

| Variable | Quantity held fixed for comparison | Expected consequence from the model | What prevents choosing it independently |
| --- | --- | --- | --- |
| Face diameter D | Geometric swept volume Vs and pressure difference | Larger D shortens travel but raises pressure force because area increases | Chamber dimensions, force capacity and flow-path layout |
| Travel S | Vs | Longer travel permits smaller face area and lower pressure force at the same pressure | Motion speed/acceleration, sealing and available length |
| Inlet/outlet effective bore | Flow history and discharge coefficient | Larger area reduces the modelled valve loss; inlet and outlet should be varied separately | Real valve geometry, opening law, actuation/holding load, availability and dead volume |
| Frequency h | Net volume per circuit pulse | Mean flow increases in proportion to h | Filling time, pressure/force demand and selected PDS operating range |
| Net delivered volume | Mean flow Q | Required volume decreases as h increases | Fixed mechanical stroke needs an additional means of altering net delivery |
| Ejection-time allocation | Delivered volume per event | Shorter delivery time increases average flow during ejection | Valve loss, fluid acceleration, filling time and target waveform |
| Retained gas reference amount | Geometry, motion and boundary conditions | Changes compressive storage and valve timing | Effect on net flow and peak force is coupled; do not assume monotonic improvement |

These directions are conditional analytical trends, not measured component
performance. The previous bore sweep changed inlet and outlet together.

## Filling and maximum-force interpretation

The high-rate note on the sketch identifies a useful case to investigate.
Instantaneous inlet and outlet flows can differ as liquid is stored or released.
For the shared chamber, periodicity is checked after the complete R+L sequence,
not by forcing it to reset after each duty. At periodic operation the net storage
change over that full sequence is zero. Persistent average imbalance instead
causes inventory/pressure drift; an atrial reservoir only delays that drift.

Retain two modelling paths: (i) an ideal fully liquid-filled reference and
(ii) a known sealed gas amount with compressive storage and possible restricted
filling. In the second path do not independently impose both an arbitrary
filling fraction and gas-volume history: they must obey the chamber balance.
The gas amount is fixed; its instantaneous volume is not. No continuing ingestion
of air is implied by a retained sealed pocket.

The current force result is **hydraulic plunger load**, not total actuator load:
F_pressure(t) = face area × [chamber pressure(t) − rear pressure(t)].
Valve and line losses and fluid inertia contribute to chamber pressure. Seal
friction, moving-part inertia and converter force distribution remain excluded.
Outlet pressure alone is therefore insufficient to specify maximum force.
The PDS's 200 mmHg outlet peak is not an internal-chamber pressure rating.

## Next decision and staged work

1. Review [OPERATING_MATRIX.md](OPERATING_MATRIX.md): select the flow/rate pairs
   that each manufactured configuration must achieve. Keep both operating
   strategies open until this review.
2. Specify 1A's routing/timing and 1B's phase relationship; retain distinct
   pulmonary/systemic loads and agree reference measurement planes.
3. Extend the model only enough to compare those cases, including R/L gas-state
   carry-over for 1A and finite reservoir balance when assessing recirculation.
4. Sweep geometry, separate valve bores, gas amount and timing over feasible
   cases. Use force/waveform/filling results to shortlist cylinders and valves.
5. Calibrate selected component coefficients, then independently validate the
   assembled pump. Add mechanism design and a weighted selection matrix when
   evidence and priorities are sufficient to justify scores.

## Provenance and limits

1. Project PDS: [PDS_Pump.pdf](https://chatgpt.com/library?file_id=libfile_fde3_f-8b6f51e65a5c8191a703ee9bdf926031_874f2029a3688191a5c12d985d25d0fa&account_id=personal),
   pp. 1 and 5; current content read on 21 November 2026. Project requirements,
   not independently verified physiological measurements. Do not treat the
   entire PDS bibliography as independently checked by this update.
2. Les AS, Yeung JJ, Schultz GM, Herfkens RJ, Dalman RL, Taylor CA (2010).
   *Supraceliac and infrarenal aortic flow in patients with abdominal aortic
   aneurysms: mean flows, waveforms, and allometric scaling relationships.*
   Cardiovascular Engineering and Technology 1, 39–51.
   [DOI](https://doi.org/10.1007/s13239-010-0004-8),
   [PubMed](https://pubmed.ncbi.nlm.nih.gov/24324530/).
   Abstract and figure captions accessed; PMC full-text access was blocked in
   this session. Used only to support anatomical-plane specificity, not to
   prescribe a patient-specific waveform or validate this pump.
3. User instructions and sketch, 21 November 2026: two architectures, flat-face
   fixed-travel plunger, retained sealed gas, 5 L/min at 75 bpm nominal, staged
   model development and both frequency/flow strategies retained.
4. Frequency and volume relationships in the operating matrix are our explicit
   cycle-accounting calculations. They are not literature-derived test results.

No new hydraulic simulations, physical tests or component selection were
performed for this matrix update. The archived one-chamber results remain
unchanged; neither complete architecture has yet been validated.
