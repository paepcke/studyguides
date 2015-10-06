#!/bin/bash

SRT_ROOT='/Users/andrewlamb/Google_Drive/Stanford/CS199/CompilersSelfPacedCS1'

SRT_NAMES=(
"${SRT_ROOT}/01-01-introduction-redo-correction.srt"
"${SRT_ROOT}/01-02-structure-of-a-compiler-final.srt"
"${SRT_ROOT}/01-03-economy-of-Programming-Languages_19m51s_.srt"
"${SRT_ROOT}/02-01-cool-overview-final.srt"
"${SRT_ROOT}/02-02-cool-example-ii-final.srt"
"${SRT_ROOT}/02-03-cool-example-iii-final-correction.srt"
"${SRT_ROOT}/03-01-Lexical-Analysis-Part-1.srt"
"${SRT_ROOT}/03-02-lexical-analysis-examples-final.srt"
"${SRT_ROOT}/03-03-A+Regular+Languages.srt"
"${SRT_ROOT}/03-04-formal-languages.srt"
"${SRT_ROOT}/03-05-lexical-specifications-final-quizupdate.srt"
"${SRT_ROOT}/04+02+finite+automata+part+1.srt"
"${SRT_ROOT}/04-01-lexical-specification.srt"
"${SRT_ROOT}/04-03-regular-expressions-to-nfas-final-quizupdate-correction.srt"
"${SRT_ROOT}/04-04-nfa-to-dfa-quizupdate.srt"
"${SRT_ROOT}/04-05-implementing-finite-automata-correction.srt"
"${SRT_ROOT}/05-01-introduction-to-parsing.srt"
"${SRT_ROOT}/05-02-A+Context+Free+Grammars.srt"
"${SRT_ROOT}/05-03-Derivations-Part-1.srt"
"${SRT_ROOT}/05-04-A+Ambiguity.srt"
"${SRT_ROOT}/06-01-error-handling.srt"
"${SRT_ROOT}/06-02-abstract-syntax-trees.srt"
"${SRT_ROOT}/06-03-recursive-descent-parsing.srt"
"${SRT_ROOT}/06-04-1-recursive-descent-limitations-04-1.srt"
"${SRT_ROOT}/06-04-recursive-descent-algorithm.srt"
"${SRT_ROOT}/06-05-A+Left+Recursion.srt"
"${SRT_ROOT}/07-01-Predictive-Parsing-Part-1.srt"
"${SRT_ROOT}/07-02-first-sets.srt"
"${SRT_ROOT}/07-03-follow-sets.srt"
"${SRT_ROOT}/07-04-ll1-parsing-tables.srt"
"${SRT_ROOT}/07-05-Bottom-Up-Parsing-Part-1.srt"
"${SRT_ROOT}/07-06-Shift-Reduce-Parsing-Part-1.srt"
"${SRT_ROOT}/08-01-Handles-Part-1.srt"
"${SRT_ROOT}/08-02-recognizing-handles.srt"
"${SRT_ROOT}/08-03-recognizing-viable-prefixes.srt"
"${SRT_ROOT}/08-04-valid-items.srt"
"${SRT_ROOT}/08-05-slr-parsing.srt"
"${SRT_ROOT}/08-06-slr-parsing-example.srt"
"${SRT_ROOT}/08-07-slr-improvements.srt"
"${SRT_ROOT}/08-08-slr-examples-correction.srt"
"${SRT_ROOT}/09-01-introduction-to-semantic-analysis.srt"
"${SRT_ROOT}/09-02-scope.srt"
"${SRT_ROOT}/09-03-symbol-tables.srt"
"${SRT_ROOT}/09-04-types.srt"
"${SRT_ROOT}/09-05-A+Type+Checking.srt"
"${SRT_ROOT}/09-06-A+Type+Environments.srt"
"${SRT_ROOT}/09-07-A+Subtyping.srt"
"${SRT_ROOT}/09-08-A+Typing+Methods.srt"
"${SRT_ROOT}/09-09-implementing-type-checking.srt"
"${SRT_ROOT}/10-01-A+Static+vs.+Dynamic+Typing.srt"
"${SRT_ROOT}/10-02-self-type.srt"
"${SRT_ROOT}/10-03-A+Self+Type+Operations.srt"
"${SRT_ROOT}/10-04-self-type-usage.srt"
"${SRT_ROOT}/10-05-A+Self+Type+Checking.srt"
"${SRT_ROOT}/10-06-error-recovery.srt"
"${SRT_ROOT}/11-01-runtime-organization.srt"
"${SRT_ROOT}/11-02-A+Activations.srt"
"${SRT_ROOT}/11-03-activation-records.srt"
"${SRT_ROOT}/11-04-globals-and-heap.srt"
"${SRT_ROOT}/11-05-alignment.srt"
"${SRT_ROOT}/11-06-stack-machines.srt"
"${SRT_ROOT}/12-01-introduction-to-code-generation.srt"
"${SRT_ROOT}/12-02-A+Code+Generation+I.srt"
"${SRT_ROOT}/12-03-A+Code+Generation+II.srt"
"${SRT_ROOT}/12-04-code-generation-example.srt"
"${SRT_ROOT}/12-05-A+Temporaries.srt"
"${SRT_ROOT}/12-06-A+Object+Layout.srt"
"${SRT_ROOT}/13-01-semantics-overview.srt"
"${SRT_ROOT}/13-02-operational-semantics.srt"
"${SRT_ROOT}/13-03-cool-semantics-i.srt"
"${SRT_ROOT}/13-04-A+Cool+Semantics+II.srt"
"${SRT_ROOT}/14-01-intermediate-code.srt"
"${SRT_ROOT}/14-02-optimization-overview.srt"
"${SRT_ROOT}/14-03-local-optimization.srt"
"${SRT_ROOT}/14-04-peephole-optimization.srt"
"${SRT_ROOT}/15-02-constant-propagation.srt"
"${SRT_ROOT}/15-03-analysis-of-loops.srt"
"${SRT_ROOT}/15-04-orderings.srt"
"${SRT_ROOT}/15-05-A+Liveness+Analysis.srt"
"${SRT_ROOT}/16-01-register-allocation.srt"
"${SRT_ROOT}/16-02-A+Graph+Coloring.srt"
"${SRT_ROOT}/16-03-A+Spilling.srt"
"${SRT_ROOT}/16-04-managing-caches.srt"
"${SRT_ROOT}/17-01-automatic-memory-management.srt"
"${SRT_ROOT}/17-02-A+Mark+and+Sweep.srt"
"${SRT_ROOT}/17-03-A+Stop+and+Copy.srt"
"${SRT_ROOT}/17-04-conservative-collection.srt"
"${SRT_ROOT}/17-05-A+Reference+Counting.srt"
"${SRT_ROOT}/18-01-java.srt"
"${SRT_ROOT}/18-02-java-arrays.srt"
"${SRT_ROOT}/18-03-java-exceptions.srt"
"${SRT_ROOT}/18-04-java-interfaces.srt"
"${SRT_ROOT}/18-05-java-coercions.srt"
"${SRT_ROOT}/18-06-java-threads.srt"
"${SRT_ROOT}/18-07-other-topics.srt"
)

python ../src/lamb_dev/utils/srt_to_txt.py --verbose 1 \
         --output ${SRT_ROOT}/captions.txt \
         --input ${SRT_NAMES[@]} \
         --stop-words ../src/lamb_dev/ranks_nl_stop_words_long.txt
word2vec -train ${SRT_ROOT}/captions.txt -output ${SRT_ROOT}/vectors.bin \
         -binary 1 -debug 2 -save-vocab ${SRT_ROOT}/vocab.txt -iter 50 -debug 2
