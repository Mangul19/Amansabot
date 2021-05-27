# -*- encoding: utf-8 -*-
import pandas as pd
import networkx as nx
import operator
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

if __name__ == '__main__':
    dataset = pd.read_csv('DTM/HFACS_DTM2.csv')

    G_centrality = nx.Graph()
    for ind in range((len(np.where(dataset['freq'] >= 0)[0]))):
        G_centrality.add_edge(dataset['word1'][ind], dataset['word2'][ind], weight=int(dataset['freq'][ind]))

    dgr = nx.degree_centrality(G_centrality)        # 연결 중심성
    btw = nx.betweenness_centrality(G_centrality)   # 매개 중심성
    cls = nx.closeness_centrality(G_centrality)     # 근접 중심성
    egv = nx.eigenvector_centrality(G_centrality)   # 고유벡터 중심성
    pgr = nx.pagerank(G_centrality)                 # 페이지 랭크

    # 중심성이 큰 순서대로 정렬한다.
    sorted_dgr = sorted(dgr.items(), key=operator.itemgetter(1), reverse=True)
    sorted_btw = sorted(btw.items(), key=operator.itemgetter(1), reverse=True)
    sorted_cls = sorted(cls.items(), key=operator.itemgetter(1), reverse=True)
    sorted_egv = sorted(egv.items(), key=operator.itemgetter(1), reverse=True)
    sorted_pgr = sorted(pgr.items(), key=operator.itemgetter(1), reverse=True)
    
    # 단어 네트워크를 그려줄 Graph 선언
    G = nx.Graph()

    # 페이지 랭크에 따라 두 노드 사이의 연관성을 결정한다. (단어쌍의 연관성)
    # 연결 중심성으로 계산한 척도에 따라 노드의 크기가 결정된다. (단어의 등장 빈도수)
    for i in range(len(sorted_pgr)):
        G.add_node(sorted_pgr[i][0], nodesize=sorted_dgr[i][1])

    for ind in range((len(np.where(dataset['freq'] > 0)[0]))):
        G.add_weighted_edges_from([(dataset['word1'][ind], dataset['word2'][ind], int(dataset['freq'][ind]))])

    # 노드 크기 조정
    sizes = [G.nodes[node]['nodesize'] * 500 for node in G]

    options = {
        'edge_color': '#FFDEA2',
        'width': 1,
        'with_labels': True,
        'font_weight': 'regular',
    }

    font_fname = 'C:\Windows\Fonts\gulim.ttc'
    fontprop = fm.FontProperties(fname=font_fname, size=18).get_name()

    nx.draw(G, node_size=sizes, pos=nx.spring_layout(G, k=3.5, iterations=100), **options, font_family=fontprop)
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#121111")
    plt.show()