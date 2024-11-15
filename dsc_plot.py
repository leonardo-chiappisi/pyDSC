#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 18:58:51 2018
@author: chiappisil
File where the functions used to plot all the data are stored. 
"""

import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import os

plt.rcParams['text.usetex'] = False

def plot_raw_data(files, data, params, filename):
    ''' Plots the raw_data'''
    
    print('\n', 15*'*', 'Plotting the raw data', 15*'*')
    # print(params)
    def applyPlotStyle(title, idx):
        if params['unit_temp'] == 'degC':
            axes[idx[0], idx[1]].set_xlabel('Temperature / °C')
        if params['unit_temp'] == 'K':
            axes[idx[0], idx[1]].set_xlabel('Temperature / K')
        if params['unit_power'] == 'uW':
            axes[idx[0], idx[1]].set_ylabel('Heat flow / 10$^{-6}$ W')
        elif params['unit_power'] == 'mW':
            axes[idx[0], idx[1]].set_ylabel('Heat flow / 10$^{-3}$ W')
        elif params['unit_power'] == 'W':
            axes[idx[0], idx[1]].set_ylabel('Heat flow / W')
            
        axes[idx[0], idx[1]].set_title(title)
        #axes[idx[0], idx[1]].legend(loc='upper left')
        if params['Exo_in_plot'] is True:
            if params['Input'] == 'exo-down':
                axes[idx[0], idx[1]].annotate('Exo-down', xy=(0.1, 0.05), xytext=(0.1, 0.25), xycoords = 'axes fraction',
                         arrowprops=dict(arrowstyle='->'), 
                         horizontalalignment='center')
            if params['Input'] == 'exo-up':
                axes[idx[0], idx[1]].annotate('Exo-up', xy=(0.1, 0.25), xytext=(0.1, 0.05), xycoords = 'axes fraction',
                         arrowprops=dict(arrowstyle='->'), 
                         horizontalalignment='center')
            
    fig, axes= plt.subplots(nrows=2, ncols=3, figsize=(16/1.1,9/1.1))

    idx = [0,0]
    applyPlotStyle('Buffer Heating', idx)
    for i in files['B_heating']:
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:], label=i)
        axes[idx[0], idx[1]].legend()
        
    idx = [0,1]
    applyPlotStyle('EC Heating', idx)
    for i in files['EC_heating']:
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:], label=i)
        axes[idx[0], idx[1]].legend()
        
    idx = [0,2]
    applyPlotStyle('Sample Heating', idx)
    for i in files['S_heating']:    
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:], label=i)
        axes[idx[0], idx[1]].legend()

    idx = [1,0]
    applyPlotStyle('Buffer Cooling', idx)
    for i in files['B_cooling']:
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:], label=i)
        axes[idx[0], idx[1]].legend()
        
    idx = [1,1]
    applyPlotStyle('EC Cooling', idx)
    for i in files['EC_cooling']:
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:], label=i)
        axes[idx[0], idx[1]].legend()
        
    idx = [1,2]
    applyPlotStyle('Sample Cooling', idx)
    for i in files['S_cooling']:    
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:], label=i) 
        axes[idx[0], idx[1]].legend()
    
    filename = os.path.join(os.path.join(params['Folder'],'Output'), filename + '_Rawdata.pdf') 
    plt.tight_layout()
    plt.savefig(filename)
    plt.close(fig)  
   
    
    
    
def plot_corrected_data(files, data, params, filename):
    ''' Plots the corrected data'''
    print('\n', 15*'*', 'Plots the corrected data', 15*'*')
    
    def applyPlotStyle(title, idx, Mw = True):
        ax.set_xlabel('Temperature / °C')
        ax.set_ylabel('Heat capacity / J K$^{-1}$')
        ax.set_title(title)
        #ax.legend(loc='upper left')
    
    
    def plot(ax, data, file, Mw = True):
        ax.plot(data[file][1,:], data[file][2,:]/np.average(data[file][4,:])/1000, '--bo', markersize=3, linewidth=1, label=file)
    
    N = len(data)
    cols = int(np.ceil(np.sqrt(N)))
    rows = int(np.ceil(N/cols)) if cols > 0 else 1
    gs = gridspec.GridSpec(rows, cols)
    
    fig = plt.figure(figsize=(cols*4.5, rows*4.5))
    
    i = 0
    for file in sorted(data):
        ax = fig.add_subplot(gs[i])
        applyPlotStyle(file, ax, Mw = 'Mw' in params)
        plot(ax, data, file, Mw = 'Mw' in params)
        i+= 1
        
    filename = os.path.join(os.path.join(params['Folder'],'Output'), filename + '_Corrected_data.pdf') 
    gs.tight_layout(fig)
    plt.savefig(filename)
    plt.close(fig)

    
def plot_final_data(files, data, params, filename):
    ''' Plots the final data'''
    print('\n', 15*'*', 'Plots the final data', 15*'*')
    
    def applyPlotStyle(title, idx, kJ, Mw = True):
        ax.set_xlabel('Temperature / °C')
        if Mw:
            if kJ == True:
                ax.set_ylabel('Heat capacity / kJ K$^{-1}$ mol$^{-1}$')
            else:
                ax.set_ylabel('Heat capacity / J K$^{-1}$ mol$^{-1}$')
        else:
            if kJ == True:
                ax.set_ylabel('Heat capacity / kJ K$^{-1}$ g$^{-1}$')
            else:
                ax.set_ylabel('Heat capacity / J K$^{-1}$ g$^{-1}$')
        ax.set_title(title)
        if params['Exo_in_plot'] is True:
            if params['Output'] == 'exo-down':
                ax.annotate('Exo-down', xy=(0.1, 0.05), xytext=(0.1, 0.25), xycoords = 'axes fraction',
                         arrowprops=dict(arrowstyle='->'), 
                         horizontalalignment='center')
            if params['Output'] == 'exo-up':
                ax.annotate('Exo-up', xy=(0.1, 0.25), xytext=(0.1, 0.05), xycoords = 'axes fraction',
                         arrowprops=dict(arrowstyle='->'), 
                         horizontalalignment='center')
        #ax.legend(loc='upper left')
    
    
    def plot(ax, data, file, kJ, Mw = True):
        if Mw:
            if kJ:
                ax.plot(data[file][:,0], data[file][:,1]/1e3)
                ax.annotate('DH = {:0.3g} kJ/mol'.format(data[file][-1,5]/1e3), xy=(0.65, 0.15), xycoords='axes fraction')
            else:
                ax.plot(data[file][:,0], data[file][:,1])
                ax.annotate('DH = {:0.3g} J/mol'.format(data[file][-1,5]), xy=(0.65, 0.15), xycoords='axes fraction')
        else:
            if kJ:
                ax.plot(data[file][:,0], data[file][:,1]/1e3)
                ax.annotate('DH = {:0.3g} kJ/g'.format(data[file][-1,5]/1e3), xy=(0.70, 0.15), xycoords='axes fraction')
            else:
                ax.plot(data[file][:,0], data[file][:,1])
                ax.annotate('DH = {:0.3g} J/g'.format(data[file][-1,5]), xy=(0.70, 0.15), xycoords='axes fraction')
        #ax.annotate('{}'.format(params['Output'][0]), xy=(0.80, 0.05), xycoords='axes fraction')
        #ax.arrow( 0.1, 0.1, 0.0, 0.2, fc="k", ec="k", head_width=0.05, head_length=0.1, xycoords='axes fraction' )
        
    N = len(data)
    cols = int(np.ceil(np.sqrt(N)))
    rows = int(np.ceil(N/cols)) if cols > 0 else 1 
    gs = gridspec.GridSpec(rows, cols)
    
    fig = plt.figure(figsize=(cols*4.5, rows*4.5))
    
    i = 0
    for file in sorted(data):
        ax = fig.add_subplot(gs[i])
        kJ = max(abs(data[file][:,1])) > 1000 #if the maximum of the data is larger than 1000 J/g or J/mol, data are plotted in kJ/g or kJ/mol. 
        applyPlotStyle(file, ax, kJ, Mw = 'Mw' in params)
        plot(ax, data, file, kJ, Mw = 'Mw' in params)
        i+= 1
    
    filename = os.path.join(os.path.join(params['Folder'],'Output'), filename + '_Final_data.pdf') 
    gs.tight_layout(fig)
    plt.savefig(filename)
    plt.close(fig)
    
def plot_uncut_data(files, data, params, sample):
    
    def applyPlotStyle(title, ax1, ax2, Mw = True):
        ax1.set_xlabel('Temperature / °C')
        if Mw:
            ax1.set_ylabel('Heat capacity (heating) / J K$^{-1}$ mol$^{-1}$')
            ax2.set_ylabel('Heat capacity (cooling) / J K$^{-1}$ mol$^{-1}$')
            
        else:
            ax1.set_ylabel('Heat capacity (heating) / J K$^{-1}$ g$^{-1}$')
            ax2.set_ylabel('Heat capacity (cooling) / J K$^{-1}$ g$^{-1}$')
        
        ax1.set_title(title)
        ax1.yaxis.label.set_color('red')
        ax1.tick_params(axis='y', colors='red')
        ax2.yaxis.label.set_color('blue')
        ax2.tick_params(axis='y', colors='blue')
        
        
    fig, ax1 = plt.subplots(1,1,figsize=(7,4))
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    applyPlotStyle(sample, ax1, ax2, Mw = 'Mw' in params)
    
    for file in sorted(data):
        if file in files['S_heating']:
            ax1.plot(data[file][:,0], data[file][:,1], color='red')
        if file in files['S_cooling']:
            ax2.plot(data[file][:,0], data[file][:,1], color='blue')
            
    filename = os.path.join(os.path.join(params['Folder'],'Output'), sample + '_uncut_data.pdf') 
    plt.tight_layout()
    plt.savefig(filename)
    plt.close(fig)
    
    
def plot_baseline_data(files, data, params, filename):
    ''' Plots the baseline corrected data'''
    print('\n', 15*'*', 'Plots the baseline corrected data', 15*'*')
    
    def applyPlotStyle(title, idx, Mw = True):
        ax.set_xlabel('Temperature / °C')
        if Mw:
            ax.set_ylabel('Heat capacity / J K$^{-1}$ mol$^{-1}$')
        else:
            ax.set_ylabel('Heat capacity / J K$^{-1}$ g$^{-1}$')
        ax.set_title(title)
        #ax.legend(loc='upper left')
    
    
    def plot(ax, data, file, Mw = True):
        ax.plot(data[file][:,0], data[file][:,2], linestyle = '-' )
        ax.plot(data[file][:,0], data[file][:,3], linestyle = '-.', color='#ff7f0e')
        ax.fill_between(data[file][:,0], data[file][:,3]-data[file][:,4], data[file][:,3]+data[file][:,4], alpha=0.4 , color='#ff7f0e')
        # ax.fill_between(data[file][:,0], data[file][:,3]+data[file][:,4], alpha=0.4)
        
        if file in files['S_heating']:
            ax.axvspan(float(params['ROI_h'][0]), float(params['ROP_h'][0]), facecolor='#a9a9a9', alpha=0.5)
            ax.axvspan(float(params['ROI_h'][1]), float(params['ROP_h'][1]), facecolor='#a9a9a9', alpha=0.5)
        if file in files['S_cooling']:
            ax.axvspan(float(params['ROI_c'][0]), float(params['ROP_c'][0]), facecolor='#a9a9a9', alpha=0.5)
            ax.axvspan(float(params['ROI_c'][1]), float(params['ROP_c'][1]), facecolor='#a9a9a9', alpha=0.5)
        #ax.axvspan(58.0, 60.0, facecolor='g', alpha=0.5)

    
    N = len(data)
    cols = int(np.ceil(np.sqrt(N)))
    rows = int(np.ceil(N/cols)) if cols > 0 else 1 
    gs = gridspec.GridSpec(rows, cols)
    
    fig = plt.figure(figsize=(cols*4.5, rows*4.5))
    
    i = 0
    for file in sorted(data):
        ax = fig.add_subplot(gs[i])
        applyPlotStyle(file, ax, Mw = 'Mw' in params)
        plot(ax, data, file, Mw = 'Mw' in params)
        i+= 1
    
    gs.tight_layout(fig)
    filename = os.path.join(os.path.join(params['Folder'],'Output'), filename + '_Baseline_data.pdf') 
    plt.savefig(filename)
    plt.close(fig)
    
    
def plot_alpha(files, data, params, filename):
    ''' Plots the degree of conversion for all data'''
    print('\n', 15*'*', 'Plots the degree of conversion for all data', 15*'*')
    
    
        #ax.legend(loc='upper left')
    fig, ax = plt.subplots() 
    ax.set_ylabel('α')
    ax.set_xlabel('Temperature / °C')
    
    

    for file in sorted(data):
        if file in files['S_cooling']:
            ax.plot(data[file][:,0], 1-data[file][:,5]/data[file][-1,5],  label=file)
        else:
            ax.plot(data[file][:,0], data[file][:,5]/data[file][-1,5],  label=file)

    
    plt.legend()
    filename = os.path.join(os.path.join(params['Folder'],'Output'), filename +  '_alpha.pdf') 
    plt.savefig(filename)
    plt.close(fig)