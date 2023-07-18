import sys
import numpy as np
# from os import listdir
# from os.path import isfile, join
from os.path import basename
from glob import glob

if len(sys.argv) < 4:
    print('\nERROR: missing arguments.')
    print('Please specify the directory where the modes are stored, then the amount of modes you wanna spot, then the number of the atom you are looking for in the file.\n')
    sys.exit()

print('\n!! The format of the atom to be found is Ex: C182 for carbon and atom number 182 !!\n')
directory = sys.argv[1]
max_total = int(sys.argv[2])
find_atom = str(sys.argv[3])

all_files = glob(str(directory + '/mode_*.xyz'))
# all_files = [f for f in listdir(directory) if isfile(join(directory, f))]
print('Reading files\n')
final_of_final = []
lmodes_delta = []
for file in all_files:
    with open(file) as fp:
        xyz_data = fp.readlines()
        xyz_data.pop(0)
        xyz_data.pop(0)

    atom_coord = []
    n = 1
    for data in xyz_data:
        try:
            name = '{}{}'.format(data.split()[0], n)
            x_coord = float(data.split()[1])
            y_coord = float(data.split()[2])
            z_coord = float(data.split()[3])
            position = np.sqrt((x_coord**2) + (y_coord**2) + (z_coord**2))
            if name == find_atom:
                atom_coord.append([position])
            n += 1
        except:
            n = 0


    delta_of_mode = max([np.ab(atom_coord[0] - i) for i in atom_coord])
    lmodes_delta.append([file, delta_of_mode])


    # all_xyz = np.array_split(atoms_coord, 30)
    # all_xyz = np.asarray(all_xyz)

    # a = (zip(*all_xyz))
    # a = list(a)
    # delta_list = []
    # for atom in a:
    #     delta = float(max(map(lambda x: x[1], atom))) - float(min(map(lambda x: x[1], atom)))
    #     delta_list.append([atom[0][0], delta, file])

    # final = sorted(delta_list, key=lambda x: x[1], reverse=True)
    # final_of_final += final


print('Sorting atoms\n')
test = sorted(final_of_final, key=lambda x: x[1], reverse=True)
found_atom = []
for data in test:
    if find_atom == data[0]:
        found_atom.append(data)
sorted_found_atom = sorted(found_atom, key=lambda x: x[1], reverse=True)
for t in sorted_found_atom[:max_total]:
    print('Mode: {}'.format(basename(t[2])), 'Atom: {}'.format(t[0]), 'Value: {:e} A'.format(t[1]))


