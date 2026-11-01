# Agent instructions

## Scope
This repository supports the UCL MECH0073 PEAR student project.
Treat inherited code and results as historical evidence, not validated truth.
Follow more specific instructions in subdirectories where applicable.
Explicit user instructions take precedence over these project conventions.

## Before changing files
- Read CONTRIBUTING.md and relevant documentation.
- Inspect git status, the current branch, remotes and the task requirements.
- Work on a task branch, never directly on main.
- Preserve existing uncommitted work. Do not reset, clean or overwrite it.
- Identify the intended behaviour and acceptance criteria.
- Inspect dependencies and callers before changing interfaces or file paths.

## Changes
- Keep each change focused on one issue.
- Preserve the inherited analysis/ and app/ layout until a migration is reviewed.
- Avoid unrelated formatting, dependency updates or generated-file changes.
- Do not delete branches, rewrite published history or force-push.
- Do not push changes to fidhalkotta/PEAR-Tool.
- Do not merge pull requests without an explicit instruction.
- Never add credentials, confidential information or identifiable patient data.
- Do not assign a new licence to inherited work without resolving permissions.

## Scientific reproducibility
- Preserve raw observations; derive processed outputs through reproducible steps.
- Record units, coordinate systems, conditions, provenance and uncertainty.
- Record code revision, configuration, input identifiers and software versions.
- Label synthetic data and inherited results explicitly.
- Separate numerical verification, calibration and independent validation.
- Do not describe bench agreement as clinical predictive validity.
- Document assumptions and the limits of any result.

## Validation
- Run checks relevant to the changed behaviour.
- Add regression tests for meaningful bug fixes where practical.
- Check dimensions, plausibility and conservation where relevant.
- Validate schema changes with valid and invalid examples.
- Never claim a check passed unless it actually ran successfully.
- Report unavailable dependencies and checks that could not be run.

## Delivery
- Review the diff and stage only intended files.
- Use a clear commit message and link the issue in the pull request.
- Target UCL-PEAR-Group/PEAR-Tool:main.
- Explain the problem, change, validation and remaining limitations.
- Keep documentation consistent with the implemented behaviour.
- Treat this file as guidance; GitHub protections and required checks enforce policy.
