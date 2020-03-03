# -*- coding: utf-8 -*-
"""
Two sets of script dedicated to the reduction of the thermograms from differential scanning calorimetry on simple solutions. 
First version by Aline Cisse
Second version by Leonardo Chiappisi (December 2018)
Edit 2019.02.05: corrected bug in dsc.plot (wrong value for enthalpy displayed) and reads Mw from input file. 
Edit 2019.02.19: dsc.correction function was added. 
Edit 2019.05.02: correction of small bugs in the dsc.correction function and addition of the plot_baseline_data function. 
Edit 2019.05.29: Included input dataformat 3cols and evaluated error in DH from data noise. Correction small bugs. 
Edit 2019.05.30: Small bug correction.
Edit 2019.06.05: Added latin1 encoding in the setaram data formats
Edit 2019.06.07: Small bug corrections.
Edit 2019.06.25: Several information are now included in the output files. Program takes care of exo-up or exo-down convention.  Version number and date will be added to the exported files. 
Edit 2019.10.31: In plot.plot_raw_data the raw heatflow is not plotted. 
Edit 2019.11.06: Small bugs corrected. 
Edit 2019.11.13: Added the function plot_alpha, which plots the degree of conversion of all sample runs. Changed degC to °C in plots. 
Edit 2020.01.08: Corrected bug in DSCplot and added encoding option to the input_params file. 
Edit 2020.02.27: Added Exo-up or Exo-down arrow in the DSC Plots
Edit 2020.01.03: Included TA_temp_power_time data format
Edit 2020.01.04: Script automatically tries to read the datafiles using different encodings. The encoding
                 parameter is not required anymore in the input_params file. Small bugs corrected.  
"""

version = '0.5.2'
date = '2020.01.04'

import DSC1 as dsc #imports the dsc1.py script, where all used functions are stored. 
import dsc_plot as plot


files = dsc.read_files(version,date)  #creates a dictionary which contains all filenames used by the script
params = dsc.read_params() #reads from the input files the parameters necessary to analyse the data, from the masses to the definiton of the temperature ranges 
data, dataraw = dsc.extract_data(files, params) #creates an array which contains all the data values within the ROIs and already binned. 
dsc.check_data(data, files, params) #veryfies that all input values are correct. 
plot.plot_raw_data(files, dataraw, params) #plots the raw data. 
refs = dsc.average_refs(data, files) #averages the reference measurements. If the size of the reference measurements does not fit, only the longest one is considered. 
#refs is a dictionary containing the reference measurements.
data_c = dsc.correction(data, refs, files, params)
plot.plot_corrected_data(files, data_c, params) #plots the raw data corrected for empty cell and buffer, if reference files are provided. 

data_norm = dsc.normalize_sampleruns(files, data_c, params)
data_final = dsc.baseline(data_norm, params, files) 
plot.plot_baseline_data(files, data_final, params)
plot.plot_final_data(files, data_final, params)
plot.plot_alpha(files, data_final, params)
dsc.export_final_data(files, data_final, params)

