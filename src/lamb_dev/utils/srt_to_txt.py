import argparse
import re
import string

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert multiple .srt files to a .txt file.'
    )
    parser.add_argument('--input', nargs='+', help='A list of .srt files.')
    parser.add_argument('--output', help='A .txt file to output.')
    parser.add_argument('--stop-words', help='A .txt file of stop words.')
    parser.add_argument('--verbose', type=int, default=0)
    args = parser.parse_args()

    stop_words = set()
    with open(args.stop_words) as f:
        for line in f:
            word = line.strip()
            stop_words.add(word)

    text_lines = []

    for name in args.input:

        if args.verbose > 0:
            print 'Reading {}'.format(name)

        with open(name) as f:
            while True:
                _seq_no = f.readline()
                if _seq_no == '': break
                _interval = f.readline()

                while True:
                    line = f.readline().strip()
                    if line == '': break
                    words = line.split(' ')

                    words = [word for word in words if word not in stop_words]
                    words = [word.replace('&#39;', "'") for word in words]
                    words = [word.lower() for word in words]
                    words = [
                        re.sub('[{}]'.format(string.punctuation), '', word)
                        for word in words
                    ]

                    text_lines.extend(words)

    if args.verbose > 0:
        print '{} words total, {} unique'.format(len(text_lines), len(set(text_lines)))

    with open(args.output, 'w') as f:
        f.write(' '.join(text_lines))