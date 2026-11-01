# Contributing to PEAR

## Everyday workflow
1. Create or select an issue with an owner and acceptance criteria.
2. Start a task branch from an up-to-date main.
3. Make a small, focused change.
4. Open a draft pull request early and identify affected files.
5. Run relevant checks and request an independent review.
6. Resolve feedback and merge using Squash and merge.
7. Start the next task on a fresh branch from main.

All pull requests must target UCL-PEAR-Group/PEAR-Tool, not the upstream repository.

## Branch names
Use <type>/<issue-number>-<short-description>.

Types: feat, fix, docs, test, refactor, chore, research.
Example: fix/42-correct-geometry-units.

The initial chore/repository-governance branch is a bootstrap exception.
Use task branches rather than permanent branches per person.
Do not delete branches without an agreed repository policy.

## Commit and pull request titles
Use <type>(<optional-scope>): <clear description>.

Example: fix(geometry): correct millimetre conversion

Keep commits focused. Do not mix scientific changes with unrelated formatting.
Review staged changes before committing.
Use the pull request description to explain the issue, approach and validation.
Link the issue with Closes #<number> only when its acceptance criteria are met.

## Avoiding conflicts
- Assign one lead contributor to each task branch.
- Coordinate before editing the same notebook, CAD file or shared configuration.
- Keep pull requests small and integrate completed work promptly.
- Do not resolve conflicts by blindly accepting an entire side.
- Ask the affected author when the intended behaviour is unclear.
- Never force-push or discard someone else's work.

## Repository layout
Keep existing analysis/ and app/ paths during initial setup.
Proposed additions:
- docs/: onboarding, architecture, decisions and experiment procedures.
- schemas/: versioned metadata and configuration contracts.
- tests/: focused regression tests and small synthetic fixtures.
- .github/: issue forms, pull request templates and automated workflows.

Create directories when they have a concrete purpose and content.
Review migrations separately from changes to scientific behaviour.

## Data and results
Preserve raw data and record where it is stored.
Do not commit large generated outputs by default.
Use manifests with stable identifiers, checksums, units and provenance.
Record the exact code revision and configuration for each experiment.
Keep calibration data distinguishable from independent validation data.
Do not upload identifiable patient data, credentials or confidential material.

## Review and merge
Main requires an independent approval and resolved review conversations.
Administrators follow the same protection rules.
Automated required checks will be configured after their workflows are verified.
Use squash merging to retain one clear main-branch commit per completed task.
Branch protection reduces mistakes but does not replace scientific review.

## Upstream
The previous group's repository is the upstream source.
Fetch updates when useful and integrate them through a dedicated reviewed PR.
Do not overwrite team work with an upstream synchronisation.
Preserve attribution and resolve inherited licensing before adding a licence.

## Task tracking
Use GitHub issues as the work records and GitHub Projects as their views.
Keep Status separate from Zone:
- Status: Not started, In progress, Blocked, Done.
- Zone: Urgent, To do, Rolling.

Record technical category, owner, priority, due/review date, dependencies,
next action, acceptance criteria and evidence links where applicable.
Do not invent owners or deadlines.
