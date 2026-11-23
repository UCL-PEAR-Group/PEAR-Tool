# Piston pump team report

`Piston_Pump_Team_Report.pdf` consolidates the team summary, unranked advantages and limitations, all three supplied concept images, enlarged sketch excerpts, derivations to date, existing plots, implementation status and gated roadmap.

The editable source is `Piston_Pump_Team_Report.tex`; all figure dependencies are in `assets/`. Images are preserved in their original bytes. Enlarged excerpts use LaTeX clipping for layout; the complete original sheet is also included.

Build from this folder with a working local LaTeX installation:

```bash
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error Piston_Pump_Team_Report.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error Piston_Pump_Team_Report.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error Piston_Pump_Team_Report.tex
```

Three passes stabilise the contents and references. The delivered PDF was compiled locally using pdfTeX; no remote compiler was used. Temporary build files and page renders are not repository deliverables.

## Scope

This report consolidates existing work. It does not implement the new enforced-valve solver, run a new hydraulic simulation, select an architecture or establish a maximum drive-force rating. Current rear-pressure/effective-area and valve/timing decisions take precedence over older assumptions. Passive-check and constant-boundary outputs are explicitly historical comparisons. MATLAB runtime execution and physical validation remain unperformed.

## Provenance

- `early_pump_schematic.png`: supplied `image(20261121-112131).png`.
- `early_opposed_sketch.jpeg`: supplied `clipboard_2026-11-21_11-24.jpeg`.
- `concept_development.jpeg`: existing `references/concept_sketch_2026-11-21.jpeg`, originally supplied as `clipboard_2026-11-21_19-06.jpeg`.
- Plot images: unchanged copies of existing research/archive outputs; `report_verification.json` records their hashes and report checks.
- Main derivation sources: `MODEL.md`, `archive/pump_coupled_model/Pump_coupled_model.tex`, research Derivations 01–05, waveform candidates, duty-allocation note and `MODEL_CHECKPOINT.md`.
- Reviewed source branch head: `b5c1c42ccc11ed548dca2c163450246532ae94f3`.

The original early schematic's external authorship is not established; it is credited as an image supplied in the conversation. No missing portion of the cropped concept sheet is reconstructed.
