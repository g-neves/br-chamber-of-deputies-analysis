import networkx as nx
import numpy as np

def exclude_weakest_links(input_matrix): 
    def calculate_largest_connected_component(matrix):
        G = nx.from_numpy_matrix(matrix)
        largest_cc = max(nx.connected_components(G), key=len)
        return len(largest_cc) / matrix.shape[0], largest_cc

    def exclude_links(matrix, value_idx_dict, values_list, idx_to_cut, n_to_exclude):
        for value in values_list[0][idx_to_cut:idx_to_cut+n_to_exclude]:
            idx_to_exclude = value_idx_dict[value][0]
            matrix[idx_to_exclude] = 0
            if len(value_idx_dict[value]) > 1:
                del value_idx_dict[value][0]

    
    # Dict with alphas as keys and indices as values
    value_idx_dict = {}
    # Iterates over the alpha_matrix: 
    # 1) If the value is zero, skip it
    # 2) If the value is not in the dict, create a 
    # key with its value and start a list with its index
    # 3) If the value is already in the dict, append the 
    # index to the list of indices
    alpha_matrix = np.ones((input_matrix.shape[0], input_matrix.shape[1])) - input_matrix
    for i in range(alpha_matrix.shape[0]):
        for j in range(alpha_matrix.shape[1]):
            if alpha_matrix[i, j] == 0:
                continue
            if alpha_matrix[i, j] not in value_idx_dict:
                value_idx_dict[alpha_matrix[i, j]] = [(i, j)]
            else:
                value_idx_dict[alpha_matrix[i, j]].append((i, j))

    # Gets all values bigger than zero in the alpha matrix
    values_list = alpha_matrix[alpha_matrix > 0].reshape(1, -1)
    # Sorts the above alphas list
    values_list.sort()

    # Since we start with the original matrix, fully connected network,
    # the starting proportion of its biggest component is 1
    # Furthermore, we want to exclude the weakest links first; thus,
    # we start with the first index, i.e. 0
    prop = 1
    idx_to_cut = 0
    while prop > 0.80:
        # If the proportion is too high, we start cutting a lot of edges
        if prop >= 0.9:
            n_to_exclude = 1000
            exclude_links(alpha_matrix, value_idx_dict, values_list, idx_to_cut, n_to_exclude)
            # Refresh the index to cut
            idx_to_cut += n_to_exclude
            # Calculates the new proportion and the largest component
            prop, largest = calculate_largest_connected_component(alpha_matrix)
        # Starting dropping the number of edges to exclude as the proportion shrinks
        elif prop >= 0.85:
            n_to_exclude = 100
            exclude_links(alpha_matrix, value_idx_dict, values_list, idx_to_cut, n_to_exclude)
            idx_to_cut += n_to_exclude
            prop, largest = calculate_largest_connected_component(alpha_matrix)
        else:
            n_to_exclude = 10
            exclude_links(alpha_matrix, value_idx_dict, values_list, idx_to_cut, n_to_exclude)
            idx_to_cut += n_to_exclude
            prop, largest = calculate_largest_connected_component(alpha_matrix)


    return alpha_matrix, largest, prop
