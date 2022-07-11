from venv import create
from utils.download_base import download_base 
from utils.create_votes_matrix import create_votes_matrix 
from utils.create_weights_matrix import create_weights_matrix
from utils.perform_backbone import perform_backbone
from utils.backbone import disparity_filter
from utils.exclude_weakest_links import exclude_weakest_links
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


if __name__ == '__main__':
    #download_base()
    #create_votes_matrix()
    #create_weights_matrix()
    # perform_backbone()

    W_matrices = []
    for year in range(2001, 2022+1):
        W_matrices.append(np.loadtxt(f'backups/W_backup/W_{year}.txt'))

    w = np.ones((W_matrices[-2].shape[0], W_matrices[-2].shape[1])) - W_matrices[-2]
    test_G = nx.from_numpy_array(w)
    test_G_2 = nx.Graph(w)
    Alpha_disparity = disparity_filter(test_G)
    Alpha_disparity_2 = disparity_filter(test_G_2)
    print(test_G)
    print(test_G_2)

    print(type(Alpha_disparity))
    print(Alpha_disparity)
    print(type(Alpha_disparity_2))
    print(Alpha_disparity_2)
    for edge in Alpha_disparity.edges():
        print(edge)
    nx.draw(Alpha_disparity)
    plt.show()
    Alpha_gdn = np.loadtxt('backups/Alpha_backup/Alpha_2020.txt')
    G = nx.Graph(Alpha_gdn)
    print(type(G))
    print(G)

    alpha_final, largest, prop = exclude_weakest_links(Alpha_gdn)

    print(prop)
    print(largest)
    for i in range(550):
        if i not in largest:
            print(i)
    print(alpha_final)

