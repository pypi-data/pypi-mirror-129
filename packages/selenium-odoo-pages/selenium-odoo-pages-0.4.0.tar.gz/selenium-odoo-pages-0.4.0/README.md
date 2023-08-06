[![pipeline status](https://gitlab.com/micro-entreprise/selenium-odoo-pages/badges/main/pipeline.svg)](https://gitlab.com/micro-entreprise/selenium-odoo-pages/)
[![coverage report](https://gitlab.com/micro-entreprise/selenium-odoo-pages/badges/main/coverage.svg)](https://gitlab.com/micro-entreprise/selenium-odoo-pages/)
[![Version status](https://img.shields.io/pypi/v/selenium-odoo-pages.svg)](https://pypi.python.org/pypi/selenium-odoo-pages/)
[![PyPi Package](https://img.shields.io/pypi/dm/selenium-odoo-pages?label=pypi%20downloads)](https://pypi.org/project/selenium-odoo-pages)

# Selenium odoo pages

A set of pages and elements used to interact with odoo
pages and widgets using the [page selenium objects](
https://selenium-python.readthedocs.io/page-objects.html
) pattern.

## Usage

This library provides set of common tools using Selenium
to interact with odoo web pages. It was written to write
Behavior-Driven Development tests but can be used without
Gherkin language as described bellow.

To learn about Gherkin language you may start with
[pytest-bdd documentation](https://pypi.org/project/pytest-bdd/)
the recommended tools to launch your tests.

The [example directory](./example) contains examples of
usages that are also used to test this library.

### Rules of thumb to make scenario easier to maintains

* scenario should be as short as possible
* a scenario should focus to one thing
* preparing data should be as fast as possible using available
  shortcut (xmlrpc, database access...)

## Contributing

The idea of this librairy is t
