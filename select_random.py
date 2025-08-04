from ase.io import read, write
import numpy as np
import random
import tqdm
import os 


inputfile = 'mace_format_SnO2_hyd.xyz'

configurations = read(inputfile, format='extxyz', index=':')

# lconfigurations_tens = list(configurations[1000::10].copy())
# Skip th first 10 to avoi big jump in Epot, and take avery 10 steps to avoid too much correlation
lconfigurations_tens = list(configurations[10::10].copy())

newpath = str('mace_data/300K_every10_after1ps/')
if not os.path.exists(newpath):
    os.makedirs(newpath)



# Shuffle data
random.shuffle(lconfigurations_tens)

# Split all into two sets of equal size
S1 = lconfigurations_tens[:int(len(lconfigurations_tens) * 0.5)]
S2 = lconfigurations_tens[int(len(lconfigurations_tens) * 0.5):]


# Get 20% of S2 as validating data
lvalidation = S2[:int(len(lconfigurations_tens) * 0.2)]

# Use the rest 80% for training 
ltrain = S2[int(len(lconfigurations_tens) * 0.2):]


print('test_set:\t', len(S1))
print('validation_set:\t', len(lvalidation))
print('training_set:\t', len(ltrain))
print('sum val + train:\t', len(lvalidation) + len(ltrain))

print('all_data set: \t', len(lconfigurations_tens))


write(str(newpath + 'macefile_mixed_alldata_sets_test_set.xyz'), S1, format='extxyz')
write(str(newpath + 'macefile_mixed_alldata_sets_validation_set.xyz'), lvalidation, format='extxyz')
write(str(newpath + 'macefile_mixed_alldata_sets_training_set.xyz'), ltrain, format='extxyz')
write(str(newpath + 'macefile_mixed_alldata_sets.xyz'), lconfigurations_tens, format='extxyz')

