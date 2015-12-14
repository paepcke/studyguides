============================================================
file: graph_clustering.py

NOTE: This algorithm is using n-gram word vectors, meaning
  that it accounts for all keywords, such as "parser" 
  "epsilon" "context_free_grammar", by joining them
  with underscores and adding the individual word vectors
  to represent the n-gram vector.

Creates a fully-connected graph where the nodes are topic 
keywords. Each edge has a weight that represents the 
"similarity" of topics. We start off with each keyword being
its own cluster, and follow a coalescing hierarchy.

This creates clusters by maintaining the invariant that the
smallest edge in the cluster is at least --threshold. This
is the coalescing criteria. We make sure that each keyword
exists in at least one of the final clusters.

There are two ways of clustering:

  Exhaustive:

    Create every cluster that satisfies the cluster invariant,
    but prune clusters that are subsets of other clusters.

  Limited:

    At each stage, only coalesce once for each cluster, and pick
    the coalesce with the highest intra-cluster edge weight.

Flags:

--threshold <double> :
    This is the minimum edge weight that can exist in order
    to allow the cluster coalescing

--suffix :
    Specify a suffix for the output. Useful for different
    word vectors

--exhaustive :
    Run the exhaustive version instead of the limited version,
    which is the default

--verbose :
    Print the stage we're in for clustering.

============================================================
file: hierarchy_clustering.py  

NOTE: Both of these algorithms use only the word vectors that
  appear as unigram words in the keywords. This means that 
  we only consider keywords like "parser" "epsilon" etc, and 
  ignore "context free grammar"

Recursive KMeans Clustering: 
  This algorithm starts with one cluster containing all of the
  keywords, and recursively splits into two clusters based on 
  particular criteria. One criteria is split until the size of
  the cluster is smaller than or equal to --max-cluster-size.
  The second criteria is split until the parent loss is within
  --threshold of the sum of the childrens' losses, which only
  splits for "big drops" in the loss. We also consider two
  measures for the loss here. One is the sum of the max distance 
  from a member to its centroid, which targets outliers. Two is 
  the mean squared distance for all members from their centroid,
  which targets outliers a bit less aggressively.
    - Distance metric: euclidean (not easily configurable)

  Output: creates a file in the kmeans-clusters folder that
    contains the IDs and elements of each cluster on a line 

Recursive K-Nearest Neighbors:
  This algorithm begins with a --seed-word and recursively
  calls KNN on the children. If we view the KNN propogation
  as a tree, at each level, before propogating the algorithm,
  we go through each child, and, if it is repeated, we assign
  it to the "closest" parent, and, in the case of a tie, picks
  a random among the closest parents.
    - Distance metric: cosine (easily configurable)
  
  Output: interactive clustering (no file output), and must hit
    enter to continue to the next branch of the recursion tree.

Flags:

--run-kmeans:
    specifies to run the kmeans clustering

--run-knn:
    specifies to run interactive knn clustering

--max-cluster-size <int> :
    Specify the maximum size of the clusters, which is used
    for the size-based kmeans splitting criteria. Default is
    10, which works reasonably well.

--rand-seed <int> :
    Specify the seed used for kmeans. Guarantees uniformity
    between trials of different values of --threshold

--seed-word <keyword> :
    This is the word that the KNN sprawl begins with 

--threshold <double> :
    This is the lower bound for the split criteria. If this value
    is not set, it defaults to the size splitting criteria.

--maxdist <double> :
    This specifies whether the threshold kmeans splitting criteria
    should consider the loss to be the max distance (captures
    variance more) or the mean squared

--verbose :
    print outputs

