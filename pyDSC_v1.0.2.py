# -*- coding: utf-8 -*-
"""
20.01.2021 : Aline Cisse. Correction of params[''][0] in param[''] (removal of the [0]) 
in correction module of DSC1.py. 
2021.02.19: Leo. Small bug correction, data are read from the path defined in the input file and exported to an output folder which is created in the rawdata folder.

"""

version = '1.0.2'
date = '2021.02.19'

import DSC1 as dsc #imports the dsc1.py script, where all used functions are stored. 
import dsc_plot as plot
from dsc_input import samples as input_data
import os
from pathlib import Path



for sample in input_data:
    files = dsc.read_files(version,date,input_data[sample])  #creates a dictionary which contains all filenames used by the script
    params = dsc.read_params(input_data[sample]) #reads from the input files the parameters necessary to analyse the data, from the masses to the definiton of the temperature ranges 
    Path(os.path.join(params['Folder'],'Output')).mkdir(parents=True, exist_ok=True)  #creates the output file directory.
    data, dataraw = dsc.extract_data(files, params) #creates an array which contains all the data values within the ROIs and already binned. 
    dsc.check_data(data, files, params) #veryfies that all input values are correct. 
    plot.plot_raw_data(files, dataraw, params, sample) #plots the raw data. 
    refs = dsc.average_refs(data, files) #averages the reference measurements. If the size of the reference measurements does not fit, only the longest one is considered. 
    #refs is a dictionary containing the reference measurements.
    data_c = dsc.correction(data, refs, files, params)
    plot.plot_corrected_data(files, data_c, params, sample) #plots the raw data corrected for empty cell and buffer, if reference files are provided. 
    
    data_norm = dsc.normalize_sampleruns(files, data_c, params)
    data_final = dsc.baseline(data_norm, params, files) 
    plot.plot_baseline_data(files, data_final, params, sample)
    plot.plot_final_data(files, data_final, params, sample)
    plot.plot_alpha(files, data_final, params, sample)
    dsc.export_final_data(files, data_final, params)

