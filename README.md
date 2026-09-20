# Reactive transport research program

A coordination layer for four independent publication repositories. Each paper
owns its manuscript, scientific code, notation, and verification evidence. This
repository owns portfolio metadata and a dashboard; it is not a paper monorepo.

## Audit and dashboard

```sh
git submodule update --init --recursive
python3 tools/portfolio.py audit
python3 tools/portfolio.py audit --root /path/to/local/paper-parent
python3 tools/portfolio.py build --output .agent-runtime/site
python3 -m unittest discover -s tests
```

The default audit reads committed project snapshots. `--root` reads manifests
and Git status from explicitly registered local paper directories without changing
them. Missing checkouts and unavailable checks remain visible. Output never
claims scientific validation from a tooling or website check.

See `workstreams.json` for acceptance gates, `ideas/README.md` for the idea backlog,
`decisions/` for scope decisions, and `archive.json` for preserved inactive projects.
