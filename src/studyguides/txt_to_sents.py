import argparse
import nltk

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')

    args = parser.parse_args()

    with open(args.file) as f:
        raw = ' '.join([line.strip() for line in f])
    sents = nltk.sent_tokenize(raw)
    with open(args.file.replace('txt', 'sents'), 'w') as f:
        for sent in sents:
            f.write(sent + ' | \n')
