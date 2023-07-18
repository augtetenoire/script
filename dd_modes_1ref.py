import sys
import numpy as np
# from os import listdir
# from os.path import isfile, join
from os.path import basename
from glob import glob
import re
import time
from joblib import Parallel, delayed
import multiprocessing

# t0 = time.time()

# if len(sys.argv) < 4:
#     print('\nERROR: missing arguments.')
#     print('Please specify the directory where the modes are stored, then the amount of modes you wanna spot, then the number of the atom you are looking for in the file.\n')
#     sys.exit()

# print('\n!! The format of the atom to be found is Ex: C182 for carbon and atom number 182 !!\n')
# directory = sys.argv[1]
# max_total = int(sys.argv[2])
# find_atom = str(sys.argv[3])

# all_files = glob(str(directory + '/mode_*.xyz'))
# # all_files = [f for f in listdir(directory) if isfile(join(directory, f))]
# print('Reading files\n')
# lmodes_delta = []
# dmodes= {}
# for file in all_files:
#     with open(file) as fp:
#         xyz_data = fp.readlines()
#         nb_atoms = int(xyz_data[0])
#         nb_lines = int(len(xyz_data))
#         nb_of_atom_to_find = int(re.findall(r'\d+', find_atom)[0])
#         xyz_data.pop(0)
#         xyz_data.pop(0)

#     ldistances = []
#     latom_coord = []
#     n = 0
#     x_ref = float(xyz_data[nb_of_atom_to_find].split()[1])
#     y_ref = float(xyz_data[nb_of_atom_to_find].split()[2])
#     z_ref = float(xyz_data[nb_of_atom_to_find].split()[3])
#     for data in xyz_data:
#         name = '{}{}'.format(data.split()[0], n)
#         try:
#             x_coord = float(data.split()[1])
#             y_coord = float(data.split()[2])
#             z_coord = float(data.split()[3])
#             atom_coord = [x_coord, y_coord, z_coord]
#             distance = np.sqrt(((x_coord - x_ref)**2) + ((y_coord - y_ref)**2) + ((z_coord - z_ref)**2))
#             if name == find_atom:
#                 ldistances.append(distance)
#                 latom_coord.append(atom_coord)
#             n += 1
#         except:
#             n = 0


#     dmodes[basename(file)] = [np.asarray(ldistances), np.asarray(latom_coord)]
#     lmodes_delta.append((basename(file), max(ldistances)))



# sorted_lmodes_delta = sorted(lmodes_delta, key=lambda x: x[1], reverse=True)



# for t in sorted_lmodes_delta[:max_total]:
#     print('Mode: {}'.format(t[0]), 'Atom: {}'.format(find_atom), 'Value: {:e} A'.format(t[1]))



# t1 = time.time()

# print('Total time (s):\t', t1-t0)




t0 = time.time()

if len(sys.argv) < 4:
    print('\nERROR: missing arguments.')
    print('Please specify the directory where the modes are stored, then the amount of modes you wanna spot, then the number of the atom you are looking for in the file.\n')
    sys.exit()

print('\n!! The format of the atom to be found is Ex: C182 for carbon and atom number 182 !!\n')
directory = sys.argv[1]
max_total = int(sys.argv[2])
find_atom = str(sys.argv[3])

# all_files = [f for f in listdir(directory) if isfile(join(directory, f))]
print('Reading files\n')



all_files = glob(str(directory + '/mode_*.xyz'))
def computing(file, find_atom):
    lmodes_delta = []
    dmodes= {}
    with open(file) as fp:
        xyz_data = fp.readlines()
        # nb_atoms = int(xyz_data[0])
        # nb_lines = int(len(xyz_data))
        nb_of_atom_to_find = int(re.findall(r'\d+', find_atom)[0])
        xyz_data.pop(0)
        xyz_data.pop(0)

    ldistances = []
    latom_coord = []
    n = 0
    x_ref = float(xyz_data[nb_of_atom_to_find].split()[1])
    y_ref = float(xyz_data[nb_of_atom_to_find].split()[2])
    z_ref = float(xyz_data[nb_of_atom_to_find].split()[3])
    for data in xyz_data:
        name = '{}{}'.format(data.split()[0], n)
        try:
            x_coord = float(data.split()[1])
            y_coord = float(data.split()[2])
            z_coord = float(data.split()[3])
            atom_coord = [x_coord, y_coord, z_coord]
            distance = np.sqrt(((x_coord - x_ref)**2) + ((y_coord - y_ref)**2) + ((z_coord - z_ref)**2))
            if name == find_atom:
                ldistances.append(distance)
                latom_coord.append(atom_coord)
            n += 1
        except:
            n = 0


    dmodes[basename(file)] = [np.asarray(ldistances), np.asarray(latom_coord)]
    lmodes_delta.append((basename(file), max(ldistances)))

    return dmodes, lmodes_delta

num_cores = multiprocessing.cpu_count()

temp = Parallel(n_jobs=num_cores)(delayed(computing)(i, find_atom) for i in all_files)


lmodes_delta = []
dmodes= {}
for i in temp:
    dmodes[list(i[0].keys())[0]] = list(i[0].values())[0]
    lmodes_delta.extend(i[1])

sorted_lmodes_delta = sorted(lmodes_delta, key=lambda x: x[1], reverse=True)



for t in sorted_lmodes_delta[:max_total]:
    print('Mode: {}'.format(t[0]), 'Atom: {}'.format(find_atom), 'Value: {:e} A'.format(t[1]))






t1 = time.time()

print('Total time (s):\t', t1-t0)




