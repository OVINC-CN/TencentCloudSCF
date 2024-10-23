#!/bin/sh
pylint --disable=C0114,C0115,C0116,R0903,R0913,R0917 --max-line-length=120 $(git ls-files '*.py')
