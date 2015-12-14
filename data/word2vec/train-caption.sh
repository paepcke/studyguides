./word2vec -train captions/captions.txt -output captions/word-vectors.bin -binary 1 -debug 2 -save-vocab captions/word-vocab.txt -iter 50 -debug 2

./word2phrase -train captions/captions.txt -output captions/phrases.txt -threshold 50
./word2vec -train captions/phrases.txt -output captions/phrases-vectors.bin -binary 1 -debug 2 -window 20 -size 500 -save-vocab captions/phrases-vocab.txt

