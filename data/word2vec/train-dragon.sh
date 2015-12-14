./word2vec -train dragon/dragon-book.txt -output dragon/word-vectors.bin -binary 1 -debug 2 -save-vocab dragon/word-vocab.txt -iter 50 -debug 2

./word2phrase -train dragon/dragon-book.txt -output dragon/phrases.txt -threshold 50
./word2vec -train dragon/phrases.txt -output dragon/phrases-vectors.bin -binary 1 -debug 2 -window 20 -size 500 -save-vocab dragon/phrases-vocab.txt

