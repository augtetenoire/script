# import dpdata
from dpdata import LabeledSystem, MultiSystems
import chemcompute.mace as macetools
import numpy as np
import os 
import tqdm
import glob
import random
import ase.io
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


lfolder = '/share/lcbcsrv9/lcbcdata/tetenoir/julien_lam/Extracted_outcar'


# load the list
lfiles = np.loadtxt('/share/lcbcsrv9/lcbcdata/tetenoir/julien_lam/outcarpath.dat', dtype=str)
folder_name = 'data_created_bis'
newpath = str('mace_data/%s/' % folder_name)
if not os.path.exists(newpath):
    os.makedirs(newpath)


# Load OUTCAR with dpdata
ms = MultiSystems()
for file in lfiles:
    try:
        ls = LabeledSystem(file, fmt='vasp/outcar') 
        ls.data['virials'] = np.zeros((ls.get_nframes(), 3, 3)) # this does the trick and mix data though they might have virial or not. I just give them virial of 0
    except:
        # ls = LabeledSystem() 
        print(file, '\t ERROR')
    if len(ls) > 0:
        ms.append(ls)

# Save multisystems in extended xyz form
for dsys in ms:
    name = dsys.formula
    latom_names = [dsys.__dict__['data']['atom_names'][x] for x in dsys.__dict__['data']['atom_types']]
    for i in tqdm.tqdm(range(len(dsys.__dict__['data']['energies']))):
        a = macetools.configuration(properties='species:S:1:pos:R:3:forces:R:3', latoms=latom_names, energy=dsys.__dict__['data']['energies'][i], lpos=dsys.__dict__['data']['coords'][i], lforces=dsys.__dict__['data']['forces'][i], pbc=['T', 'T', 'T'], lattice=dsys.__dict__['data']['cells'][i].flatten(), config_type=name, dihedral_angle=None)
        
        #if not os.path.isfile(str(newpath + 'macefile_%s.xyz' % name)):
        a.write_conf(str(newpath + 'macefile_%s.xyz' % name), mode='a')


# # Save all file in extxyz format
# for dsys in ms:
#     name = dsys.formula
#     latom_names = [dsys.__dict__['data']['atom_names'][x] for x in dsys.__dict__['data']['atom_types']]
#     for i in tqdm.tqdm(range(len(dsys.__dict__['data']['energies']))):
#         a = macetools.configuration(properties='species:S:1:pos:R:3:forces:R:3', latoms=latom_names, energy=dsys.__dict__['data']['energies'][i], lpos=dsys.__dict__['data']['coords'][i], lforces=dsys.__dict__['data']['forces'][i], pbc=['T', 'T', 'T'], lattice=dsys.__dict__['data']['cells'][i].flatten(), config_type=name, dihedral_angle=None)
        
#         #if not os.path.isfile(str(newpath + 'macefile_%s.xyz' % name)):
#         a.write_conf(str(newpath + 'macefile_alldata_set.xyz'), mode='a')









macefile_all_data = []
for i in glob.glob(str(newpath + 'macefile_*.xyz')):
    macefile_all_data.extend(macetools.read_extended_file(i))

# Shuffle data
random.shuffle(macefile_all_data)

# Split all into two sets of equal size
S1 = macefile_all_data[:int(len(macefile_all_data) * 0.5)]
S2 = macefile_all_data[int(len(macefile_all_data) * 0.5):]


# Get 20% of S2 as validating data
lvalidation = S2[:int(len(macefile_all_data) * 0.2)]

# Use the rest 80% for training 
ltrain = S2[int(len(macefile_all_data) * 0.2):]


print('test_set:\t', len(S1))
print('validation_set:\t', len(lvalidation))
print('training_set:\t', len(ltrain))
print('sum val + train:\t', len(lvalidation) + len(ltrain))

print('all_data set: \t', len(macefile_all_data))

for conf in tqdm.tqdm(S1):
    conf.write_conf(str(newpath + 'macefile_mixed_alldata_sets_test_set.xyz'), mode='a')
for conf in tqdm.tqdm(lvalidation):
    conf.write_conf(str(newpath + 'macefile_mixed_alldata_sets_validation_set.xyz'), mode='a')
for conf in tqdm.tqdm(ltrain):
    conf.write_conf(str(newpath + 'macefile_mixed_alldata_sets_training_set.xyz'), mode='a')
for conf in tqdm.tqdm(macefile_all_data):
    conf.write_conf(str(newpath + 'macefile_mixed_alldata_sets.xyz'), mode='a')











# file = str(newpath + 'macefile_alldata_set.xyz')
for macefile in ['macefile_Ru114.xyz', 'macefile_Ru256.xyz', 'macefile_Ru288.xyz', 'macefile_Ru55.xyz', 'macefile_Ru576.xyz']:
    file = str(newpath + macefile)
    filename = file.replace('.xyz', '')

    macefile_all_data = macetools.read_extended_file(file)

    # Shuffle data
    random.shuffle(macefile_all_data)

    # Split all into two sets of equal size
    S1 = macefile_all_data[:int(len(macefile_all_data) * 0.5)]
    S2 = macefile_all_data[int(len(macefile_all_data) * 0.5):]


    # Get 20% of S2 as validating data
    lvalidation = S2[:int(len(macefile_all_data) * 0.2)]

    # Use the rest 80% for training 
    ltrain = S2[int(len(macefile_all_data) * 0.2):]


    print('test_set:\t', len(S1))
    print('validation_set:\t', len(lvalidation))
    print('training_set:\t', len(ltrain))
    print('sum val + train:\t', len(lvalidation) + len(ltrain))

    print('all_data set: \t', len(macefile_all_data))

    for conf in tqdm.tqdm(S1):
        conf.write_conf(str(filename + '_test_set.xyz'), mode='a')
    for conf in tqdm.tqdm(lvalidation):
        conf.write_conf(str(filename + '_validation_set.xyz'), mode='a')
    for conf in tqdm.tqdm(ltrain):
        conf.write_conf(str(filename + '_training_set.xyz'), mode='a')










# Correct energy

denergies = {
    'Ru' : -0.74621405E+01,
}
file = str(newpath + 'macefile_mixed_alldata_sets.xyz')
a = ase.io.read(file, format='extxyz', index=':')
b = ase.io.read(file, format='extxyz', index=':')
for count, atom in enumerate(b):
    
    string = b[0].__dict__['info']['config_type']
    temp = re.split('(\d+)', string)
    
    # ditem = {'H':0, 'C':0, 'N':0, 'O':0, 'Mo':0}
    ditem = {'Ru':0}
    for num, i in enumerate(temp):
        if i in ditem.keys():
            ditem[i] = int(temp[num + 1])
    
    for key in ditem.keys():
        atom.__dict__['info']['REF_energy'] = atom.__dict__['info']['REF_energy'] - ditem[key] * denergies[key]

print(a[0].__dict__['info']['REF_energy']) # total energy
print(b[0].__dict__['info']['REF_energy']) # corrected energy







# for i in *.xyz ; do sed -i 's/energy/REF_energy/g' ${i} ; sed -i 's/forces/REF_forces/g' ${i} ;done






with PdfPages('plot_energie.pdf') as pdf:
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Metadata informations
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    d = pdf.infodict()
    d['Title'] = ''
    d['Author'] = 'A. TETENOIRE'




    """ 
    PLOT
    """

    fig=plt.figure(figsize=(10,6), dpi=600)
    ax = fig.add_subplot(111)
    
    for macefile in ['macefile_Ru114.xyz', 'macefile_Ru256.xyz', 'macefile_Ru288.xyz', 'macefile_Ru55.xyz', 'macefile_Ru576.xyz']:

        nb_atom = int(re.findall(r'\d+', macefile)[0])
        conf = ase.io.read(str(newpath + macefile), format='extxyz', index=':')
        array = np.asarray([x.__dict__['info']['REF_energy'] for x in conf]) / nb_atom
        # plt.hist(array[array < 0], bins = 100)
        plt.hist(array, bins = 100, label=macefile)


        ax.tick_params(axis='both', which='major', length=5, width=2)
        ax.tick_params(axis='both', which='minor', length=2.5, width=1)

        # ax.xaxis.set_ticks_position('both')
        ax.tick_params(axis='both', labelsize=16)
        ax.minorticks_on()
        # ax.tick_params(axis='x', which='minor', bottom=False)



        ax.set_xlabel('Energies (eV)', fontsize=20)
        ax.set_ylabel('Number of configuration (count)', fontsize=20)


        ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncols=4)
    

    pdf.savefig(bbox_inches='tight')
    plt.close()





    """ 
    PLOT
    """

    fig=plt.figure(figsize=(10,6), dpi=600)
    ax = fig.add_subplot(111)
    
    array = np.asarray([x.__dict__['info']['REF_energy'] for x in a])
    # plt.hist(array[array < 0], bins = 100)
    plt.hist(array, bins = 100)


    ax.tick_params(axis='both', which='major', length=5, width=2)
    ax.tick_params(axis='both', which='minor', length=2.5, width=1)

    # ax.xaxis.set_ticks_position('both')
    ax.tick_params(axis='both', labelsize=16)
    ax.minorticks_on()
    # ax.tick_params(axis='x', which='minor', bottom=False)



    ax.set_xlabel('Energies (eV)', fontsize=20)
    ax.set_ylabel('Number of configuration (count)', fontsize=20)


    # ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncols=4)
    

    pdf.savefig(bbox_inches='tight')
    plt.close()

    """ 
    PLOT
    """

    fig=plt.figure(figsize=(10,6), dpi=600)
    ax = fig.add_subplot(111)
    
    array = np.asarray([x.__dict__['info']['REF_energy'] for x in b])
    # plt.hist(array[array < 0], bins = 100)
    plt.hist(array, bins = 100)


    ax.tick_params(axis='both', which='major', length=5, width=2)
    ax.tick_params(axis='both', which='minor', length=2.5, width=1)

    # ax.xaxis.set_ticks_position('both')
    ax.tick_params(axis='both', labelsize=16)
    ax.minorticks_on()
    # ax.tick_params(axis='x', which='minor', bottom=False)



    ax.set_xlabel('Energies (eV)', fontsize=20)
    ax.set_ylabel('Number of configuration (count)', fontsize=20)


    # ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncols=4)
    

    pdf.savefig(bbox_inches='tight')
    plt.close()