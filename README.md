# yarnlog

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
pytest --cov=yarnlog --cov-report html:htmlcov tests
```
