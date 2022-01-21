import sys
import os
import numpy as np                                                     
import pandas as pd   
import seaborn as sns                                                  
import matplotlib.pyplot as plt                                        
                                                                  
                                                                      
from Calculator import src_nogrd                                                       
from Calculator.src_nogrd import sym_func_show                                    
from Calculator.src_nogrd import xyzArr_generator                                 
from Calculator.src_nogrd import feat_scaling_func                                
from Calculator.src_nogrd import at_idx_map_generator_old                             
                                                                                                                           
                                                       
import Utils.DirNav                                                
from Utils.dftb_traj_io import read_scan_traj                          
import Utils.DirNav                                      
                                                                       
np.random.seed(98167)  # for reproducibility       

geom_filename          = os.path.join('C:\\Users\\Tysh\\Desktop/dummy.xyz')
md_train_arr_origin    = read_scan_traj(filename=geom_filename)
md_train_arr = md_train_arr_origin.copy(deep=False).reset_index(drop=True)

nAtoms, xyzArr = xyzArr_generator(md_train_arr)

# Calculate distance dataframe from xyz coordinates
distances = src_nogrd.distances_from_xyz(xyzArr, nAtoms)

at_idx_map = at_idx_map_generator_old(md_train_arr[0])

# radial symmetry function parameters
# Need to automate the Rs_array part
cutoff_rad = 10  
#Rs_array = np.linspace(0.8, 5, num=24)   # based on max and min of the distances
Rs_array = np.linspace(0.2, 5, num=10)   # based on max and min of the distances
eta_array = 5/(np.square(0.2*Rs_array))
rad_params = np.array([(Rs_array[i], eta_array[i], cutoff_rad) for i in range(len(Rs_array)) ])

# angular symmetry function parameters
cutoff_ang = 5
lambd_array = np.array([-1, 1])
#zeta_array = np.array([1, 4, 16])
zeta_array = np.array([1,4,16])
#eta_ang_array = np.array([0.001, 0.01, 0.05])
eta_ang_array = np.array( [0.001, 0.01, 0.05])
    
# Each of the element need to be parametrized for all of the list. 
angList = np.array(['CS', 'SS', 'CC','CN','CO','SC','SN','SO','NN','NO'])
ang_comp = {'S':angList,'C':angList,'N':angList,'O':angList}
ang_params = np.array([[eta, zeta, lambd, cutoff_ang] for eta in eta_ang_array for zeta in zeta_array for lambd in lambd_array])
    
Gparam_dict = {}
for at_type in at_idx_map.keys():
    Gparam_dict[at_type] = {}
    Gparam_dict[at_type]['rad'] = {}
    for at2_rad in at_idx_map.keys():
            Gparam_dict[at_type]['rad'][at2_rad] = rad_params

# This Section is already designed to be general
    Gparam_dict[at_type]['ang'] = {}
    for at23_ang in ang_comp[at_type]:
        Gparam_dict[at_type]['ang'][at23_ang] = ang_params

Gfunc_data = src_nogrd.symmetry_function(distances, at_idx_map, Gparam_dict)

sys.stdout = open('%s.txt' % n, "w")

print(Gfunc_data)

sys.stdout.close()