# Design 1: Piston Pump

Start with [MODEL.md](MODEL.md), the maintained calculation and decision
record. It links the archived calculations and explains fixed-stroke flow
control. The MATLAB entry point is [Pump_Model_Live.m](matlab/Pump_Model_Live.m).

## What is available

- `MODEL.md`: readable model definition, input provenance, equations, results,
  decisions and remaining questions.
- `matlab/`: MATLAB functions, a plain-text Live Script and a regression check
  against the executed Python reference results.
- `archive/pump_hydraulic_sweep/`: the original 118-case calculation, CSV/JSON
  outputs, plots, verification records and LaTeX report.
- `archive/pump_coupled_model/`: earlier coupled-model derivation and source.
- `archive/pump_tradeoffs/`: initial geometry/displacement trade-off plots.
- `DECISIONS.md` and `PROGRESS.md`: dated decisions and work status.
- `MANIFEST.sha256`: hashes of the preserved source/data/report archive.

## MATLAB use

Open `matlab/Pump_Model_Live.m` in MATLAB R2025a or newer for the plain-text
Live Editor format. The computational functions use standard MATLAB; no
Simulink or Simscape toolbox is required. On older releases, the text markup
appears as comments and the code can be run as a script (plotting requires
`tiledlayout`, introduced in R2019b).

From the `matlab` directory, first run:

```matlab
verify_reference
Pump_Model_Live
% Optional full rerun; saves to ../results/matlab without overwriting archive:
run_sweep
```

**Execution status:** the archived results were executed in Python. The MATLAB
port has not been run in MATLAB in the preparation environment, because no
MATLAB runtime was available. `verify_reference` must pass before MATLAB
outputs replace the reference results. Syntax checks are not runtime
verification, and agreement between implementations is not physical validation.

Only the small, current model is migrated. No actuator, controller, bypass
valve or whole-circulation model is claimed to be implemented. The fixed-stroke
control alternatives in `MODEL.md` remain open design choices.
