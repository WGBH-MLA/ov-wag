# Maintenance

This page describes how to maintain the project. This includes [running scripts](#run-scripts), [creating lockfiles](#create-lockfiles), and [updating dependencies](#update-lockfiles).

## Install project

```bash
pdm install
```

## Run scripts

There are several scripts that can be run directly from the command line. They can be run by running:

```bash
pdm ov
```

## Create lockfiles

```bash
# dev
pdm lock -G dev,test,cli
# prod
pdm lock --prod -G production -L pdm-locks/pdm.prod.lock
# docs
pdm lock --no-default -G docs -L pdm-locks/pdm.doc.lock
```

## Update lockfiles

```bash
# dev
pdm update -G dev,test,cli --unconstrained --save-compatible --no-self
# prod
pdm update --prod -G production -L pdm-locks/pdm.prod.lock --unconstrained --save-compatible --no-self
# docs
pdm update --no-default -G docs -L pdm-locks/pdm.doc.lock --unconstrained --save-compatible --no-self
```

## Run tests

```bash
pytest
```

## Serve docs

Use the project script shortcut:

```bash
ov-docs
```

Or pass custom arguments to the underlying command:

```bash
mkdocs serve [args]
```
