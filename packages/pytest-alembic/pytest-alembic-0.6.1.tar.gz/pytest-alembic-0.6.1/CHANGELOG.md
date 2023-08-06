# Changelog

## [Unreleased](https://github.com/schireson/pytest-alembic/compare/v0.5.1...HEAD) (2021-11-30)

### Features

* Add ability to set a minimum bound downgrade migration 4149bfe
* Add new test which asserts parity between upgrade and downgrade detectable effects. ab9b645
* Add new test for roundtrip downgrade isolation. 2fb20d0

### Fixes

* Run pytest tests inline (faster and easier coverage). ea9b59d


### [v0.5.1](https://github.com/schireson/pytest-alembic/compare/v0.5.0...v0.5.1) (2021-11-23)

#### Fixes

* Increase minimum python version to 3.6+ (this was already true!). e6bdfe6
* Incompatibility of branched history downgrade strategy with alembic 1.6+. 192686b
* ensure the up-down consistency test actually verifies migrations a2e9d13


## [v0.5.0](https://github.com/schireson/pytest-alembic/compare/v0.4.0...v0.5.0) (2021-09-03)

### Features

* Add experimental test to identify tables which alembic will not recognize. d12e342

### Fixes

* Add back missing lint job. 80242f3


## [v0.4.0](https://github.com/schireson/pytest-alembic/compare/v0.3.3...v0.4.0) (2021-08-16)

### Features

* Create a mechanism in which to create multiple alembic runner fixtures. ef1d5da
* Allow alembic Config to be used directly in alembic_config fixture. 3b00103

### Fixes

* Run covtest on all branches. f1bd6ac


### [v0.3.3](https://github.com/schireson/pytest-alembic/compare/v0.3.2...v0.3.3) (2021-08-04)

#### Fixes

* Conditionally set script_location. a26f59b


### [v0.3.2](https://github.com/schireson/pytest-alembic/compare/v0.3.1...v0.3.2) (2021-08-04)


### [v0.3.1](https://github.com/schireson/pytest-alembic/compare/v0.3.0...v0.3.1) (2021-05-10)


## [v0.3.0](https://github.com/schireson/pytest-alembic/compare/v0.2.6...v0.3.0) (2021-05-10)


### [v0.2.6](https://github.com/schireson/pytest-alembic/compare/v0.2.5...v0.2.6) (2021-04-26)


### [v0.2.5](https://github.com/schireson/pytest-alembic/compare/v0.2.4...v0.2.5) (2020-07-13)

#### Features

* Allow the customization of the location at which the built in tests are executed. 255c95c


### [v0.2.4](https://github.com/schireson/pytest-alembic/compare/v0.2.3...v0.2.4) (2020-07-01)

#### Fixes

* Require dataclasses only below 3.7, as it is included in stdlib 3.7 onward. 0b30fb4


### [v0.2.3](https://github.com/schireson/pytest-alembic/compare/v0.2.2...v0.2.3) (2020-06-26)

#### Features

* Reduce the multiple pages of traceback output to a few lines of context that are actually meaningful to a failed test. d9bcfcc


### [v0.2.2](https://github.com/schireson/pytest-alembic/compare/v0.2.1...v0.2.2) (2020-06-25)

#### Features

* Add rendered migration body to failed model-sync test. 108db31


### [v0.2.1](https://github.com/schireson/pytest-alembic/compare/v0.1.1...v0.2.1) (2020-03-23)

#### Fixes

* Fix deprecation pytest warning in 3.4. f15a86b


### [v0.1.1](https://github.com/schireson/pytest-alembic/compare/v0.1.0...v0.1.1) (2020-03-09)


## v0.1.0 (2020-03-09)


