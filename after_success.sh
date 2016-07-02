#!/bin/bash

echo "after_success"
echo "args: $@"
env | grep -i -e tox -e travis -e ci | sort
