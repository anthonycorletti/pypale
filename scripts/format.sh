#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports pypale tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place pypale tests scripts --exclude=__init__.py
black pypale tests scripts
isort pypale tests scripts
