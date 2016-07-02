#!/bin/bash

echo "test script"
env | grep -i -e tox -e travis -e ci | sort
