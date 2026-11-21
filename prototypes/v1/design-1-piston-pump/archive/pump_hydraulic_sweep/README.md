# MECH0073 piston hydraulic-force sweep

First exploratory numerical sweep, prepared 21 November 2026. No measured data
or experimental calibration are included. Read `Hydraulic_force_sweep.pdf`
before interpreting the numerical results as design loads.

## Scope and assumptions

The model follows one prescribed plunger-volume trajectory, one retained gas
pocket, two ideal passive check valves, two lumped fluid-inertance/loss legs,
and constant upstream/downstream pressure reservoirs. It reports pressure
force on a flat piston face with atmospheric pressure behind it. Seal friction,
moving-solid inertia, mechanism loads and motor limitations are excluded.

The baseline geometric displacement is 66.6667 mL per event, derived from the
user's ideal reference of 5 L/min at 75 events/min. A 50 mm face diameter gives
33.95 mm travel. These are illustrative dimensions, not a selected cylinder.
The sweep keeps geometric displacement fixed, so it does not enforce 5 L/min
at every frequency. Diameter plots rescale force and travel at fixed volume
history; they are not independent cylinder simulations.

Baseline pressures are inlet 10 and outlet 90 mmHg gauge. Reference air volume
is 10 mL at 10 mmHg gauge; atmospheric pressure is assumed 760 mmHg. Other
assumptions are recorded in every CSV case row and explained in the report.
All pressures in CSVs are gauge unless the name explicitly says `abs`.

The motion is smooth quintic advance over 40% of the period and return over
60%. The valve inlet and outlet bores are varied together. Air-volume,
outlet-load, gas-exponent, discharge-coefficient and timing sensitivities are
included, but the sweep is not a full factorial search or a proven maximum
over all possible operating conditions.

## Files

- `Hydraulic_force_sweep.pdf`: LaTeX-generated report with assumptions,
  plots, equations, evidence and numerical verification.
- `Hydraulic_force_trends.png`: frequency, valve bore, piston diameter and
  mean-delivery trends.
- `Hydraulic_force_waveforms.png`: signed forces over a periodic cycle and
  sensitivity to retained gas volume. Vertical scales differ between panels.
- `case_results.csv`: all 118 dynamic cases, including the stopped case.
- `full_fill_reference.csv`: 28 separate, imposed-full-fill algebraic cases.
- `selected_cases.csv`: eight baseline cases used in the report table.
- `waveforms.json`: final periodic-cycle traces for three illustrative cases.
- `verification.json`, `additional_verification.json`: coarse/refined runs.
- `test_*.json`: initial representative runs with their full-cycle traces.
- `environment.json`: software versions used to generate the results.
- `hydraulic_sweep.py`, `make_outputs.py`, `make_report.py`,
  `verify_additional.py`: reproducible calculation and presentation scripts.
- `Hydraulic_force_sweep.tex`: report source.

## Reproduce

Python dependencies: NumPy, pandas, SciPy and Matplotlib. Exact installed
versions are in `environment.json`. Use a normal pdfLaTeX installation to
compile the report; no unusual local runtime configuration is required.

```sh
python hydraulic_sweep.py --test
python hydraulic_sweep.py --sweep
python verify_additional.py
python make_outputs.py
python make_report.py
pdflatex Hydraulic_force_sweep.tex
pdflatex Hydraulic_force_sweep.tex
```

Scripts write regenerated files beside themselves. Preserve a copy of the
provided results if comparing modifications. Edit the `Case` defaults and
the `sweep()` case list to explore new inputs; regenerate all dependent files
after changes. Narrative values in `make_report.py` describe this specific
run and must be reviewed if inputs change.

## Result columns

- `force_peak_N`: largest positive pressure force during the sampled cycle.
- `force_min_N`: most negative signed pressure force.
- `force_absmax_N`: maximum absolute pressure force, the plotted maximum.
- `pc_peak_mmhg`, `pc_min_mmhg`: chamber pressure extrema, not reservoir
  pressure extrema.
- `Q_Lmin`: cycle-mean outlet flow.
- `delivered_ml`, `inlet_ml`: net outlet/inlet volumes integrated over the
  final cycle.
- `eta`: net-delivery/swept-volume ratio. It can exceed one in this ideal
  inertial valve model and is not a calibrated efficiency bounded by one.
- `fill_deficit_ml`: full-retraction liquid deficit relative to the liquid
  inventory at the reference inlet pressure. This is distinct from a
  delivered-volume shortfall.
- `balance_error_ml`: largest chamber-volume balance residual over the cycle.
- `net_cycle_error_ml`: absolute difference between inlet and outlet cycle
  volumes, which should approach zero at periodic operation.
- `periodic_residual`: largest endpoint state difference scaled as specified
  in `simulate()`. It is a numerical convergence measure.
- `status`: `periodic` or a guard/failure status. The one stopped case has no
  fabricated periodic force or flow result.

## Limits

117 dynamic cases reached periodic operation; one hit an exploratory lower
absolute-pressure guard. The 50 mmHg absolute floor is not a measured
cavitation threshold. Passing it does not establish cavitation-free operation,
especially at local valve restrictions. A liquid-inventory floor of 0.1 mL
is also implemented. The gas-free reference uses a separate pressure screen.

Constant reservoir pressures exclude reservoir depletion and whole-loop
recirculation limitations. No actual Windkessel dynamics, left/right circuit
balance, BMF viscosity calibration, distributed pressure waves or finite
valve leaflet dynamics are included. Three refinement checks verify numerical
stability of representative outputs, not physical validity.

The largest case in this sweep is about 1275 N at 180/min with 8 mm valves
and a 30% advance fraction. Its implied internal pressure is far above the
outlet reference. This demanded load is not a recommended operating point,
component rating or universal maximum-force bound.
