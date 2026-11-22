# Design 1: Piston Pump

Waveform options: [published candidates, adjustable timing and comparison plots](research/WAVEFORM_CANDIDATES.md).

Latest step: [Derivation 02: volume-preserving waveform joining](research/DERIVATION_02_WAVEFORM_JOINING.md).
The workbook now includes a **Waveform** sheet with selectable shapes, endpoint
smoothing, flow, velocity, acceleration and position. The 5% smoothing trial
removes acceleration jumps but increases peak acceleration; it is not a selected
motor command. Run `python research/build_smooth_waveforms.py` to reproduce the
comparison and width sensitivity.

Continue the analytical development with
[Derivation 01: full-liquid chamber, pressure and force](research/DERIVATION_01_FULL_LIQUID.md).

Supporting sources: [cardiovascular piston-pump literature review](research/PISTON_PUMP_LITERATURE_REVIEW.md)
and [formula-driven pressure starter workbook](spreadsheet/Pump_pressure_literature_starter.xlsx).
The baseline is 5 L/min at 75 pulses/min per circuit. The workbook contains a
local open-valve calculation, not a completed dynamic model or maximum-force estimate.
See [spreadsheet scope and verification](spreadsheet/README.md).

Start with the [goal and concept comparison](GOAL_AND_CONCEPT_MATRIX.md) and
[operating-case matrix](OPERATING_MATRIX.md) ([CSV](OPERATING_MATRIX.csv)).
Both the single chamber with alternating duties (1A) and two dedicated
ventricular chambers (1B) remain under consideration.

Python is the primary model language. Continue with [MODEL.md](MODEL.md) and the
[variable register](VARIABLES.md) ([CSV](VARIABLES.csv)). Editable calculations
and plots are in [Pump_Model.ipynb](python/Pump_Model.ipynb). The notebook is
optional: every simulation can run through the command line.

## Run locally

From this directory, using Python 3.12:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python python/run_model.py check
python python/run_model.py baseline
```

The baseline writes `results/python/baseline.json` and `baseline.png`.
Those generated outputs are ignored by Git; the original archive is preserved.
To change an operating case, edit a JSON file containing `Case` fields:

```sh
python python/run_model.py baseline --config python/example_case.json
python python/run_model.py sweep
```

The sweep regenerates all 118 cases and the two trend figures in
`results/python/`. It does not alter the archive. The executed reference used
Python 3.12 and the versions pinned in `requirements.txt`; local installation
on the user's computer has not been performed by this task.

For the optional notebook, install the extra kernel dependencies and open it
in VS Code's Jupyter extension or another Jupyter frontend:

```sh
python -m pip install -r requirements-notebook.txt
```

Select the virtual environment's Python kernel. The notebook locates the model
from either its own directory, this design directory or the repository root.
It performs one new baseline simulation and plots its output; the archived
sweep is identified separately. All notebook code cells were executed sequentially in an in-process IPython
shell during this update. A separate Jupyter kernel could not bind sockets
in this environment, so frontend rendering remains unchecked. The committed
notebook has outputs cleared to keep code review clean.

To regenerate the architecture volume/timing budget (standard library only):

```sh
python python/build_operating_matrix.py
```

This does not run hydraulic simulations or modify the archived results.

## Files and model status

- `GOAL_AND_CONCEPT_MATRIX.md`: project goal, concept comparison and evidence gates.
- `OPERATING_MATRIX.md`, `OPERATING_MATRIX.csv`: 11 operating points × two
  architectures, with explicit per-circuit and physical-chamber frequencies.
- `references/`: unaltered user sketch and provenance.
- `python/`: active model, runner, plotting script, notebook and matrix/register generators.
- `VARIABLES.csv`: editable source of the variable register; run
  `python python/render_variables.py` to update `VARIABLES.md`.
- `MODEL.md`: maintained equations, input provenance, interpretation and choices.
- `DECISIONS.md`, `PROGRESS.md`: dated decisions and work status.
- `python/verification_status.json`: executed regression and notebook checks.
- `archive/`: unchanged earlier source, data, figures and LaTeX reports.
- `MANIFEST.sha256`: original archive hashes.
- `matlab/`: superseded experimental port, not the active implementation; it was
  never executed in MATLAB. It is retained as a record of the earlier choice.

The Python hydraulic equations and baseline parameters are unchanged from the
executed reference. Regression checks cover three representative cases,
conservation, motion endpoints and the expected low-pressure guard. These are
numerical checks, not calibration or independent physical validation. Actuator
loads, feedback control, bypass paths and the whole circulation remain outside
the present solver.
