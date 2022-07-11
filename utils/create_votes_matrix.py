import unidecode
import json
import numpy as np


def create_votes_matrix(save_backup=True):
    
    # Auxiliar function to standardize the deputies
    # names
    def format_name(name):
        name = name.lower()
        name = unidecode.unidecode(name)
        
        return name

    BASE_DATA = './data/votacoesVotos-{}.json'

    # Dict in which the data will be stored according to its year
    data_dict = {}
    # Dict in which the project's number will be stored according to its year
    projects_dict = {}
    # Dict in which the deputies names will be stored according to its year
    deputies_dict = {}
    # Dict in which the votes matrix will be stored according to its year
    A_dict = {}

    # Iterating over the years
    for year in range(2001, 2022+1):
        with open(BASE_DATA.format(year), 'r') as f:
            json_data = json.loads(f.read())
        
        data_dict[year] = json_data['dados']
            
        # List with all different projects from a given year
        projects_dict[year] = []
        # Dict with all deputies and their infos from a given year
        deputies_dict[year] = {}
        for vote in data_dict[year]:
            # Checking for the project in the projects list
            vote_id = vote['idVotacao']
            if vote_id not in projects_dict[year]:
                projects_dict[year].append(vote_id)
            
            # Deputy name
            deputy_name = vote['deputado_']['nome']
            deputy_name = format_name(deputy_name)
            
            # Inserting the vote entry into the deputy data
            if deputy_name not in deputies_dict[year]:
                deputies_dict[year][deputy_name] = {'votes': {}}
                deputies_dict[year][deputy_name]['votes'][vote_id] = vote['voto']
            else:
                deputies_dict[year][deputy_name]['votes'][vote_id] = vote['voto']

            # Inserting the deputy party
            deputies_dict[year][deputy_name]['party'] = vote['deputado_']['siglaPartido']
        
        
        # n_rows: number of deputies of given year
        # n_cols: number of projects of given year
        deputies_list = list(deputies_dict[year].keys())
        projects_list = projects_dict[year]
        n_rows = len(deputies_list)
        n_cols = len(projects_list)
        
        # Votes matrix (A for adjacency)
        A = np.zeros((n_rows, n_cols))

        for row in range(n_rows):
            for col in range(n_cols):
                # Get the deputy name
                deputy = deputies_list[row]
                # Get the project 
                project = projects_list[col]
                # Get the actual vote
                if project in deputies_dict[year][deputy]['votes']:
                    vote = deputies_dict[year][deputy]['votes'][project]
                else:
                    vote = 'Ausente'
                
                # Now we define the matrix entry
                matrix_entry = 0
                if vote == 'Sim':
                    matrix_entry = 1
                elif vote in ['Não', 'Obstrução']:
                    matrix_entry = -1
                    
                A[row, col] = matrix_entry

        # Saves the votes matrix into its dict  
        A_dict[year] = A

        if save_backup:
            np.savetxt(f'./backups/A_backup/A_{year}.txt', A)
            print(f'>>> A_{year}.txt saved.')


    