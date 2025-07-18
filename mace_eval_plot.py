import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
# import sys
# import matplotlib.patches as patches
# import sklearn
# import matplotlib as mpl
from math import sqrt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from ase.io import read, write
from sys import argv


ref_file = argv[1]
output_file = argv[2]
data_width = 100

#######################
#   DATA Preparation  #
#######################

print("1st Stage: data preparation")

# Loading datasets
configurations = read(ref_file, index=':')

# Creation of energy sets
macetest_energies = [i.__dict__['info']['MACE_energy'] for i in configurations]
dfttest_energies =  [i.__dict__['info']['REF_energy'] for i in configurations]


# Creation of forces sets
dfttest_forces_x = []
dfttest_forces_y = []
dfttest_forces_z = []

for i in configurations:
    mace_test_allforces = i.__dict__['arrays']['REF_forces']
    dfttest_forces_x.extend(mace_test_allforces[:, 0])
    dfttest_forces_y.extend(mace_test_allforces[:, 1])
    dfttest_forces_z.extend(mace_test_allforces[:, 2])


macetest_forces_x = []
macetest_forces_y = []
macetest_forces_z = []


for i in configurations:
    mace_test_allforces = i.__dict__['arrays']['MACE_forces']
    macetest_forces_x.extend(mace_test_allforces[:, 0])
    macetest_forces_y.extend(mace_test_allforces[:, 1])
    macetest_forces_z.extend(mace_test_allforces[:, 2])

####  RMSE calculation ####
rmse_energy_test = sqrt(mean_squared_error(dfttest_energies, macetest_energies))
rmse_forces_x_test = sqrt(mean_squared_error(dfttest_forces_x, macetest_forces_x))
rmse_forces_y_test = sqrt(mean_squared_error(dfttest_forces_y, macetest_forces_y))
rmse_forces_z_test = sqrt(mean_squared_error(dfttest_forces_z, macetest_forces_z))

####  R2 calculation   ####
r2_energy_test = r2_score(dfttest_energies, macetest_energies)
r2_forces_x_test = r2_score(dfttest_forces_x, macetest_forces_x)
r2_forces_y_test = r2_score(dfttest_forces_y, macetest_forces_y)
r2_forces_z_test = r2_score(dfttest_forces_z, macetest_forces_z)

###########################
#    Plotting the data    #
###########################

print("2nd Stage: plotting data")


with PdfPages(output_file) as pdf:
    #### PLOT ENERGIES ####
    # Test energies
    fig = plt.figure(figsize=(7, 6), dpi=150)
    fig.suptitle("Evaluation of Test Energy", fontsize=25, fontweight='bold', x = 0.48)
    fig.subplots_adjust(top=0.85)
    ax = fig.add_subplot(111)
    MINDEN = 1  # uncomment to set range of colors
    MAXDEN = 1e4  # uncomment to set range of colors
    GAMMA = 1  # control contrast between colors: GAMMA=1 linear scaling

    x = dfttest_energies
    y = macetest_energies
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    bin_width, bin_length = (xmax-xmin)/data_width, (ymax-ymin)/data_width

    ax.plot(np.arange(xmin, xmax, 0.1), np.arange(xmin, xmax, 0.1), color='k', alpha=0.75)
    # Creating histogram
    print('3.2rd Stage: Creating Test energy histogram')
    image = ax.hist2d(x=x, y=y, cmap='jet', bins=[np.arange(xmin, xmax, bin_width), np.arange(ymin, ymax, bin_length)],
                      norm=colors.LogNorm(vmin=MINDEN, vmax=MAXDEN))  # use with automatic boundaries and scalings
    # axes properties
    cbar = fig.colorbar(image[3], ax=ax, pad=0.02)
    cbar.ax.tick_params(labelsize=12, length=5, width=2, direction='out')
    cbar.set_label('Counts', size=20, rotation=-90, labelpad=20)
    axis_energy_test = "RMSE:" + " " + str(round(rmse_energy_test, 3)) + "   " + "R2:" + " " + str(round(r2_energy_test,3))
    ax.set_title(axis_energy_test, fontsize=10, pad = 15)
    ax.tick_params(axis='both', labelsize=16)
    ax.tick_params(axis='both', which='major', length=5, width=2)
    ax.tick_params(axis='both', which='minor', length=2.5, width=1)
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.minorticks_on()
    ax.set_xlabel('DFT energies (eV)', fontsize=20)
    ax.set_ylabel('MACE energies (eV)', fontsize=20)
    pdf.savefig(bbox_inches='tight')
    plt.close()

    #### PLOT FORCES ####
    # Test forces on x
    fig = plt.figure(figsize=(7, 6), dpi=150)
    fig.suptitle("Evaluation of Test Forces on X", fontsize=25, fontweight='bold', x = 0.48)
    fig.subplots_adjust(top=0.85)
    ax = fig.add_subplot(111)

    MINDEN = 1  # uncomment to set range of colors
    MAXDEN = 1e4  # uncomment to set range of colors
    GAMMA = 1  # control contrast between colors: GAMMA=1 linear scaling

    x = dfttest_forces_x
    y = macetest_forces_x

    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    bin_width, bin_length = (xmax-xmin)/data_width, (ymax-ymin)/data_width
    ax.plot(np.arange(xmin, xmax, 0.1), np.arange(xmin, xmax, 0.1), color='k', alpha=0.75)

    print('4.2th Stage: Creating Test forces on x histogram')
    image = ax.hist2d(x=x, y=y, cmap='jet', bins=[np.arange(xmin, xmax, bin_width), np.arange(ymin, ymax, bin_length)],
                      norm=colors.LogNorm(vmin=MINDEN, vmax=MAXDEN))  # use with automatic boundaries and scalings

    # axes properties
    cbar = fig.colorbar(image[3], ax=ax, pad=0.02)
    cbar.ax.tick_params(labelsize=12, length=5, width=2, direction='out')
    cbar.set_label('Counts', size=20, rotation=-90, labelpad=20)
    axis_forces_x_test = "RMSE:" + " " + str(round(rmse_forces_x_test,3)) + "   " + "R2:" + " " + str(round(r2_forces_x_test,3))
    ax.set_title(axis_forces_x_test, fontsize=10, pad = 15)
    ax.tick_params(axis='both', labelsize=16)
    ax.tick_params(axis='both', which='major', length=5, width=2)
    ax.tick_params(axis='both', which='minor', length=2.5, width=1)
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.minorticks_on()
    ax.set_xlabel('DFT Forces on x (eV)', fontsize=20)
    ax.set_ylabel('MACE Forces on x (eV)', fontsize=20)
    pdf.savefig(bbox_inches='tight')
    plt.close()

    # Test forces on y
    fig = plt.figure(figsize=(7, 6), dpi=150)
    fig.suptitle("Evaluation of Test Forces on Y", fontsize=25, fontweight='bold', x = 0.48)
    fig.subplots_adjust(top=0.85)
    ax = fig.add_subplot(111)

    MINDEN = 1  # uncomment to set range of colors
    MAXDEN = 1e4  # uncomment to set range of colors
    GAMMA = 1  # control contrast between colors: GAMMA=1 linear scaling

    x = dfttest_forces_y
    y = macetest_forces_y

    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    bin_width, bin_length = (xmax-xmin)/data_width, (ymax-ymin)/data_width
    ax.plot(np.arange(xmin, xmax, 0.1), np.arange(xmin, xmax, 0.1), color='k', alpha=0.75)

    print('5.2th Stage: Creating Test forces on y histogram')
    image = ax.hist2d(x=x, y=y, cmap='jet', bins=[np.arange(xmin, xmax, bin_width), np.arange(ymin, ymax, bin_length)],
                      norm=colors.LogNorm(vmin=MINDEN, vmax=MAXDEN))  # use with automatic boundaries and scalings

    # axes properties
    cbar = fig.colorbar(image[3], ax=ax, pad=0.02)
    cbar.ax.tick_params(labelsize=12, length=5, width=2, direction='out')
    cbar.set_label('Counts', size=20, rotation=-90, labelpad=20)
    axis_forces_y_test = "RMSE:" + " " + str(round(rmse_forces_y_test, 3)) + "   " + "R2:" + " " + str(round(r2_forces_y_test, 3))
    ax.set_title(axis_forces_y_test, fontsize=10, pad = 15)
    ax.tick_params(axis='both', labelsize=16)
    ax.tick_params(axis='both', which='major', length=5, width=2)
    ax.tick_params(axis='both', which='minor', length=2.5, width=1)
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.minorticks_on()
    ax.set_xlabel('DFT Forces on y (eV)', fontsize=20)
    ax.set_ylabel('MACE Forces on y (eV)', fontsize=20)
    pdf.savefig(bbox_inches='tight')
    plt.close()

    # Test forces on z
    fig = plt.figure(figsize=(7, 6), dpi=150)
    fig.suptitle("Evaluation of Test Forces on Z", fontsize=25, fontweight='bold', x = 0.48)
    fig.subplots_adjust(top=0.85)
    ax = fig.add_subplot(111)

    MINDEN = 1  # uncomment to set range of colors
    MAXDEN = 1e4  # uncomment to set range of colors
    GAMMA = 1  # control contrast between colors: GAMMA=1 linear scaling

    x = dfttest_forces_z
    y = macetest_forces_z

    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    bin_width, bin_length = (xmax-xmin)/data_width, (ymax-ymin)/data_width
    ax.plot(np.arange(xmin, xmax, 0.1), np.arange(xmin, xmax, 0.1), color='k', alpha=0.75)

    print('6.2th Stage: Creating Test forces on z histogram')
    image = ax.hist2d(x=x, y=y, cmap='jet', bins=[np.arange(xmin, xmax, bin_width), np.arange(ymin, ymax, bin_length)],
                      norm=colors.LogNorm(vmin=MINDEN, vmax=MAXDEN))  # use with automatic boundaries and scalings

    # axes properties
    cbar = fig.colorbar(image[3], ax=ax, pad=0.02)
    cbar.ax.tick_params(labelsize=12, length=5, width=2, direction='out')
    cbar.set_label('Counts', size=20, rotation=-90, labelpad=20)
    axis_forces_z_test = "RMSE:" + " " + str(round(rmse_forces_z_test, 3)) + "   " + "R2:" + " " + str(round(r2_forces_z_test, 3))
    ax.set_title(axis_forces_z_test, fontsize=10, pad = 15)
    ax.tick_params(axis='both', labelsize=16)
    ax.tick_params(axis='both', which='major', length=5, width=2)
    ax.tick_params(axis='both', which='minor', length=2.5, width=1)
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.minorticks_on()
    ax.set_xlabel('DFT Forces on z (eV)', fontsize=20)
    ax.set_ylabel('MACE Forces on z (eV)', fontsize=20)
    pdf.savefig(bbox_inches='tight')
    plt.close()
