# yarnlog

[![Tests Status](https://github.com/attomos/yarnlog/workflows/Tests/badge.svg?branch=main&event=push)](https://github.com/attomos/yarnlog/actions?query=workflow%3ATests+branch%3Amain+event%3Apush)
[![codecov](https://codecov.io/gh/attomos/yarnlog/branch/main/graph/badge.svg?token=FQUPRYP17V)](https://codecov.io/gh/attomos/yarnlog)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yarnlog)](https://pypi.org/project/yarnlog)

Download Apache Hadoop YARN log to your local machine.

## Usage

```bash
$ yarnlog <YARN_URL>
```

## Dev

### Set up development environment

I use Poetry to manage dependencies

```bash
$ poetry install
$ source $(poetry env info --path)/bin/activate
```

### Debug yarnlog locally

```bash
$ poetry run yarnlog
```

### Run tests

```bash
$ pytest

# coverage
$ pytest --cov=yarnlog tests

# coverage with html report
$ pytest --cov=yarnlog --cov-report html:htmlcov tests
```
