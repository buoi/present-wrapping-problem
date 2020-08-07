#!/bin/bash
for file in /Users/buio/ai/constraint_zeynep/project_work/instances_txt/*
do
    echo "running $file"
    python /Users/buio/ai/constraint_zeynep/myz3/bin/python/smt_solver.py "$file"
done
