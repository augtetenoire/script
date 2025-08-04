from ase.io import read, write
import numpy as np
import tqdm

# Create an Atom object combining the reading from the forces, energy and infos (timestep) of xyz and position of pdb

energy_file = 'position.pdb'
force_file = 'forces.xyz'

print('Loading Energy file')
atoms_energies = read(energy_file, index=':')
print('Loading Force file')
atoms_forces = read(force_file, index=':')

print('Processing Atoms objects')
new_atoms= atoms_energies.copy()
for num, atom in enumerate(tqdm.tqdm(new_atoms)):

    # Forces
    # 1 Ha/Bohr  =  51.422086 ev/angstrom; 1 ev/angstrom  =  0.0194469 Ha/Bohr
    atom.__dict__['arrays']['REF_forces'] = atoms_forces[num].__dict__['arrays']['positions'] * 51.422086 #converting Hartree/Bohr to eV/A

    # Energy
    atom.__dict__['info']['REF_energy'] = float(atoms_forces[num].__dict__['info']['E']) *  27.2114 #converting from Hartree to eV

    # Info (timestep)
    atom.__dict__['info']['step'] = int(atoms_forces[num].__dict__['info']['i'])
    atom.__dict__['info']['time'] = float(atoms_forces[num].__dict__['info']['time'])


    # Remove useless infos
    atom.__dict__['arrays'].pop('residuenames')
    atom.__dict__['arrays'].pop('bfactor')
    atom.__dict__['arrays'].pop('occupancy')



# Get duplicated with timestep

lstep = [x.__dict__['info']['step'] for x in new_atoms]
d = {}
for i, num in enumerate(lstep):
    if num in d:
        d[num].append(i)
    else:
        d[num] = [i]

# Filter to keep only the numbers with more than one occurrence
ans = {key: value for key, value in d.items() if len(value) > 1}

# Create a list of the index of the duplicated
lremove = []
for key in ans.keys():
    lremove.extend(ans[key][1:])

lremove.reverse()

# Remove duplicated
for i in lremove:
    new_atoms.pop(i)


outputfile = 'mace_format_SnO2_hyd.xyz'
write(outputfile, new_atoms, format='extxyz')

print('File %s created' % outputfile)

