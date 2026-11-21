# Design 1: Piston Pump

Python is the primary model language. Start with [MODEL.md](MODEL.md) and the
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

## Files and model status

- `python/`: active model, runner, plotting script, notebook and CSV renderer.
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
