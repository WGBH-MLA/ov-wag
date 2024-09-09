# PDM

Package management scripts for ov-wag

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
