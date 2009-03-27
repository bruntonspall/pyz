#!/bin/bash
cd test
PYTHONPATH=$PYTHONPATH:../src
for x in *_test.py; do
  python $x
done
