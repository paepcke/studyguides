from scipy.spatial.distance import cdist
from sets import Set
import argparse
import math
import os
import process_text_files as ptf
import random
import word2vec

parser = argparse.ArgumentParser()
parser.add_argument('--threshold', action="store", dest="threshold", default="1.0")
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False)
parser.add_argument('--exhaustive', action='store_true', dest='exhaustive', default=False)
args = parser.parse_args()

print "josehdz: threshold = ", args.threshold

###########################################################
####                     MODEL                         ####
###########################################################
class Graph:
  def __init__(self, terms, vectors, occurences = None):
    self.vectors = vectors
    self.occurences = occurences
    self.nodes = list(terms)
    self.edges = dict()
    for i in range(len(terms) - 1):
      for j in range(i + 1, len(terms)):
        inode = self.nodes[i]
        jnode = self.nodes[j]
        weight = self.getEdgeWeight(inode, jnode)
        self.edges[(inode, jnode)] = weight
        self.edges[(jnode, inode)] = weight
    self.vectors = None
    # self.occurences = None

  def getOccurence(self, one, two):
    return self.occurences[(one, two)]
  
  def getDistance(self, one, two):
    if len(self.vectors[one].shape) == 1:
      self.vectors[one].resize((100,1))
      self.vectors[one] = self.vectors[one].transpose()
    if len(self.vectors[two].shape) == 1:
      self.vectors[two].resize((100,1))
      self.vectors[two] = self.vectors[two].transpose()
    return cdist( \
      self.vectors[one], \
      self.vectors[two], \
      'sqeuclidean')
  
  def getEdgeWeight(self, one, two):
    numer = float(self.getOccurence(one, two))
    denom = float(self.getDistance(one, two))
    return float('+inf') if denom == 0 else numer / denom

  def shouldCoalesce(self, singleton, cluster):
    edgemin = float('+inf')
    for single in singleton:
      for term in cluster:
        edgemin = min(edgemin, graph.edges.get((single, term), edgemin))
        if edgemin < float(args.threshold):
          # edge is too weak sauce
          return False, edgemin
#    print "josehdz: shouldCoalesce!!!"
    return True, edgemin

###########################################################
####                PRE-PROCESSING                     ####
###########################################################

vocabulary = list()
#with open('../../data/word2vec/auto_index.txt') as src:
with open('../../data/word2vec/dragon/dragon-index.txt') as src:
  for line in src:
    line = " ".join(line.split("-"))
    lines = line.split(",")
    for l in lines:
      vocabulary.append(l.strip().lower())
print "len(vocabulary) = ", len(vocabulary)

vectors = dict() # term => vector
model = word2vec.load('../../data/word2vec/dragon-ngrams/word-vectors-pruned.bin')
#model = word2vec.load('../../data/word2vec/dragon/word-vectors-pruned.bin')
for iterm in vocabulary:
  vterms = iterm.split(" ")
  shouldContinue = True
  for vterm in vterms:
    if vterm not in model.vocab:
      shouldContinue = False
  if shouldContinue: 
    vterm = "_".join(vterms)
    vectors[vterm] = model[vterms[0]]
    for ii in range(1, len(vterms)):
      vectors[vterm] += model[vterms[ii]]
vocabulary = vectors.keys()
print "len(vocabulary) = ", len(vocabulary)
print ""
print "josehdz: initialized word vectors"

occurences = dict() # (one, two) => count
for ii in range(len(vocabulary)):
  for jj in range(ii + 1, len(vocabulary)):
    okey = (vocabulary[ii], vocabulary[jj])
    rkey = (vocabulary[jj], vocabulary[ii])
    _, count = ptf.get_occurences(okey[0], okey[1])
    occurences[okey] = count 
    occurences[rkey] = count
print "josehdz: initialized word co-occurences"

###########################################################
####                    CLUSTERING                     ####
###########################################################

def cluster(graph, clusters):
  newClusters = list()
  for ii in range(len(clusters)):
    if args.exhaustive:
      coalesced = False
      for jj in range(ii + 1, len(clusters)):
        if ii != jj:
          coalesce, edgemin = graph.shouldCoalesce(clusters[ii], clusters[jj])
          if coalesce:
            candidate = clusters[ii] | clusters[jj]
            coalesced = True
            repeated = True
            for cluster in newClusters:
              if candidate.issubset(cluster):
                repeated = True
                break
            if not repeated:
              newClusters.append(bestCluster)
      if not coalesced:
        newClusters.append(clusters[ii])
    else:
      bestCluster = clusters[ii]
      bestBound = float('+inf')
      for jj in range(len(clusters)):
        if ii != jj:
          coalesce, edgemin = graph.shouldCoalesce(clusters[ii], clusters[jj])
          if coalesce and edgemin < bestBound:
            bestCluster = clusters[ii] | clusters[jj]
            bestBound = edgemin
      repeated = False
      for cluster in newClusters:
        if cluster.issubset(bestCluster) and bestCluster.issubset(cluster):
          repeated = True
          break
      if not repeated:
        newClusters.append(bestCluster)
  return clusters, newClusters
  
graph = Graph(vocabulary, vectors, occurences)
print "josehdz: initialized graph"
clusters = [Set([term]) for term in graph.nodes]
print "josehdz: initialized clusters"

for ii in range(len(graph.nodes)):
#  print "nleft =", (len(graph.nodes) - ii), "\tnclusters =", len(clusters)
  oldClusters, clusters = cluster(graph, clusters)
print ""

print "###########################################################"
#print clusters

suffix = "_textbook"
if args.exhaustive:
  suffix += "_exhaustive"
fout = open("graph-clusters_" + args.threshold + suffix + ".txt", "w+")
for cluster in clusters:
  fout.write(str(cluster) + "\n")
fout.close()
