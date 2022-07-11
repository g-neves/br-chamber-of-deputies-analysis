import numpy as np

def create_weights_matrix(save_backup=True):
    for year in range(2001, 2022+1):
        A = np.loadtxt(f'./backups/A_backup/A_{year}.txt')
        n_rows = A.shape[0]
        W = np.zeros((n_rows, n_rows))
        
        for deputy_a in range(n_rows):
            for deputy_b in range(n_rows):
                denominator = np.sum(np.abs(A[deputy_a]*A[deputy_b]))
                numerator = np.dot(A[deputy_a], A[deputy_b])
                
                if denominator == 0 or numerator < 0 or deputy_a == deputy_b:
                    W[deputy_a, deputy_b] = 0
                else:
                    W[deputy_a, deputy_b] = numerator / denominator
                
        if save_backup:
            np.savetxt(f'./backups/W_backup/W_{year}.txt', W)
            print(f'>>> W_{year}.txt saved.')


