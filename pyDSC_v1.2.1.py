# -*- coding: utf-8 -*-
"""
20.01.2021 : Aline Cisse. Correction of params[''][0] in param[''] (removal of the [0]) 
in correction module of DSC1.py. 
2021.02.19: Leo. Small bug correction, data are read from the path defined in the input file and exported to an output folder which is created in the rawdata folder.
2021.02.19: Leo. Bug corrections and clearer error messages are returned when file do not exists or dataformat provided is wrong. 
2021.06.02: Leo. Small bug corrections. 
2022.01.19: Leo. Small bug correction.
2022.01.26: Leo. Bug corrections plus error estimate for Delta CP and DeltaH. Requires scipy>1.8
2022.09.08: Leo: Small bug corrections.
2023.05.04: Leo: Small bug corrections.
2023.05.22: Leo: Bug corrections in the code.
2023.05.23: Export normalized date on the full temperature range implemented. Handling of headers changed.
2023.06.21 Leo: Small bug corrections in export function.
"""

version = '1.2.1'
date = '2023.06.21'


import DSC1 as dsc #imports the dsc1.py script, where all used functions are stored. 
import dsc_plot as plot
from dsc_input import samples as input_data
import os
from pathlib import Path
import numpy as np


for sample in input_data:
    header_heating = dict() #Dictionary containing the headers of the exported heating files
    header_cooling = dict() #Dictionary containing the headers of the exported cooling files
    
    files = dsc.read_files(version,date,input_data[sample], header_heating, header_cooling)  #creates a dictionary which contains all filenames used by the script
    params = dsc.read_params(input_data[sample], header_heating, header_cooling) #reads from the input files the parameters necessary to analyse the data, from the masses to the definiton of the temperature ranges 
    Path(os.path.join(params['Folder'],'Output')).mkdir(parents=True, exist_ok=True)  #creates the output file directory.
    data, dataraw, data_uncut = dsc.extract_data(files, params, header_heating, header_cooling) #creates an array which contains all the data values within the ROIs and already binned. 
    # print(np.shape(data_uncut['myoglobin_cell1_scan2.txt']))
    dsc.check_data(data, files, params, header_heating, header_cooling) #veryfies that all input values are correct. 
    plot.plot_raw_data(files, dataraw, params, sample) #plots the raw data. 
    refs = dsc.average_refs(data, files) #averages the reference measurements. If the size of the reference measurements does not fit, only the longest one is considered. 
    #refs is a dictionary containing the reference measurements.
    data_c = dsc.correction(data, refs, files, params)
    plot.plot_corrected_data(files, data_c, params, sample) #plots the raw data corrected for empty cell and buffer, if reference files are provided. 
    
    data_norm = dsc.normalize_sampleruns(files, data_c, params)
    data_uncut_norm = dsc.normalize_sampleruns(files, data_uncut, params)
    plot.plot_uncut_data(files, data_uncut_norm, params, sample)
    dsc.export_uncut_data(files, data_uncut_norm, params, header_heating, header_cooling)
    data_final = dsc.baseline(data_norm, params, files,header_heating, header_cooling) 
    plot.plot_baseline_data(files, data_final, params, sample)
    plot.plot_final_data(files, data_final, params, sample)
    plot.plot_alpha(files, data_final, params, sample)

    dsc.export_final_data(files, data_final, params, header_heating, header_cooling)
    
