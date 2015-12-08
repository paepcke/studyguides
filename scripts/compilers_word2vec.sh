#!/bin/bash

word2vec -train ../data/compilers_concatenated.txt -output "../data/vectors.txt" \
         -min-count 0 -size 300 -debug 2q
