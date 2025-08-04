#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from ase.io import read
import pickle 


lpath = [
'./job_205137_ase_neb_dftbplus_23.1/results_80-20_1500K_2ps.xyz',
'./foundation_model_test/job_205386_ase_neb_dftbplus_23.1/results_80-20_1500K_2ps.xyz',
'./test_new_starting_point/foundation/job_205894_ase_neb_dftbplus_23.1/results_80-20_1500K_2ps.xyz',
'./test_new_starting_point/scratch/job_205895_ase_neb_dftbplus_23.1/results_80-20_1500K_2ps.xyz',
]

lnames = [
    'scratch-t1-01fs',
    'foundation-rt1-01fs',
    'new_start_scratch-t1-01fs',
    'new_start_foundation-rt1-01fs',
]
ltime_steps = [0.1, 0.1, 0.1, 0.1] # fs
lwriting_interval = [5, 5, 5, 5]

dfiles = {}

# Load ASE data
for num, path in enumerate(lpath):
    key = lnames[num]
    print('loading \t %s' % path)

    dfiles[key] = {}
    dfiles[key]['ase_data'] = read(path, format='extxyz', index=':')

    # Remove cofigurations with NAN
    for i in range(len(dfiles[key]['ase_data'])-1, 0, -1):
        try:
            dfiles[key]['ase_data'][i].get_total_energy()
        except:
            dfiles[key]['ase_data'].pop(i)

    # Extract data from valid configurations
    dfiles[key]['potential_energy'] = np.asarray([x.get_potential_energy() for x in dfiles[key]['ase_data']])
    dfiles[key]['kinetic_energy'] = np.asarray([x.get_kinetic_energy() for x in dfiles[key]['ase_data']])
    dfiles[key]['forces'] = np.asarray([x.get_forces() for x in dfiles[key]['ase_data']])
    
    
    ts = ltime_steps[num] # fs
    writing_interval = lwriting_interval[num] # every ts
    number_steps = len(dfiles[key]['potential_energy'])
    integration_time = ts * number_steps *  writing_interval # fs

    dfiles[key]['path'] = path
    dfiles[key]['ts'] = ts
    dfiles[key]['integration_time'] = integration_time
    dfiles[key]['number_steps'] = number_steps
    dfiles[key]['writing_interval'] = writing_interval




print('Saving Files')
# Open a file and use dump() 
with open('md_objects.pkl', 'wb') as file: 
    # A new file will be created 
    pickle.dump(dfiles, file) 
