# import matplotlib.pyplot as plt 
from autoadsorbate import Fragment, Surface,get_drop_snapped \
# , docs_plot_conformers, get_marked_smiles, docs_plot_sites, _example_config,  construct_smiles
from autoadsorbate.Surf import attach_fragment
# from ase.visualize.plot import plot_atoms
# from ase.visualize import view
from ase import Atoms, Atom
import ase.io 
import numpy as np
# import pickle
import os
import os.path
# import copy
from dscribe.descriptors import SOAP
from mace.calculators import MACECalculator




"""
Variables
"""

nb_init = 1
slab_path = 'POSCAR_Mo5N6_surface'
height_ads = 1.6
calculator = MACECalculator(model_path='/share/lcbcsrv9/lcbcdata/tetenoir/github/mace-foundations/mace_matpes_0/MACE-matpes-pbe-omat-ft.model', device='cpu')


"""
Create the slab and get the adsorption sites
"""

slab = ase.io.read(slab_path, format='vasp', index=0)  # load slab file as ase.Atoms object
slab.positions = ase.geometry.wrap_positions(slab.positions, slab.cell, pbc=True, center=(0.5, 0.5, 0.5), pretty_translation=False, eps=1e-07)
s2 = Surface(slab)   


"""
Remove duplicated adsorption sites using SOAP descriptor and removing the ones that are too close (0.1) to the other site in terms of euclidian distance 
"""



species = ["N", "Mo"]
r_cut = 6.0
n_max = 8
l_max = 6

# Setting up the SOAP descriptor
soap = SOAP(
    species=species,
    periodic=True,
    r_cut=r_cut,
    n_max=n_max,
    l_max=l_max,
)


# Get site centers
centers = np.asarray([s2.site_df.iloc[i].coordinates for i in range(len(s2.site_df))])
# Create SOAP matrix
coulomb_matrices = soap.create(slab, centers, n_jobs=24)


def metric(lvalues, reference):
    """
    Compare Euclidian distance between two vectors
    """
    ldist = [np.linalg.norm(value - reference) for value in lvalues]
    dist_max = np.max(ldist)
    return  (ldist / dist_max)


# Compare all the sites
lindex_same = []
for i in range(len(s2.site_df)):
    
    ldiff = metric(coulomb_matrices, coulomb_matrices[i])
   
    # compare the distance and note the sites that are the same with a distance of 0.1 in scaled metric
    # for j in range(i, len(ldiff)):
        # if (ldiff[j] <= 0.1) and ( ldiff[j] > 0):
    for j in range(i+1, len(ldiff)):
        if (ldiff[j] <= 0.1):
            lindex_same.append(j)

# remove diplicate
lindex_same = list(dict.fromkeys(lindex_same))
lindex_same.sort()

s2.site_df = s2.site_df.drop(lindex_same)



"""
Create Fragment list
"""


CO_fragments = [
    Fragment('ClC#[O+]', to_initialize=nb_init), # CO n1 
    Fragment('S1SC1=O', to_initialize=nb_init), # CO n2 C in bridge
    # Fragment('S1S[C--]O1', to_initialize=nb_init), # CO n2 horizontal
    # Fragment('[Cl+]1[C-]=[O+]1', to_initialize=nb_init), # CO n1 horizontal
]

H2O_fragments = [
    # Fragment('Cl[H-](O[H])', to_initialize=nb_init), # H20 n1 H attached
    # Fragment('Cl[O+]([H])[H]', to_initialize=nb_init), # H20 n1 O attached
    # # Fragment('Cl1O([H])[H-]1', to_initialize=nb_init), # H20 n1 OH attached
    # Fragment('S1S[O++]1([H])[H]', to_initialize=nb_init), # H20 n2 O attached
    # Fragment('S1S[H--]1(O[H])', to_initialize=nb_init), # H20 n2 H attached
    # Fragment('S1S[H-][O+]1([H])', to_initialize=nb_init), # H2O n2 OH attached
]

HO_fragments = [
    # Fragment('ClO', to_initialize=nb_init), # OH n1
    # Fragment('S1S[O][H-]1', to_initialize=nb_init), # OH n2
    # Fragment('S1S[O+]1([H])', to_initialize=nb_init), # OH n2
]

H_fragments = [
    # Fragment('Cl', to_initialize=nb_init), # H n1
    #  Fragment('S1S[H]1', to_initialize=nb_init), # H n2 H in bridge
]

O_fragments = [
    # Fragment('Cl', to_initialize=nb_init), # H n1
    #  Fragment('S1S[H]1', to_initialize=nb_init), # H n2 H in bridge
]

H2_fragments = [
    # Fragment('Cl', to_initialize=nb_init), # H n1
]


CO2_fragments = [
    # Fragment('ClC(=O)[O-]', to_initialize=nb_init), # CO2 n1
    # Fragment('S1SC1([O-])[O-]', to_initialize=nb_init), # CO2 n2 C in bridge
    # Fragment('S1SC(=O)O1', to_initialize=nb_init), # CO2 n2 CO bridge
]

COOH_fragments = [
    # Fragment('S1SC(=[OH+])O1', to_initialize=nb_init), # COOH n2 CO in bridge
    # Fragment('S1SC(=[OH++]1)[O-]', to_initialize=nb_init), # COOH n2 C in bridge
    # Fragment('ClC(=O)O', to_initialize=nb_init), # COOH n1
]



llabel = ['CO', 'H2O']
lfragment = [CO_fragments, H2O_fragments]

# llabel = ['CO', 'H2O', 'HO', 'H', 'O', 'H2', 'CO2', 'COOH']
# lfragment = [CO_fragments, H2O_fragments, HO_fragments, H_fragments, O_fragments, H2_fragments, CO2_fragments, COOH_fragments]


"""
Create the Fragments based on smiles
"""

lconformers = []
lconformations = []
for index in range(len(lfragment)):
    print(llabel[index])
    out_trj = []
    for  i, fragment in enumerate(lfragment[index]):
        print('Fragment %i' %i)
        # out_trj = []
        for site_nb in range(len(s2.site_df)):
            site =s2.site_df.iloc[site_nb].to_dict()
            f = fragment.get_conformer(0)
            """
            Rotate the conformer
            """
            # loop from 0 to 4 * 45° roation
            for rot_index in range(0,5):
                # loop x, y ,z axis
                for axes in ['x', 'y', 'z']:
                    if 'S1S' in f.info["smiles"]:
                        f_rot = f[2:].copy()
                        # print(f)
                        # print(f_rot)
                        
                        f_rot.rotate(45*rot_index, axes, center=f_rot.get_center_of_mass())
                        f_rot = Atoms(list(f[:2]) + list(f_rot))
                    elif 'Cl' in f.info["smiles"]:
                        f_rot = f[1:].copy()
                        # print(f)
                        # print(f_rot)
                        
                        f_rot.rotate(45*rot_index, axes, center=f_rot.get_center_of_mass())
                        f_rot = Atoms(list(f[:1]) + list(f_rot))
                    

                    # Save conformers
                    lconformers.append(f_rot)
                    out_trj.append(attach_fragment(slab.copy(), site, f_rot, n_rotation=0, height=height_ads))
            # lconformers.append(f)
            # out_trj.append(attach_fragment(slab.copy(), site, f, n_rotation=0, height=height_ads))
        
        # Save all configurations
        print('Number conformation : %i' % len(out_trj))
        ase.io.write('configuration_%s_%i_presorted.xyz' % (llabel[index], i), out_trj, format='extxyz')

        """
        SOAP on the molecule mass center environment and remove the similar ones (vector distance < 0.1)
        """
        # paramerize SOAP descriptor
        species = list(dict.fromkeys(out_trj[0].get_chemical_symbols()))

        r_cut = 6.0
        n_max = 8
        l_max = 6

        # Setting up the SOAP descriptor
        soap = SOAP(
            species=species,
            periodic=True,
            r_cut=r_cut,
            n_max=n_max,
            l_max=l_max,
        )

        # Get site centers
        centers = np.asarray([atoms.get_center_of_mass() for atoms in out_trj])
        # Create SOAP matrix
        coulomb_matrices = soap.create(slab, centers, n_jobs=24)

        # loop over the configuration to find the silimar ones
        lindex_same = []
        for center in range(len(centers)):
            
            ldiff = metric(coulomb_matrices, coulomb_matrices[center])
        
            # compare the distance and note the sites that are the same with a distance of 0.1 in scaled metric
            for j in range(center + 1, len(ldiff)):
                if (ldiff[j] <= 0.1):
                    lindex_same.append(j)

        # remove diplicate
        lindex_same = list(dict.fromkeys(lindex_same))
        lindex_same.sort()
        out_trj = [out_trj[x] for x in range(len(out_trj)) if x not in lindex_same]


        # Save informations
        print('Number conformation SOAP sorted: %i' % len(out_trj))
        lconformations.extend(out_trj)
        ase.io.write('configuration_%s_%i_soap_sorted.xyz' % (llabel[index], i), out_trj, format='extxyz')
        # ase.io.write('%s_%i_XDATCAR' % (llabel[index], i), out_trj, format='vasp-xdatcar')


        """
        SCF compute the system with matpes-pbe
        """

        energies = []
        forces = []
        # lconf = [lconformations[i] for i in [0, 100, 200, 300, 400, 500, 600]]
        # for conf in lconf:
        for conf in out_trj:
            conf.calc = calculator
            energies.append(conf.get_potential_energy())
            forces.append(conf.get_forces())
            
        forces_norm = []
        for force in forces:
            forces_norm.append(np.asarray([np.linalg.norm(x) for x in force]))

        total_forces_norm = np.asarray([np.linalg.norm(x) for x in forces])

        """
        Sort and remove the high forces (> mean+ std*2)
        """
        to_remove = []
        threshold = np.std(total_forces_norm) * 2 + np.mean(total_forces_norm)
        for forces_index in range(len(total_forces_norm)):
            if total_forces_norm[forces_index] >= threshold:
                to_remove.append(forces_index)
        to_remove.reverse()
        
        for index_remove in to_remove:
            del out_trj[index_remove]


        print('Number conformation SOAP and Forces sorted: %i' % len(out_trj))
        ase.io.write('configuration_%s_%i_soap_forces_sorted.xyz' % (llabel[index], i), out_trj, format='extxyz')

        """
        Create POSCAR for calculations
        """
        folder = str(llabel[index] + '_%i' %  i)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        for num, conf in enumerate(out_trj):
            ase.io.write(str(folder + '/POSCAR_%i' % num), conf, format='vasp')

    ase.io.write('configuration_%s.xyz' % llabel[index], out_trj, format='extxyz')
    # ase.io.write('%s_XDATCAR' % llabel[index], out_trj, format='vasp-xdatcar')

    # out_trj_droped = get_drop_snapped(out_trj, d_cut=0.5)
    # ase.io.write('configuration_droped_%s.xyz' % llabel[index], out_trj, format='extxyz')
    # ase.io.write('%s_droped_XDATCAR' % llabel[index], out_trj_droped, format='vasp-xdatcar')






