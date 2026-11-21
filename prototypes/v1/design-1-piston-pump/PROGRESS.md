# Progress and next checks

## Completed — 21 November 2026

- Established prototype and Design 1 branch organisation.
- Preserved earlier trade-off plots, coupled derivation and the 118-case
  hydraulic sweep with its source, data and numerical refinement records.
- Added a maintained model document, parameter provenance and decision record.
- Prepared MATLAB parameter, motion, loss/inertance, gas-free reference,
  dynamic solver, sweep runner and regression-check functions.
- Added a plain-text Live Script for flow/bpm budgeting, geometry, reference
  plots and optional new MATLAB dynamic calculation.
- Explained compatible fixed-stroke operating points and candidate controls
  for independently selecting circuit flow and pulse frequency.

## Python restored as primary — 21 November 2026

- Latest user instruction supersedes the MATLAB migration.
- Added an active Python directory, local run commands, pinned dependencies,
  optional executable notebook and complete variable register.
- Executed three reference comparisons, conservation checks, motion endpoint
  checks and the expected low-pressure stop. Executed all notebook code cells in-process; frontend rendering unchecked.
- Physical equations and numerical defaults match the previous Python model.
- The original 118-case sweep was not repeated for this packaging-only change;
  original results remain available and the new runner can regenerate them.
- MATLAB source remains a superseded, unexecuted alternative.

## Pending calibration and validation
- Calibrate hydraulic coefficients using selected components and fluid data.
- Independently validate the assembled physical model against measurements.

## Open design decisions

- Which combinations within 2–7 L/min and 40–180/min are required?
- Must fixed travel be retained when selecting mean flow independently?
- If so, compare bypass/diversion with actively timed spill; no choice yet.
- Determine gas reference amount, real valve characteristics, line geometry
  and representative Windkessel boundary histories.

Keep completed numerical verification, calibration and independent validation
as separate entries. No physical calibration or independent validation has
been completed by the Python packaging and register update.


## Both piston architectures scoped — 21 November 2026

- Added a goal statement, measurable objectives, qualitative concept comparison,
  parameter trade-offs and staged decision gates in GOAL_AND_CONCEPT_MATRIX.md.
- Preserved the user's sketch and recorded the interpretation of 1A/1B.
- Added 11 candidate operating points for both architectures (22 CSV rows),
  generated reproducibly with Python and checked by volume/time accounting.
- Distinguished per-circuit pulse frequency from physical chamber cycle rate;
  identified 360 cycles/min for shared-chamber operation at 180 bpm per circuit.
- Read the current PDS, including separate pulmonary mean loads and open
  waveform requirements. Kept the user's 75 bpm nominal reference.
- Updated the variable register with architecture budgets and unimplemented
  routing/timing interfaces. No coupled chamber, switching or reservoir solver
  has been implemented. No hydraulic cases were rerun for this documentation
  and accounting update; previous numerical results remain unchanged.

Immediate next decision: select the compatible flow/rate/load combinations
and define the shared-chamber routing/timing alongside the dual-chamber phase
relationship. Then extend the hydraulic model only enough to assess those cases.
