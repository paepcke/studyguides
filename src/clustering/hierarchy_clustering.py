from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sys import stdin
import argparse
import math
import os
import random
import word2vec

parser = argparse.ArgumentParser()
parser.add_argument('--rand-seed', action='store', dest='rand_seed', default="0")
parser.add_argument('--seed-word', action="store", dest="seed_word", default="parser")
parser.add_argument('--threshold', action="store", dest="threshold", default="0")
parser.add_argument('--max-cluster-size', action='store', dest='max_cluster_size', default="10")
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False)
parser.add_argument('--maxdist', action='store_true', dest='maxdist', default=False)
args = parser.parse_args()

###############################################################################
####                     KMEANS CLUSTERING MODEL                           ####
###############################################################################

NUM_CLUSTERS = 2

class ClusterTree(object):
  """
  Attributes:
    terms = dict(string, list(float))
    parent = ClusterTree
    children = list(ClusterTree)
  """
  def __init__(self, clusterID, terms, parent = None, _ = None):
    self.clusterID = clusterID
    self.parent = parent
    self.terms = dict(terms)
    self.children = list()
    self.loss = 0
    clusters = dict() # dict(label, dict(term, vector))
    if NUM_CLUSTERS <= len(self.terms) and \
        (float(args.threshold) > 0.0 or \
          int(args.max_cluster_size) < len(self.terms)):
      # identify clusters
      X = self.terms.values()
      labels = KMeans(n_clusters=NUM_CLUSTERS).fit_predict(X)
      if args.rand_seed != 0:
        labels = KMeans( \
          n_clusters=NUM_CLUSTERS, \
          random_state=int(args.rand_seed)).fit_predict(X)
      # separate vectors based on labels
      for index, term in enumerate(self.terms):
        label = labels[index]
        if label not in clusters:
          clusters[label] = dict()
        clusters[label][term] = self.terms[term]
      tempClusters = dict()
      tempClusters[0] = self.terms;
      self.loss = self.getLoss(tempClusters)
      # create child clusters based on labels
      for i, label in enumerate(clusters):
        childID = NUM_CLUSTERS * self.clusterID + i
        child = ClusterTree(childID, clusters[label], self)
        self.children.append(child)
      if float(args.threshold) > 0.0 and \
          abs(self.loss - sum([c.loss for c in self.children])) \
            < float(args.threshold):
        self.children = list()
    else:
      clusters[0] = self.terms
      self.loss = self.getLoss(clusters)

  def getCentroids(self, clusters):
    # calculate centroid sum
    centroids = dict()
    for label in clusters:
      centroid = [0] * len(clusters[label][clusters[label].keys()[0]])
      for term in clusters[label]:
        for i in range(len(clusters[label][term])):
          centroid[i] += clusters[label][term][i]
      centroids[label] = centroid
    for label in centroids:
      count = float(len(clusters[label]))
      for i in range(len(centroids[label])):
        centroids[label][i] = float(centroids[label][i]) / count
    return centroids

  def getLoss(self, clusters):
    if args.maxdist:
      return self.getMaxDistLoss(clusters)
    else:
      return self.getSqErrorLoss(clusters)

  def getSqErrorLoss(self, clusters):
    centroids = self.getCentroids(clusters)
    loss = 0.0
    for label in centroids:
      closs = 0.0
      for term in clusters[label]:
        dist = 0.0
        for i in range(len(clusters[label][term])):
          dist += math.pow((centroids[label][i] - clusters[label][term][i]), 2)
        closs += math.sqrt(dist);
      loss += closs
    return loss

  def getMaxDistLoss(self, clusters):
    centroids = self.getCentroids(clusters)
    loss = 0.0
    for label in centroids:
      closs = -1.0
      for term in clusters[label]:
        dist = 0.0
        for i in range(len(clusters[label][term])):
          dist += math.pow((centroids[label][i] - clusters[label][term][i]), 2)
        closs = max(closs, math.sqrt(dist));
      loss += closs
    return loss

  def printNode(self, fout):
    if self.isLeaf():
      fout.write("cluster: " + str(self.clusterID) + " " + str(self.terms.keys()) + "\n")
#      if self.parent != None:
#        fout.write("         " + str(len(self.parent.children)) + ", " + str(self.parent.loss) + " --> " + str(self.loss) + "\n")
    else:
      for child in self.children:
        child.printNode(fout)

  def getCentroid(self):
    return self.terms[0] if len(self.terms) > 0 else ""

  def isLeaf(self):
    return len(self.children) == 0

  def isRoot(self):
    return self.parent == None

###############################################################################
####                        PROPOGATING KNN                                ####
###############################################################################

NUM_NEIGHBORS = 5
MAX_NEIGHBORS_SIZE = 10

class PropKNN(object):
  """
  Attributes:
    label
    children
  """
  def __init__(self, nodeID, term, terms, parent = None):
    self.nodeID = nodeID
    self.term = term
    self.parent = parent
    self.childrenLabels = dict()
    self.children = list()
    assert term in terms
    termVector = terms[term]
    iterm = terms.keys().index(term)
    X = terms.values()
    knn = NearestNeighbors(n_neighbors=NUM_NEIGHBORS + 1, algorithm='brute', metric='cosine').fit(X)
    distances, neighbors = knn.kneighbors(X)
    keys = terms.keys()
    assert len(distances) == len(keys)
    for i, ikey in enumerate(neighbors[iterm]):
      if term != keys[ikey]:
        self.childrenLabels[keys[ikey]] = distances[iterm][i]
    del terms[term]

  def getWordDistance(self, word):
    return self.childrenLabels.get(word, float('+inf'))

  def removeWord(self, word):
    if word in self.childrenLabels:
      del self.childrenLabels[word]

  def shouldBuildChildren(self):
    return MAX_NEIGHBORS_SIZE < len(self.childrenLabels)

# removes repeated terms in one level
# level = list( PropKNN )
def pruneLevel(level):
  print "<<<<<<<<<<<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>>>>"
  for node in level:
    print "original: ", node.term, " => ", node.childrenLabels.keys()

  # create a dict of terms 
  usedTerms = dict() # dict( key , [ bestDistance, bestIndeces, badIndeces ] )
  for i, node in enumerate(level):
    for childTerm in node.childrenLabels:
      distance = node.childrenLabels[childTerm]
      if childTerm not in usedTerms: # add new best index
        usedTerms[childTerm] = (distance, [i], list())
#        print "created: ", childTerm, usedTerms[childTerm]
      else:
        bestDistance, bestIndeces, badIndeces = usedTerms[childTerm]
        if distance < bestDistance: # update best index
          usedTerms[childTerm] = (distance, [i], badIndeces + bestIndeces)
#          print "     updated: ", childTerm, usedTerms[childTerm]
        elif distance == bestDistance:
          usedTerms[childTerm] = (distance, bestIndeces + [i], badIndeces)
        else:
          usedTerms[childTerm] = (distance, bestIndeces, badIndeces + [i])

  print "---------------------------------------------------"

#  print "\n", usedTerms, "\n" 

  # remove terms from trees that didnt make the cut
  for term in usedTerms:
    _, bestIndeces, badIndeces = usedTerms[term]
    bestIndex = random.choice(bestIndeces)
    bestIndeces.remove(bestIndex)
    badIndeces += bestIndeces
    for i in badIndeces:
      del level[i].childrenLabels[term]

  for node in level:
    print "     pruned: ", node.term, " => ", node.childrenLabels.keys()
  print "<<<<<<<<<<<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>>>>"
  print ""

# remove the terms used in the level
def getPrunedTerms(level, terms):
  pruned = dict(terms)
  for i, node in enumerate(level):
    for term in node.childrenLabels:
      if term in pruned:
        del pruned[term]
  return pruned

def getUnusedTerms(terms, usedTerms):
  tempTerms = dict(terms)
  for term in usedTerms:
    if term in tempTerms:
      del tempTerms[term]
  return tempTerms

def createKNNTree(term, nodeID, terms):


  root = PropKNN(nodeID, term, terms)
  usedTerms = [term]
  for childTerm in root.childrenLabels:
    if childTerm not in usedTerms:
      usedTerms.append(childTerm)
  assert term not in terms
  level = [root]
  nlevels = 0
  nnodes = 0
  while 0 < len(level):
    nlevels += 1
    nnodes += len(level)
    pruneLevel(level) # eliminate repeated terms from trees in level
    nextTerms = getUnusedTerms(terms, usedTerms)
    
    if args.verbose:
      print "josehdz: nlevels: ", nlevels, "     nnodes: ", nnodes, "     nterms: ", len(nextTerms)
    levelTerms = ""
    for node in level:
      levelTerms += (node.term + " ")
    if args.verbose:
      print "         levelTerms: ", levelTerms
      print "         usedTerms: ", usedTerms
      print " "
    userinput = stdin.readline()

    nextLevel = list()
    for node in level:
      for i, childTerm in enumerate(node.childrenLabels):
        assert childTerm in usedTerms
        assert childTerm not in nextTerms
        nextTerms[childTerm] = terms[childTerm]
        childID = node.nodeID * NUM_NEIGHBORS + i
        child = PropKNN(childID, childTerm, nextTerms)
        for used in child.childrenLabels:
          if used not in usedTerms:
            usedTerms.append(used)
        node.children.append(child)
        nextLevel.append(child)
        assert childTerm in usedTerms
        assert childTerm not in nextTerms
    level = nextLevel
    terms = nextTerms
  return root

###############################################################################
####                        CLUSTERING CODE                                ####
###############################################################################

model = word2vec.load(constants.W2V_UNIGRAM_REL_PATH + W2V_VOCAB_FILE)
terms = dict()
for term in model.vocab:
  terms[term] = model[term]

def generateKMeansClusters():
  suffix = "_" + args.max_cluster_size + "maxsize"
  if int(args.threshold) > 0:
    suffix = "_" + args.threshold
    if args.maxdist:
      suffix = "maxdist"
    else:
      suffix = "meandist"
  outfilename = "kmeans-clusters_" + args.threshold + "_" + suffix + ".txt"
  outfilename = constants.KMEANS_CLUSTERS_REL_PATH + outfilename
  os.system("rm -f " + outfilename)
  rootCluster = ClusterTree(1, terms, None, None)
  fout = open(outfilename, "w+")
  rootCluster.printNode(fout)
  fout.close()

def generateKNNTree(term, nodeID):
  tempTerms = dict(terms)
  root = createKNNTree(term, nodeID, tempTerms)

if args.run_kmeans:
  generateKMeansClusters()
elif args.run_knn:
  generateKNNTree(args.seed_word, 1)
