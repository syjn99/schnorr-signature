#!/bin/bash

for i in {1..6}; do
  echo "Running test vector $i..."
  uv run main.py test --test_vector_file ./test_vectors/test$i.txt
  echo "----------------------------------------"
done