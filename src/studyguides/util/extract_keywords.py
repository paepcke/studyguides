import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('directory')
parser.add_argument('outfile')

args = parser.parse_args()

# From (file, keyword) => (first, rank)
keywords = {}

for name in os.listdir(args.directory):
	with open(os.path.join(args.directory, name)) as f:
		while True:
			line = f.readline().strip()

			if line == '':
				break

			_, temp = line.split('|')
			temp = temp.strip()
			if temp != '':
				terms = [term.strip().lower() for term in temp.split(',')]
				for term in terms:

					if term[-1] == '*':
						term = term[:-1].strip()
						keywords[name, term] = [True, 0]
					else:
						keywords[name, term] = [False, 0]

		rank_line = f.readline().strip()
		assert rank_line.startswith('Keywords')
		# if rank_line.startswith('Keywords'):
		rank = 1
		while True:
			term = f.readline().strip().lower().lstrip('-')
			if term == '':
				break

			if (name, term) not in keywords:
				print('In file {}, term "{}" in top terms but not listed on any line.'.format(name, term))
				keywords[name, term] = [False, rank]
			else:
				keywords[name, term][1] = rank
		# else:
		# 	if not rank_line.startswith('Top Term'):
		# 		print('Could not find top terms for {}'.format(name))
		# 	else:
		# 		_, temp = rank_line.split(':')

		# 		terms = []
		# 		if temp == '':
		# 			while True:
		# 				term = f.readline().strip().lower()
		# 				if term == '':
		# 					break
		# 				terms.append(term)
		# 		else:
		# 			terms = [term.strip().lower() for term in temp.split(',')]

		# 		for idx, term in enumerate(terms):

		# 			if (name, term) not in keywords:
		# 				print('In file {}, term "{}" in top terms but not listed on any line.'.format(name, term))
		# 				keywords[name, term] = [False, idx + 1]
		# 			else:
		# 				keywords[name, term][1] = idx + 1


with open(args.outfile, 'w') as f:
	for (file_name, term), (first, rank) in sorted(keywords.items()):
		f.write('{},{},{},{}\n'.format(file_name, term, first, rank))
