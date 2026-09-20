# Research program coordination

This repository indexes independent paper repositories. It owns priorities,
ideas, decisions, migration evidence, and a read-only portfolio dashboard.
Paper manuscripts, scientific implementations, and their authority remain local.

- Read `portfolio.json`, `workstreams.json`, and the relevant decision record.
- Audit only explicitly registered projects. Local paths are CLI arguments,
  never machine-specific tracked configuration.
- Audit commands must not modify paper repositories. Consumer changes require
  an explicit task and separate commits in each paper repository.
- Preserve the manuscript freeze declared by each project. Never run manuscript
  builds or generators as a side effect of an infrastructure audit.
- Report unavailable checks and distinguish infrastructure, implementation,
  analytical, convergence, finite-deformation, and physical evidence.
- Record sanitized decisions, not transcripts or credentials. No personal or
  confidential submission information belongs on the public dashboard.
- Use six-section process-log commits and exact shared-workflow pins.
- Apply `licensing-policy.json` when setting up or updating original project
  licensing: Apache-2.0 for code and CC BY 4.0 for manuscripts. This is the
  owner's standing choice; do not ask again unless an explicit exception is
  requested. Preserve third-party licenses and the manuscript-content freeze.
