import numpy as np
import scipy.integrate as integrate

def perform_backbone(save_backup=True):
    def get_ki(W, i):
        ki = int(np.sum(np.ceil(W[i])))
        return ki

    def calculate_backbone(W):
        n_rows = W.shape[0]
        n_cols = W.shape[1]
        Alpha = np.ones((n_rows, n_cols))
        
        for i in range(n_rows):
            for j in range(n_cols):
                ki = get_ki(W, i)
                p_ij = W[i, j] / np.sum(W[i])
                integral_kernel = integrate.quad(lambda x: (1 - x)**(ki - 2), 0, p_ij)
                Alpha[i, j] = 1 - (ki - 1)*integral_kernel[0]
                
        return Alpha


    for year in range(2001, 2022+1):
        W = np.loadtxt(f'./backups/W_backup/W_{year}.txt')
        Alpha = calculate_backbone(W)

        if save_backup:
            np.savetxt(f'./backups/Alpha_backup/Alpha_{year}.txt', Alpha)
            print(f'>>> Alpha_{year}.txt saved.')