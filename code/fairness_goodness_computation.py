'''
Code for the paper:
Edge Weight Prediction in Weighted Signed Networks. 
Conference: ICDM 2016
Authors: Srijan Kumar, Francesca Spezzano, VS Subrahmanian and Christos Faloutsos

Author of code: Srijan Kumar
Email of code author: srijan@cs.stanford.edu
'''

import networkx as nx
import math

def compute_fairness_goodness(G):
    fairness = {}
    goodness = {}
    for i in G.nodes():
        fairness[i] = 1
        goodness[i] = 1
    nodes = G.nodes()
    iter = 0
    while iter < 10000:
        df = 0
        dg = 0
        for node in nodes:
            inedges = G.in_edges(node, data='weight')
            g = 0
            for edge in inedges:
                g += fairness[edge[0]]*edge[2]
            try:
                dg += abs(g/len(inedges) - goodness[node])
                goodness[node] = g/len(inedges)
            except:
                pass
        for node in nodes:
            outedges = G.out_edges(node, data='weight')
            f = 0
            for edge in outedges:
                f += 1.0 - abs(edge[2] - goodness[edge[1]])/2.0
            try:
                df += abs(f/len(outedges) - fairness[node])
                fairness[node] = f/len(outedges)
            except:
                pass
        #print('Differences in fairness score and goodness score = %.2f, %.2f' % (df, dg))
        if df < math.pow(10, -6) and dg < math.pow(10, -6):
            break
        iter+=1
    return fairness, goodness

#skip = int(sys.argv[1])

G = nx.MultiGraph()
f = open("soc-sign-bitcoinotc.csv","r")
for l in f:
    ls = l.strip().split(",")
    G.add_edge(int(ls[0]), int(ls[1]), weight = float(ls[2])/15) ## the weight should already be in the range of -1 to 1
f.close()


# these two dictionaries have the required scores
fairness, goodness = compute_fairness_goodness(G)
print(fairness)
print(goodness)