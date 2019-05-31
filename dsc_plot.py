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


def plot_raw_data(files, data, params):
    ''' Plots the raw_data'''
    
    print('\n', 15*'*', 'Plotting the raw data', 15*'*')
     
    def applyPlotStyle(title, idx):
        axes[idx[0], idx[1]].set_xlabel('Temperature / degC')
        axes[idx[0], idx[1]].set_ylabel('Heat capacity / 10$^{-3}$ J K$^{-1}$')
        axes[idx[0], idx[1]].set_title(title)
        #axes[idx[0], idx[1]].legend(loc='upper left')
        
    fig, axes= plt.subplots(nrows=2, ncols=3, figsize=(16/1.1,9/1.1))

    idx = [0,0]
    applyPlotStyle('Buffer Heating', idx)
    for i in files['B_heating']:
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:]/np.average(data[i][4,:]), label=i)
        axes[idx[0], idx[1]].legend()
        
    idx = [0,1]
    applyPlotStyle('EC Heating', idx)
    for i in files['EC_heating']:
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:]/np.average(data[i][4,:]), label=i)
        axes[idx[0], idx[1]].legend()
        
    idx = [0,2]
    applyPlotStyle('Sample Heating', idx)
    for i in files['S_heating']:    
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:]/np.average(data[i][4,:]), label=i)
        axes[idx[0], idx[1]].legend()

    idx = [1,0]
    applyPlotStyle('Buffer Cooling', idx)
    for i in files['B_cooling']:
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:]/np.average(data[i][4,:]), label=i)
        axes[idx[0], idx[1]].legend()
        
    idx = [1,1]
    applyPlotStyle('EC Cooling', idx)
    for i in files['EC_cooling']:
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:]/np.average(data[i][4,:]), label=i)
        axes[idx[0], idx[1]].legend()
        
    idx = [1,2]
    applyPlotStyle('Sample Cooling', idx)
    for i in files['S_cooling']:    
        axes[idx[0], idx[1]].plot(data[i][1,:], data[i][2,:]/np.average(data[i][4,:]), label=i) 
        axes[idx[0], idx[1]].legend()
    
    plt.tight_layout()
    plt.savefig('Rawdata.pdf')
    plt.close(fig)  
    
    
def plot_corrected_data(files, data, params):
    ''' Plots the corrected data'''
    print('\n', 15*'*', 'Plots the corrected data', 15*'*')
    
    def applyPlotStyle(title, idx, Mw = True):
        ax.set_xlabel('Temperature / degC')
        if Mw:
            ax.set_ylabel('Heat capacity / J K$^{-1}$ mol$^{-1}$')
        else:
            ax.set_ylabel('Heat capacity / J K$^{-1}$ g$^{-1}$')
        ax.set_title(title)
        #ax.legend(loc='upper left')
    
    
    def plot(ax, data, file, Mw = True):
        ax.plot(data[file][1,:], data[file][2,:]/np.average(data[file][4,:]), '--bo', markersize=3, linewidth=1, label=file)
    
    N = len(data)
    cols = int(np.ceil(np.sqrt(N)))
    rows = int(np.ceil(N/cols))
    gs = gridspec.GridSpec(rows, cols)
    
    fig = plt.figure(figsize=(cols*4.5, rows*4.5))
    
    i = 0
    for file in data:
        ax = fig.add_subplot(gs[i])
        applyPlotStyle(file, ax, Mw = 'Mw' in params)
        plot(ax, data, file, Mw = 'Mw' in params)
        i+= 1
    
    gs.tight_layout(fig)
    plt.savefig('Corrected_data.pdf')
    plt.close(fig)

    
def plot_final_data(files, data, params):
    ''' Plots the final data'''
    print('\n', 15*'*', 'Plots the final data', 15*'*')
    
    def applyPlotStyle(title, idx, Mw = True):
        ax.set_xlabel('Temperature / degC')
        if Mw:
            ax.set_ylabel('Heat capacity / J K$^{-1}$ mol$^{-1}$')
        else:
            ax.set_ylabel('Heat capacity / J K$^{-1}$ g$^{-1}$')
        ax.set_title(title)
        #ax.legend(loc='upper left')
    
    
    def plot(ax, data, file, Mw = True):
        ax.plot(data[file][:,0], data[file][:,1])
        if Mw:
            ax.annotate('DH = {:1.0f} J/mol'.format(data[file][-1,4]), xy=(0.05, 0.05), xycoords='axes fraction')
        else:
            ax.annotate('DH = {:1.1f} J/g'.format(data[file][-1,4]), xy=(0.05, 0.05), xycoords='axes fraction')
    
    N = len(data)
    cols = int(np.ceil(np.sqrt(N)))
    rows = int(np.ceil(N/cols))
    gs = gridspec.GridSpec(rows, cols)
    
    fig = plt.figure(figsize=(cols*4.5, rows*4.5))
    
    i = 0
    for file in data:
        ax = fig.add_subplot(gs[i])
        applyPlotStyle(file, ax, Mw = 'Mw' in params)
        plot(ax, data, file, Mw = 'Mw' in params)
        i+= 1
    
    gs.tight_layout(fig)
    plt.savefig('Final_data.pdf')
    plt.close(fig)
    
    
    
def plot_baseline_data(files, data, params):
    ''' Plots the baseline corrected data'''
    print('\n', 15*'*', 'Plots the baseline corrected data', 15*'*')
    
    def applyPlotStyle(title, idx, Mw = True):
        ax.set_xlabel('Temperature / degC')
        if Mw:
            ax.set_ylabel('Heat capacity / J K$^{-1}$ mol$^{-1}$')
        else:
            ax.set_ylabel('Heat capacity / J K$^{-1}$ g$^{-1}$')
        ax.set_title(title)
        #ax.legend(loc='upper left')
    
    
    def plot(ax, data, file, Mw = True):
        ax.plot(data[file][:,0], data[file][:,2], linestyle = '-' )
        ax.plot(data[file][:,0], data[file][:,3], linestyle = '-.' )
        if file in files['S_heating']:
            ax.axvspan(float(params['ROI_h'][0]), float(params['ROP_h'][0]), facecolor='#a9a9a9', alpha=0.5)
            ax.axvspan(float(params['ROI_h'][1]), float(params['ROP_h'][1]), facecolor='#a9a9a9', alpha=0.5)
        if file in files['S_cooling']:
            ax.axvspan(float(params['ROI_c'][0]), float(params['ROP_c'][0]), facecolor='#a9a9a9', alpha=0.5)
            ax.axvspan(float(params['ROI_c'][1]), float(params['ROP_c'][1]), facecolor='#a9a9a9', alpha=0.5)
        #ax.axvspan(58.0, 60.0, facecolor='g', alpha=0.5)

    
    N = len(data)
    cols = int(np.ceil(np.sqrt(N)))
    rows = int(np.ceil(N/cols))
    gs = gridspec.GridSpec(rows, cols)
    
    fig = plt.figure(figsize=(cols*4.5, rows*4.5))
    
    i = 0
    for file in data:
        ax = fig.add_subplot(gs[i])
        applyPlotStyle(file, ax, Mw = 'Mw' in params)
        plot(ax, data, file, Mw = 'Mw' in params)
        i+= 1
    
    gs.tight_layout(fig)
    plt.savefig('Baseline_data.pdf')
    plt.close(fig)