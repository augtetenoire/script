import numpy as np
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages



# Define some constant
Na = 6.022140e23 # (mol)
kb_jk = 1.380649e-23 # (J/K)
kb_evk = 8.617330e-5 # (eV/K)

# Unit converter functions
def au2ev(x):
    # 1 au = 27.211324 (eV)
    return x * 27.211324
def au2kj(x):
    # 1 au 	= 4.359744e-21  (kJ)
    return x * 4.359744e-21
def au2kcal(x):
    # 1 au 	= 1.042003e-21  (kcal)
    return x * 1.042003e-21


energies_au = np.loadtxt('extracted_energies.out')
energies_ev = au2ev(energies_au)

gradient_norm_au = np.loadtxt('extracted_gradient_norm.out')



def plot_energy_gradient(energy, gradient, label_e):

    fig=plt.figure(figsize=(7,6), dpi=600)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    # Plot
    ax1.plot(energy, linewidth=2, label='Energy', color='r')
    ax2.plot(gradient, linewidth=2, label='Gradient', color='b')

    # Parameters
    # ax.set_xlim(0, 4)
    # ax.set_ylim(2, 14)
    # ax.xaxis.set_ticks(np.arange(0, 4.5, 0.5))
    # ax.yaxis.set_ticks(np.arange(2, 16, 2))
    
    ax2.set_yscale('log')



    # ax1.set_xlim(0, 4.05)
    # ax1.set_ylim(0, 6)
    # ax2.set_ylim(0, max_y)

    # ax1.xaxis.set_ticks(np.arange(0, 4.5, 0.5))
    # ax1.yaxis.set_ticks(np.arange(0, 7, 1))
    # ax2.yaxis.set_ticks(np.arange(0, max_y + 1, 1))


    ax1.tick_params(axis='both', which='major', length=5, width=2)
    ax1.tick_params(axis='both', which='minor', length=2.5, width=1)
    ax2.tick_params(axis='both', which='major', length=5, width=2)
    ax2.tick_params(axis='both', which='minor', length=2.5, width=1)

    ax1.xaxis.set_ticks_position('both')
    ax1.tick_params(axis='both', labelsize=16)
    ax2.tick_params(axis='both', labelsize=16)
    ax1.minorticks_on()
    ax2.minorticks_on()





    # ax.tick_params(axis='both', labelsize=16)
    # ax.tick_params(axis='both', which='major', length=5, width=2)
    # ax.tick_params(axis='both', which='minor', length=2.5, width=1)

    # ax.xaxis.set_ticks_position('both')
    # ax.yaxis.set_ticks_position('both')
    # ax.minorticks_on()

    ax1.set_xlabel('Number of step (count)', fontsize=20)
    ax1.set_ylabel(label_e, fontsize=20)
    ax2.set_ylabel('Gradient norm (H/au)', fontsize=20, rotation =-90, labelpad=25)

    # ax.legend(fontsize=10, ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.15), frameon=False,  labelspacing=0.2, handletextpad=0.2, columnspacing=1)   
    # ax1.legend(fontsize=10, loc='upper right', bbox_to_anchor=(0.9, 1), frameon=False)

    l1, h1 = ax1.get_legend_handles_labels()
    l2, h2 = ax2.get_legend_handles_labels()
    label = l1 + l2
    handle = h1 + h2

    plt.legend(label, handle, fontsize=16, loc='upper right', bbox_to_anchor=(0.9, 1), frameon=False)

   

with PdfPages('dftb_plus_output_analysis.pdf') as pdf:
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Metadata informations
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    d = pdf.infodict()
    d['Title'] = ''
    d['Author'] = 'A. TETENOIRE'


 
    '''
    Plot
    '''
    plot_energy_gradient(energies_au, gradient_norm_au, label_e='Energy (au)')

    pdf.savefig(bbox_inches='tight')
    plt.close()

    '''
    Plot
    '''
    plot_energy_gradient(energies_ev, gradient_norm_au, label_e='Energy (eV)')

    pdf.savefig(bbox_inches='tight')
    plt.close()
