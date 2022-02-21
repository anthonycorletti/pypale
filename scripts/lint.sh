#!/bin/sh -ex

mypy pypale tests
flake8 pypale tests
black pypale tests --check
isort pypale tests scripts --check-only
