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
