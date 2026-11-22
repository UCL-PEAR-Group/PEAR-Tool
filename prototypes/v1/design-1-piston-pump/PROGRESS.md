# Progress and next checks

## Piston-phase and pressure coordination — 22 November 2026

- Corrected an overly restrictive interpretation: enforced valves can use
  pressure feedback, while piston position/phase participates in coordination.
- Preserved the cardiac functional assignments and both pump architectures.
- Added a general command-law dependency and proposed four-phase sequence for
  review. No timing, pressure threshold or controller has been selected.
- Distinguished position from cycle phase, commanded timing from physical
  transition duration, and prescribed piston motion from actual valve flow.
- Reviewed the Paeme et al. physiological valve model for context; it does not
  validate the proposed controller. Existing code and results are unchanged.

Next: agree how phase and optional pressure conditions govern transitions before
completing the control law and coupled derivation.

## Enforced valve correction — 22 November 2026

- Recorded the user's correction: valve states are enforced in both concepts.
- Mapped the single chamber's sequential circuit assignments and the two
  chambers' dedicated tricuspid/mitral inlets and pulmonic/aortic outlets.
- Retained gas/storage conservation while superseding the passive design law.
- Distinguished requested state, effective opening and signed hydraulic flow;
  exact command timing, selectors and finite closure law remain unresolved.
- Marked earlier passive simulations and spreadsheet diagnostics as comparison
  cases. Numerical outputs and executable model code are unchanged.

Next: derive the commanded phase sequence and transition response before any
new coupled simulation or maximum-force claim. See
[valve control and routing](research/VALVE_CONTROL_AND_ROUTING.md).

## Retained-air and valve-event derivation — 22 November 2026

- Confirmed that the eventual MATLAB interface follows the coupled derivation.
- Derived chamber continuity with a fixed-mass polytropic gas pocket, its
  pressure-dependent compliance and continuous pressure through piston reversal.
- Specified an ideal passive-valve event law consistent with fluid inertance;
  pressure reversal alone does not instantly close an already flowing branch.
- Combined the chamber and three-element arterial load into four hydraulic state
  equations with discrete valve states, explicit inventory and periodicity checks.
- Checked dimensions, signs, the closed-valve limit and a small analytical opening
  budget. The earlier illustrative gas state gives about 0.791 mL compression
  displacement before opening against a constant 90 mmHg gauge outlet. This is
  not net stroke loss or a simulated cycle.
- Existing solvers, spreadsheet results and waveform comparisons are unchanged.
  No new coupled numerical result, MATLAB execution or maximum force is claimed.

Next: review the gas/reference-state and valve assumptions, then implement and
verify the coupled equations before interpreting new pressure/flow/force curves.


## Pressure histories and physiological reference — 22 November 2026

- Reconstructed the ten-harmonic aortic and main pulmonary arterial signals in
  Qureshi et al. (2018), Appendix A Table A1, reproduced from Milnor (1989).
  Kept their original 75/min and 6.6 L/min conditions; no fitted waveform error
  or independent physiological corroboration is claimed for our 5 L/min trial.
- Added a periodic three-element load interface, conditional inlet/outlet phase
  pressures and hydraulic forces, and checks on assumed-closed passive valves.
- Added editable systemic/pulmonary presets, linked formulas and two native
  comparison charts in the new Pressure cycle workbook sheet.
- With the stated trial loads, arterial ranges are 72.6–106.0 mmHg systemic and
  10.8–21.0 mmHg pulmonary. Means of 90 and 15 mmHg follow from chosen resistances.
- Chamber minima of −34.5 and −39.5 mmHg gauge, a pulmonary closed-valve conflict
  over about 13.4% of the cycle, and unresolved pressure joins limit interpretation.
  Phase-only force maxima of 32.6 and 15.5 N are not complete-cycle force ratings.
- Checked cycle volumes, periodicity, constant-flow limit, load energy balance,
  grid refinement, parameter responses and workbook formulas. Reference data,
  trial inputs and numerical reports are retained for reproduction.
- Excel/LibreOffice execution, component calibration and independent physical
  validation remain unperformed. The earlier gas solver is unchanged.

Next: resolve chamber storage and valve transitions with the proposed retained
sealed gas pocket, then reassess filling pressures and complete-cycle force.
Ventricular pressure rise/relaxation and arterial pressure are separate targets.

## Waveform joining and editable spreadsheet — 22 November 2026

- Added a volume-preserving endpoint window to the published harmonic and
  half-sine candidates, with configurable width, rate, flow, timing and diameter.
- Checked phase volumes, return position, both acceleration joins, analytic
  derivatives and integration refinement. Recorded width sensitivity and
  preserved the earlier unsmoothed comparison.
- The 5% trial changes harmonic flow peaks by about 0.4% and 1.0%, but raises
  peak piston acceleration from 2.845 to 5.026 m/s² at the illustrative 50 mm
  diameter. No width or final waveform is selected.
- Extended the workbook with formula-driven shape selection, endpoint smoothing,
  kinematics and two native scatter charts against physical cycle time.
- Compared baseline outputs to Python, changed shape/width/rate/timing inputs,
  restored the baseline and found no formula errors. The sampled spreadsheet
  acceleration maximum is 5.018 m/s², 0.15% below the fine-grid reference.
- Pressure/gas coupling, actual valve feasibility and a new maximum-force result
  remain pending. Native Excel/LibreOffice and physical validation are unperformed.

Next: derive the pressure history for a chosen full-liquid waveform and check
the assumed valve states before interpreting the maximum hydraulic force.

## Existing waveforms compared — 22 November 2026

- Inspected Franzetti's published half-sine, Swanson–Clark and Talukder–Reul
  expressions. Located primary implementation examples and alternative peak-time
  and three-segment volume-waveform studies.
- Added a reproducible shape comparison at 5 L/min and 75/min, interpreting the
  60:40 fallback as filling:ejection. Included the existing quintic motion as an
  explicitly non-physiological engineering reference.
- Verified phase integrals, endpoint volumes, positive forward phase flow and
  acceleration-join differences. Harmonic pairs need join matching before use as
  motor commands. No hydraulic simulation or workbook change was performed.

Next: compare ratio/shape changes separately, then check valve-state feasibility
and pressure/force histories under the same specified load.

## Full-liquid analytical derivation — 21 November 2026

- Derived moving-chamber continuity, the open-path pressure law, and separate
  filling/ejection pressure expressions with consistent units and signs.
- Combined ejection motion and pressure into an explicit hydraulic-force
  expression. Identified limits when valve-state assumptions fail or both valves
  close; retained gas and finite compliance remain subsequent stages.
- Recorded the supplied Windkessel interface without selecting hardware or a
  new waveform. The 5 L/min, 75/min target remains fixed for the first case.
- Checked dimensions, phase signs and limiting behaviour analytically. No new
  simulation, workbook change, calibration or physical validation was performed.

Next derivation input: ejection/filling timing and a smooth waveform with the
required 66.67 mL delivery integral, followed by valve-state consistency checks.

## Literature-led pressure derivation started — 21 November 2026

- User selected 5 L/min and 75 pulses/min as the first operating point and a
  spreadsheet for transparent analytical prototyping.
- Reviewed the supplied Franzetti paper/thesis, the requested Mazhar review,
  and primary content for eleven additional papers. Recorded access limitations,
  pump purpose and platform overlap in a fourteen-entry register.
- Added a pressure-model equation map, distinguishing local algebra from
  unimplemented dynamic gas, valve, reservoir and Windkessel coupling.
- Created a three-sheet formula workbook with 43 formulas, two diameter charts,
  editable inputs, source register and calculation limitations.
- Checked baseline values independently, three input perturbations, absence of
  formula errors, exported formula/chart presence and rendered all sheets.
- Verified the apparent missing 1/3 in thesis printed Eq 2.5 by direct integration
  and the straight-pipe limit. Original thesis simulation code was not inspected.
- Existing Python simulations and archive were not changed or rerun. Maximum
  force, full-cycle spreadsheet dynamics, native Excel testing and physical
  calibration/validation remain outstanding.

Next: agree the first chamber control volume, pressure measurement locations and
valve/line pressure law, then derive the full-liquid time history before gas.

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
