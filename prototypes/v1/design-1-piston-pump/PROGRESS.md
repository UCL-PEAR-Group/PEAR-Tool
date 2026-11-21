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

## Pending verification

- Run `verify_reference` in MATLAB and record the release and output.
- Open and run `Pump_Model_Live.m` in MATLAB's Live Editor; inspect plots and
  table rendering. A source-only syntax check is not a substitute for this.
- Rerun the full MATLAB sweep and compare statuses and outputs with the archive.
- Calibrate hydraulic coefficients using selected components and fluid data.
- Independently validate the assembled physical model against measurements.

## Open design decisions

- Which combinations within 2–7 L/min and 40–180/min are required?
- Must fixed travel be retained when selecting mean flow independently?
- If so, compare bypass/diversion with actively timed spill; no choice yet.
- Determine gas reference amount, real valve characteristics, line geometry
  and representative Windkessel boundary histories.

Keep completed numerical verification, calibration and independent validation
as separate entries. Do not mark MATLAB execution complete on the basis of
the Python results or syntax parsing.
