# Model checkpoint report

- `Pump_Model_Checkpoint.pdf`: consolidated status, equations, assumptions, rear-pressure correction and staged next steps.
- `Pump_Model_Checkpoint.tex`: editable LaTeX source.
- `rear_boundary_algebra_checks.json`: synthetic algebra checks; not a pump simulation or physical validation.

Build with a working TeX installation, for example:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=reports/checkpoint reports/checkpoint/Pump_Model_Checkpoint.tex
```

Run from the design directory. The report was generated locally with pdfTeX/LaTeX, without a remote compiler. Stored
numerical verification reports were inspected; historical simulations were not
rerun for the checkpoint. Old outputs retain their original assumptions.
