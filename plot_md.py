#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import chemcompute.common as common
import pickle 



# Open the file in binary mode 
with open('md_objects.pkl', 'rb') as file: 
    dfiles = pickle.load(file) 


N=340
kb=8.617e-5

lkeys = list(dfiles.keys())


with PdfPages('md_plot.pdf') as pdf:
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Metadata informations
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    d = pdf.infodict()
    d['Title'] = ''
    d['Author'] = 'A. TETENOIRE'


    """
    PLOT
    """

    for num, key in enumerate(dfiles.keys()): 
        print('Plot ts=%s' % key)
        # Plot

        fig=plt.figure(figsize=(10,6), dpi=600)
        ax = fig.add_subplot(111)

        y =dfiles[key]['potential_energy'] - dfiles[lkeys[0]]['potential_energy'][0]
        time_step = [dfiles[key]['writing_interval']*dfiles[key]['ts']*x for x in range(len(y))]
        ax.plot(time_step, y, label=str('ts=%s' %key))

        # Parameters
        # ax.xaxis.set_ticks(np.arange(0, 4.5, 0.5))
        # ax.set_xlim(0.8, 3.5)


        ax.tick_params(axis='both', which='major', length=5, width=2)
        ax.tick_params(axis='both', which='minor', length=2.5, width=1)

        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params(axis='both', labelsize=16)
        ax.minorticks_on()
        # ax.tick_params(axis='x', which='minor', bottom=False)


        # Change xtick labels

        # Set number of ticks for x-axis
        # ax.set_xticks(np.arange(len(key_df)) + 0.5)
        # Set ticks labels for x-axis
        # ax.set_xticklabels(key_df, rotation=45, fontsize=16)


        ax.set_xlabel('Timestep (fs)', fontsize=20)
        ax.set_ylabel('Potential energy (eV)', fontsize=20)

        ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncols=4)

        


        pdf.savefig(bbox_inches='tight')
        plt.close()



    """
    PLOT
    """

    # Plot

    fig=plt.figure(figsize=(10,6), dpi=600)
    ax = fig.add_subplot(111)

    print('Plot')
    for num, key in enumerate(dfiles.keys()): 
        
        y =dfiles[key]['potential_energy']- dfiles[lkeys[0]]['potential_energy'][0]
        time_step = [dfiles[key]['writing_interval']*dfiles[key]['ts']*x for x in range(len(y))]
        ax.plot(time_step, y, label=str('ts=%s' %key))


        # Parameters
        # ax.xaxis.set_ticks(np.arange(0, 4.5, 0.5))
        # ax.set_xlim(0.8, 3.5)


        ax.tick_params(axis='both', which='major', length=5, width=2)
        ax.tick_params(axis='both', which='minor', length=2.5, width=1)

        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params(axis='both', labelsize=16)
        ax.minorticks_on()
        # ax.tick_params(axis='x', which='minor', bottom=False)


        # Change xtick labels

        # Set number of ticks for x-axis
        # ax.set_xticks(np.arange(len(key_df)) + 0.5)
        # Set ticks labels for x-axis
        # ax.set_xticklabels(key_df, rotation=45, fontsize=16)


        ax.set_xlabel('Timestep (fs)', fontsize=20)
        ax.set_ylabel('Potential energy (eV)', fontsize=20)

        ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncols=4)

        


    pdf.savefig(bbox_inches='tight')
    plt.close()



    """
    PLOT
    """

    # Plot

    fig=plt.figure(figsize=(10,6), dpi=600)
    ax = fig.add_subplot(111)

    print('Plot')
    for num, key in enumerate(dfiles.keys()): 
        
        y =dfiles[key]['kinetic_energy'] - dfiles[lkeys[0]]['kinetic_energy'][0]
        time_step = [dfiles[key]['writing_interval']*dfiles[key]['ts']*x for x in range(len(y))]
        ax.plot(time_step, y, label=str('ts=%s' %key))


        # Parameters
        # ax.xaxis.set_ticks(np.arange(0, 4.5, 0.5))
        # ax.set_xlim(0.8, 3.5)


        ax.tick_params(axis='both', which='major', length=5, width=2)
        ax.tick_params(axis='both', which='minor', length=2.5, width=1)

        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params(axis='both', labelsize=16)
        ax.minorticks_on()
        # ax.tick_params(axis='x', which='minor', bottom=False)


        # Change xtick labels

        # Set number of ticks for x-axis
        # ax.set_xticks(np.arange(len(key_df)) + 0.5)
        # Set ticks labels for x-axis
        # ax.set_xticklabels(key_df, rotation=45, fontsize=16)


        ax.set_xlabel('Timestep (fs)', fontsize=20)
        ax.set_ylabel('Kinetic energy (eV)', fontsize=20)

        ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncols=4)

        


    pdf.savefig(bbox_inches='tight')
    plt.close()



    """
    PLOT
    """

    # Plot

    fig=plt.figure(figsize=(10,6), dpi=600)
    ax = fig.add_subplot(111)

    print('Plot')
    for num, key in enumerate(dfiles.keys()): 
        
        y =dfiles[key]['kinetic_energy'] * 2 / (3*N*kb)
        time_step = [dfiles[key]['writing_interval']*dfiles[key]['ts']*x for x in range(len(y))]
        ax.plot(time_step, y, label=str('ts=%s' %key))


        # Parameters
        # ax.xaxis.set_ticks(np.arange(0, 4.5, 0.5))
        # ax.set_xlim(0.8, 3.5)


        ax.tick_params(axis='both', which='major', length=5, width=2)
        ax.tick_params(axis='both', which='minor', length=2.5, width=1)

        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params(axis='both', labelsize=16)
        ax.minorticks_on()
        # ax.tick_params(axis='x', which='minor', bottom=False)


        # Change xtick labels

        # Set number of ticks for x-axis
        # ax.set_xticks(np.arange(len(key_df)) + 0.5)
        # Set ticks labels for x-axis
        # ax.set_xticklabels(key_df, rotation=45, fontsize=16)
        ax.set_yscale('log')

        ax.set_xlabel('Timestep (fs)', fontsize=20)
        ax.set_ylabel('Kinetic temperature energy (K)', fontsize=20)

        ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncols=4)

        


    pdf.savefig(bbox_inches='tight')
    plt.close()


    """
    PLOT
    """

    # Plot

    fig=plt.figure(figsize=(10,6), dpi=600)
    ax = fig.add_subplot(111)

    print('Plot')
    for num, key in enumerate(dfiles.keys()): 
        
        y =dfiles[key]['kinetic_energy'] + dfiles[key]['potential_energy'] - dfiles[lkeys[0]]['kinetic_energy'][0] - dfiles[lkeys[0]]['potential_energy'][0]
        time_step = [dfiles[key]['writing_interval']*dfiles[key]['ts']*x for x in range(len(y))]
        ax.plot(time_step, y, label=str('ts=%s' %key))


        # Parameters
        # ax.xaxis.set_ticks(np.arange(0, 4.5, 0.5))
        # ax.set_xlim(0.8, 3.5)


        ax.tick_params(axis='both', which='major', length=5, width=2)
        ax.tick_params(axis='both', which='minor', length=2.5, width=1)

        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.tick_params(axis='both', labelsize=16)
        ax.minorticks_on()
        # ax.tick_params(axis='x', which='minor', bottom=False)


        # Change xtick labels

        # Set number of ticks for x-axis
        # ax.set_xticks(np.arange(len(key_df)) + 0.5)
        # Set ticks labels for x-axis
        # ax.set_xticklabels(key_df, rotation=45, fontsize=16)


        ax.set_xlabel('Timestep (fs)', fontsize=20)
        ax.set_ylabel('Total energy (eV)', fontsize=20)

        ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncols=4)

        


    pdf.savefig(bbox_inches='tight')
    plt.close()




    # '''
    # Plot
    # '''
    # # ax = plt.subplot(111)
    # fig=plt.figure(figsize=(7,6), dpi=600)
    # ax = fig.add_subplot(111)


    # MINDEN  = 1         # uncomment to set range of colors
    # MAXDEN  = 1e4   # uncomment to set range of colors

    # lforces_x = []
    # for i in dfiles['from_scratch-t1']['forces']:
    #     lforces_x.extend(i[:, 0])
    # lforces_x = np.asarray(lforces_x)

    # x = np.asarray([np.arange(0, 12501) for i in range(340)]).flatten()
    # y =lforces_x

    # xmin, xmax = min(x), max(x)
    # ymin, ymax = min(y), max(y)
    # bin_width, bin_length = (max(x)-min(x))/1e2, (max(y)-min(y))/1e2


    # image=ax.hist2d(x=x, y=y ,cmap='jet',bins = [np.arange(xmin,xmax, bin_width), np.arange(ymin,ymax,bin_length)],norm=colors.LogNorm(vmin=MINDEN,vmax=MAXDEN)) # use with automatic boundaries and scalings




    # # axes properties
    # cbar=fig.colorbar(image[3],ax=ax, pad=0.02)
    # cbar.ax.tick_params(labelsize=12, length=5, width=2,direction='out')
    # cbar.set_label('Counts',size=20, rotation =-90, labelpad=20)

    # # ax.set_xlim(0, 4)
    # # ax.set_ylim(2, 14)
    # # ax.xaxis.set_ticks(np.arange(0, 4.5, 0.5))
    # # ax.yaxis.set_ticks(np.arange(2, 16, 2))

    # ax.tick_params(axis='both', labelsize=16)
    # ax.tick_params(axis='both', which='major', length=5, width=2)
    # ax.tick_params(axis='both', which='minor', length=2.5, width=1)

    # ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    # ax.yaxis.set_ticks_position('both')
    # ax.minorticks_on()

    # ax.set_xlabel('Time (ps)', fontsize=20)
    # ax.set_ylabel(r'Forces (eV/$\AA$)', fontsize=20)


    # pdf.savefig(bbox_inches='tight')
    # plt.close()
