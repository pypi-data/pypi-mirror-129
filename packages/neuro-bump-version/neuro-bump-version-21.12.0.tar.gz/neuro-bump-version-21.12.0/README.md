# neuro-bump-version
Bump neu-ro tag to the next version


## Installation

Install with [pipx](https://pypa.github.io/pipx/) in *user* space to access the tool
everywhere:

```
$ pipx install neuro-bump-version
```

## Usage

1. Change the current folder to cloned git project (or a subfolder).

2. Run `neuro-bump-version` to create a next tag using Neu.ro versioning schema (see below).
   Only projects with `use_scm_version` configured are supported.


## Versioning schema

The schema should conform SemVer, CalVer, and Python PEP 440.

We use `YY.MM(.NN)` naming where `YY` is the last 2 digits of year, `MM` is the month
number without trailing zero, NN is an incremental number instead, resetting this number
to zero every month.

Zero incremental number is omitted.

For example, the first release in October will be `21.10` (implicit trailing zero),
the next is `21.10.1`, `21.10.2` and so on until November.
The first release in November should be `21.11`.
