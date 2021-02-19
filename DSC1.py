# -*- coding: utf-8 -*-
"""
All the functions used by the scripts correction1 are stored in this python file. 
File created on december 2018 by Leonardo Chiappisi
"""
import numpy as np
#import pandas as pd
import os
from math import log
from scipy import interpolate, integrate
from scipy.stats import linregress

encodings = [ 'utf-8', 'utf-16', 'latin1']
header_heating = dict() #Dictionary containing the headers of the exported heating files
header_cooling = dict() #Dictionary containing the headers of the exported cooling files

def write_header(header_heating, header_cooling, files):
    for i in files['S_heating']:
        filename = os.path.join('Output', 'exp-' + str(i) + '.dat')
        with open(filename, 'w+') as f:
            f.write(header_heating[i])
            
    for i in files['S_cooling']:
        filename = os.path.join('Output', 'exp-' + str(i) + '.dat')
        with open(filename, 'w+') as f:
            f.write(header_cooling[i])
            
    return None

def read_files(version, date, sample):
    ''' Function which imports all needed data: heating and cooling cycles as well as correction files: 
    Buffer-buffer thermograms and empty cell corrections. The name of the files are stored in the sample dictionary. 
    '''
    files = {'S_heating': sample['Heating_runs'],
             'EC_heating': sample['Empty_cell_heat_runs'], 
             'B_heating': sample['Buffer_heat_runs'],
             'S_cooling': sample['Cooling_runs'], 
             'EC_cooling': sample['Empty_cell_cool_runs'],  
             'B_cooling': sample['Buffer_cool_runs']} #files is a dictionary containing all the file names used in the script.


    s = 'Found {} entries for the sample heating cycles: {} \n \
        {} entries for the empty cell heating cycles:  {} \n \
        {} entries for the buffer heating cycles: {} \n \
        {} entries for the cooling cycles: {} \n \
        {} entries for the empty cell cooling cycles: {} \n \
        {} entries for the buffer cooling cycles: {}'.format(len(files['S_heating']), files['S_heating'], 
                                                        len(files['EC_heating']), files['EC_heating'],
                                                        len(files['B_heating']), files['B_heating'],
                                                        len(files['S_cooling']), files['S_cooling'],
                                                        len(files['EC_cooling']), files['EC_cooling'],
                                                        len(files['B_cooling']), files['B_cooling'])
        
    
    #Creating output data files with first informations. 
    sc = '# Data threated with pyDSC, version {} from {}. \n'.format(version, date) #heading for heating curves
    sh = '# Data threated with pyDSC, version {} from {}. \n'.format(version, date) #heading for heating curves
    sc += 50*'#' + '\n'
    sh += 50*'#' + '\n'


    
    print(15*'*', 'DATA INPUT', 15*'*')
    print(s, '\n')
    
    print(15*'*', 'DATA Correction', 15*'*')
    if len(files['B_heating']) > 0 and len(files['EC_heating']) > 0:
        print('Heating curves will be corrected by empty cell and buffer-buffer experiments. \n')
        sh += '# Heating curves were corrected by empty cell {} and buffer-buffer experiments {}. \n'.format(files['EC_heating'], files['B_heating'])
    if len(files['B_heating']) > 0 and len(files['EC_heating']) == 0:
        print('Heating curves will be corrected by buffer-buffer experiments')
        sh += '# Heating curves were corrected by buffer-buffer experiments {}'.format(files['B_heating'])
    if len(files['B_heating']) == 0 and len(files['EC_heating']) > 0:
        print('Heating curves will be corrected by empty cell experiments. \n')
        sh += '# Heating curves were corrected by empty cell {} experiments \n'.format(files['EC_heating'])
    if len(files['B_heating']) == 0 and len(files['EC_heating']) == 0:
        print('Heating curves will not be corrected with reference measurements. \n')
        sh += '# Heating curves were not corrected with reference measurements. \n'
    if len(files['B_cooling']) > 0 and len(files['EC_cooling']) > 0:
        print('Cooling curves will be corrected by empty cell and buffer-buffer experiments')
        sc += '# Cooling curves were corrected by empty cell {} and buffer-buffer experiments {}. \n'.format(files['EC_cooling'], files['B_cooling'])
    if len(files['B_cooling']) > 0 and len(files['EC_cooling']) == 0:
        print('Cooling curves will be corrected by buffer-buffer experiments')
        sc += '# Cooling curves were corrected by buffer-buffer experiments {}. \n'.format(files['B_cooling'])
    if len(files['B_cooling']) == 0 and len(files['EC_cooling']) > 0:
        print('Cooling curves will be corrected by empty cell experiments')
        sc += '# Cooling curves were corrected by empty cell {} experiments. \n'.format(files['EC_cooling'])
    if len(files['B_cooling']) == 0 and len(files['EC_cooling']) == 0:
        print('Cooling curves will not be corrected with reference measurements')
        sc += '# Cooling curves were not corrected with reference measurements. \n'
    
    print('\n')
    
    for key in files:
        if 'S_heating' in key:
            for file in files[key]:
                header_heating[file] = sh
        if 'S_cooling' in key:
            for file in files[key]:
                header_cooling[file] = sc
    
    return files



def read_params(input_data):
    '''Function which reads the parameter input firles and extracts all relevant informations, i.e., sample mass, mw, temperature
    region of interests, regions where the baseline will be evaluated, etc.    
    '''    
    print(15*'*', 'Input Parameters', 15*'*')
    params = {}
    for item in input_data:
        if 'runs' not in item:
            params[item] = input_data[item]
            s = 'Input parameter {} read correctly as {}'.format(item, params[item])
            print(s)
            
 

    
    if isinstance(params['Mw'], str):  del params['Mw'] #removes the Mw element if no Mw is provided in the input data file. 
    if params['Mw'] == 0: del params['Mw']
    
    params['Input'] = params['Input'].lower() #String is converted in lowcase letters only, to avoid problems with 'Exo-up' or similar
    params['Output'] = params['Output'].lower() #String is converted in lowcase letters only, to avoid problems with 'Exo-up' or similar


    for key in header_heating:
        header_heating[key] += '# Sample solution mass = {} mg, reference solution mass = {} mg. \n'.format(params['mass_s'], params['mass_r'])
        if 'Mw' in params: 
            header_heating[key] += '# Sample contains {:.3g} mg of sample, corresponding to a concentration of {:.2f} wt% and {:.3g} mol/kg. \n'.format(float(params['mass_s'])*float(params['s_wt']), float(params['s_wt'])*100, float(params['mass_s'])*float(params['s_wt'])/float(params['mass_s'])/float(params['Mw'])*1000)
        else:
            header_heating[key] += '# Sample contains {:.2f} mg of sample, corresponding to a concentration of {:.2f} wt%. \n'.format(float(params['mass_s'])*float(params['s_wt']), float(params['s_wt'])*100)
        header_heating[key] += '# Data were provided in the {} convention and are exported in the {} convention. \n'.format(params['Input'], params['Output'])
    for key in header_cooling:
        header_cooling[key] += '# Sample solution mass = {} mg, reference solution mass = {} mg. \n'.format(params['mass_s'], params['mass_r'])
        if 'Mw' in params: 
            header_cooling[key] += '# Sample contains {:.3g} mg of sample, corresponding to a concentration of {:.2f} wt% and {:.3g} mol/kg. \n'.format(float(params['mass_s'])*float(params['s_wt']), float(params['s_wt'])*100, float(params['mass_s'])*float(params['s_wt'])/float(params['mass_s'])/float(params['Mw'])*1000)
        else:
            header_cooling[key] += '# Sample contains {:.3g} mg of sample, corresponding to a concentration of {:.2f} wt%. \n'.format(float(params['mass_s'])*float(params['s_wt']), float(params['s_wt'])*100)
        header_cooling[key] += '# Data were provided in the {} convention and are exported in the {} convention. \n'.format(params['Input'], params['Output'])
        
    return params


def extract_data(files, params, *args, **kwargs):
    ''' Extract the time, temperature, heatflow data from the data files as experted from the instrument in the ascii format. 
    Returns a dictionary containing all data files within the region of interest and binned according to bins.     
    The user needs to specify the data format (i.e., from setaram with 4 columns  "Index, time, temperature, heatflow") in the settings_files. 
    setaram4--> Index, time, temperature, heatflow in addition of header of variable length. Beginning of data identifies by the word Furnace
    setaram3--> time, temperature, heatflow in addition of header of variable length. Beginning of data identifies by the word Furnace
    At the end, all files will be saves as time, temperature, heatflow. If the time information is not given, the first column will be filled with zeros.
    
    All file definitions are given in the readme file.
    Availabe data formats are: Setaram3, Setaram4, 3cols, Setaram3temptime
    '''
    print(15*'*', 'Reading data files', 15*'*')
    data = {} #Creation of empty dictionary, where the datasets will be stored, indexed by their filename. 
    dataraw = {} #Creation of empty dictionary, where the datasets will be stored, indexed by their filename. 
    for key in files: 
        for j in files[key]: #the two for loops run over all files defined in the file_input definition file. 
            if j:  #this if sentence is made to avoid trying to read empty key values. 
                if params['Dataformat'] == 'Setaram3':
                    for code in encodings:
                        try:
                            with open(os.path.join(params['Folder'], str(j)), 'r', errors='replace', encoding=code) as inp:
                                hl = 1 #length of the header of the file to be read. 
                                line = inp.readline()
                                while 'Furnace' not in line.split():
                                    line = inp.readline()
                                    hl += 1
                                    if hl > 500:
                                        raise Exception('Cannot import datafile {} correctly. Ensure the encoding is set correctly. Current encoding is {}.'.format(j, code))
                            tmp = np.genfromtxt(os.path.join(params['Folder'], str(j)), skip_header=hl+1, skip_footer=2, unpack=True, usecols=(0,1,2), encoding=code) #imports all data stored in files
                            print('File {} opened with {} encoding.'.format(str(j), code))
                            break
                        except:
                            None
#                            print('Tried to open the file {} with {} encoding. Failed.'.format(str(j), code))
                            
                elif params['Dataformat'] == 'Setaram3temptime':
                    for code in encodings:
                        try:
                            with open(os.path.join(params['Folder'], str(j)), 'r', errors='replace', encoding=code) as inp:
                                hl = 1 #length of the header of the file to be read. 
                                line = inp.readline()
                                while 'Furnace' not in line.split():
                                    line = inp.readline()
                                    hl += 1
                                    if hl > 500:
                                        raise Exception('Cannot import datafile {} correctly. Ensure the encoding is set correctly. Current encoding is {}.'.format(j, code))
                            tmp = np.genfromtxt(os.path.join(params['Folder'], str(j)), skip_header=hl+1, skip_footer=2, unpack=True, usecols=(1,0,2), encoding=code) #imports all data stored in files
                            print('File {} opened with {} encoding.'.format(str(j), code))
                            break
                        except:
                            None
#                            print('Tried to open the file {} with {} encoding. Failed.'.format(str(j), code))
                
                elif params['Dataformat'] == 'Setaram4':
                    for code in encodings:
                        try:
                            with open(os.path.join(params['Folder'], str(j)), 'r', errors='replace', encoding=code) as inp:
                                hl = 1 #length of the header of the file to be read. 
                                line = inp.readline()
                                while 'Furnace' not in line.split():
                                    line = inp.readline()
                                    hl += 1
                                    if hl > 500:
                                        raise Exception('Cannot import datafile {} correctly. Ensure the encoding is set correctly. Current encoding is {}.'.format(j, code))
                            tmp = np.genfromtxt(os.path.join(params['Folder'], str(j)), skip_header=hl+1, skip_footer=2, unpack=True, usecols=(1,2,3), encoding=code) #imports all data stored in files
                            print('File {} opened with {} encoding.'.format(str(j), code))
                            break
                        except:
                            None
#                            print('Tried to open the file {} with {} encoding. Failed.'.format(str(j), code))
                    
                elif params['Dataformat'] == '3cols':
                    for code in encodings:
                        try:
                            hl = 1 #length of the header of the file to be read. 
                            tmp = np.genfromtxt(os.path.join(params['Folder'], str(j)), skip_header=hl, skip_footer=2, unpack=True, usecols=(0,1,2), encoding=code) #imports all data stored in files
                            print('File {} opened with {} encoding.'.format(str(j), code))
                            break
                        except:
                            None
                            
                elif params['Dataformat'] == '3cols_variable_header':
                    for code in encodings:
                        try:
                            hl = int(params['Header_length'][0]) #length of the header of the file to be read. 
                            tmp = np.genfromtxt(os.path.join(params['Folder'], str(j)), skip_header=hl, skip_footer=2, unpack=True, usecols=(0,1,2), encoding=code) #imports all data stored in files
                            print('File {} opened with {} encoding.'.format(str(j), code))
                            break
                        except:
                            None
                            
                elif params['Dataformat'] == '3cols_variable_header_temp_power_time':
                    for code in encodings:
                        try:
                            hl = int(params['Header_length'][0]) #length of the header of the file to be read. 
                            tmp = np.genfromtxt(os.path.join(params['Folder'], str(j)), skip_header=hl, skip_footer=2, unpack=True, usecols=(2,0,1), encoding=code) #imports all data stored in files
                            print('File {} opened with {} encoding.'.format(str(j), code))
                            break
                        except:
                            None
                            
                elif params['Dataformat'] == '4cols_variable_header':
                    for code in encodings:
                        try:
                            hl = int(params['Header_length'][0]) #length of the header of the file to be read. 
                            tmp = np.genfromtxt(os.path.join(params['Folder'], str(j)), skip_header=hl, skip_footer=2, unpack=True, usecols=(1,2,3), encoding=code) #imports all data stored in files
                            print('File {} opened with {} encoding.'.format(str(j), code))
                            break
                        except:
                            None
#                            print('Tried to open the file {} with {} encoding. Failed.'.format(str(j), code))                    
                
                elif params['Dataformat'] == 'TA_temp_power_time':
                    for code in encodings:
                        try:
                            hl = 1 #length of the header of the file to be read.
                            tmp = np.genfromtxt(os.path.join(params['Folder'], str(j)), skip_header=hl, skip_footer=2, unpack=True, usecols=(2,0,1), encoding=code) #imports all data stored in files
                            print('File {} opened with {} encoding.'.format(str(j), code))
                            break
                        except:
                            None
                            # print('Tried to open the file {} with {} encoding. Failed.'.format(str(j), code))
                            
                    tmp[2,:] /= 1000 #conversion from uWatt into mW 

                if 'heating' in key:
                    mask = ((float(params['ROI_h'][0]) < tmp[1,:]) & (float(params['ROI_h'][1]) > tmp[1,:])) #defines a mask with the points where the temperature is in the region of interest. 
                elif 'cooling' in key:
                    mask = ((float(params['ROI_c'][0]) < tmp[1,:]) & (float(params['ROI_c'][1]) > tmp[1,:])) #defines a mask with the points where the temperature is in the region of interest. 
                tmp2 = tmp[:,mask] #creates the data array with only the relevant data points. Whatever is outside the region of interest, is not used any longer.                 
                # print(tmp2)
                
                if params['Input'] != params['Output']: #renormalized from exo-up to exo-down convention, or viceversa. 
                    tmp2[2,:] *= -1
                
                if params['unit_time'] == 'min': #Converts time from minutes to seconds
                    tmp2[0,:] *= 60
                
                if params['unit_power'] == 'uW': #Converts the heatflow from uW into mW
                    tmp2[2,:] /= 1000
                    
                if params['unit_power'] == 'W': #Converts the heatflow from W into mW
                    tmp2[2,:] *= 1000

        
                data_set = binning(tmp2, params)  #the data are binned according to the size defined by bins. No binning is performed if binsize is 1 or less. 
                
                
            
            data[j] = data_set
            
            for j in files[key]:
                if params['Input'] != params['Output']: #renormalized from exo-up to exo-down convention, or viceversa. 
                    tmp2[2,:] *= -1
                dataraw[j] = tmp2
            
            
            print('Datafile {} read correctly'.format(j))
    print('\n')
    return data, dataraw #a dictionary containing all data, already cut, binned, and with the heatrate calculated. 


def binning(data, params):
    ''' Function which bins the data array. width points are averaged and an array of length original length//width is retuned.
    No binning is performed when the binsize is smaller or equal to 1. Heatrate is also calculated if the time-temperature data are available. 
    Before binning, if the original file is not a multiple of width, the exceeding points are dropped. '''
    width = int(params['bins'])
    if int(params['bins']) > 1:
        data_binned = np.vstack(([data[i,:(data[i,:].size // width) * width].reshape(-1, width).mean(axis=1) for i in range(len(data[:,0]))]))
        stdev = np.std(data[2,:(data[2,:].size // width) * width].reshape(-1, width), axis=1) #standard deviation of binned points. 
    else:
        data_binned = data
        stdev = np.empty(len(data_binned[0,:]))
    if params['Dataformat'][0] != '2cols':
    #if params['Dataformat'][0] == 'Setaram3' or params['Dataformat'][0] == 'Setaram4' or params['Dataformat'][0] == '3cols':
        hrate = np.diff(data_binned[1,:])/np.diff(data_binned[0,:]) 
    else:
        hrate = np.empty(len(stdev)-1)
    return np.concatenate([np.delete(data_binned, -1, axis=1), np.append([stdev[:-1]], [hrate], axis=0)], axis=0) 


def check_data(data, files, params):
    ''' Functions to check that the information in the data files and those provided in the input files are consistent.
    Eg. temperature increases in the heating scans, temperature range and ROI are consistent, etc. TODO
    It should also check wether all files are present in the rawdata folder. '''
    
    print(15*'*', 'File Check', 15*'*')
    W_counter = 0 #counts warnings
    D_counter = 0 #counts number of rejected files
    

    
    for key in files:  
        for i in files[key]:
#veryfies that the heating files are really a heating file. If not, program stops.             
            if 'heating' in key:
                if (data[i][1,1] > data[i][1,-1]): 
                    print(data[i][1,1], data[i][1,-1])
                    raise Exception('Error: {} is not a heating file!'.format(i))
#Verification for a constant heatrate and if it is consistent with the one provided in parameter file. 
                hr, hrstd = data[i][4,:].mean()*60, data[i][4,:].std()*60
                if 'S_heating' in key:
                 header_heating[i] += '# Heating rate = {:.2f} K/min. \n'.format(hr)
                
                if hrstd/hr > 0.02:
                    W_counter += 1
                    print('Warning {}: the heatrate is not constant and varies by {:.2g}% for file {}.'.format(W_counter, hrstd/hr*100, i))
                if not (0.95 <= (float(params['Scanrate_h'])/hr) <= 1.05): #veryfies consistency with input parameter file
                    print('Warning {}: the determined heatrate of file {} is {:.2g} K/min \
and is not consistent with the one provided in the input parameter file of {:.2g} K/min.'.format(W_counter, i, hr, float(params['Scanrate_h'])))
                    W_counter += 1
                else:
                    print('Heat rate of {:.2g} K/min in file {} consistent with parameter input file.'.format(hr, i))
#veryfies that the buffer and empty cell measurements are identical, i.e., do not differ by more than 5%. 
                    
#veryfies that the cooling files are really a heating file. If not, program stops.                
            if 'cooling' in key:
                if (data[i][1,1] < data[i][1,-1]):
                    raise Exception('Error: {} is not a cooling file!'.format(i))
                    
#Verification for a constant heatrate and if it is consistent with the one provided in parameter file. 
                hr, hrstd = data[i][4,:].mean()*60, data[i][4,:].std()*60
                if 'S_cooling' in key:
                    header_cooling[i] += '# Cooling rate = {:.2f} K/min. \n'.format(-hr)

                if hrstd/hr > 0.02:
                    W_counter += 1
                    print('Warning {}: the heatrate is not constant and varies by {:.2g}% for file {}.'.format(W_counter, hrstd/hr*100, i))
                if not (0.95 <= (-float(params['Scanrate_c'])/hr) <= 1.05): #veryfies consistency with input parameter file
                    print('Warning {}: the determined heatrate of file {} is {:.2g} K/min \
and is not consistent with the one provided in the input parameter file of {:.2g} K/min.'.format(W_counter, i, hr, float(params['Scanrate_c'])))
                    W_counter += 1
                else:
                    print('Heat rate of {:.2g} K/min in file {} consistent with parameter input file.'.format(hr, i))

#Eliminates all the files which do not cover the region of interest. 
    print('\n')
    for key in files:  
        for i in files[key]:           
            minT, maxT = np.min(data[i][1,:]), np.max(data[i][1,:])
            if 'cooling' in key:
                if minT-1.0 > float(params['ROI_c'][0]) or maxT+1.0 < float(params['ROI_c'][1]):
                    D_counter += 1
                    print('Error: temperature range of file {} does not cover the region of interest!'.format(i))
                    print('Requested range is {} -- {}. File covers range {} -- {}.'.format(float(params['ROI_c'][0]), float(params['ROI_c'][1]), minT, maxT))
                    print('File {} will be ignored in all successive calculations.'.format(i))
                    del data[i]
                    files[key].remove(i)
            if 'heating' in key:
                if minT-1.0 > float(params['ROI_h'][0]) or maxT+1.0 < float(params['ROI_h'][1]):
                    D_counter += 1
                    print('Error: temperature range of file {} does not cover the region of interest!'.format(i))
                    print('Requested range is {} -- {}. File covers range {} -- {}.'.format(float(params['ROI_h'][0]), float(params['ROI_h'][1]), minT, maxT))
                    print('File {} will be ignored in all successive calculations.'.format(i))
                    del data[i]
                    files[key].remove(i)

    print('\n')
#Checks weather the heating files have all the same length.
    len_h =  list(filter(None, [[np.shape(data[i])[1] for i in files[key]] for key in files if 'heating' in key])) #creates a list with the lengths of the heating runs
    len_h_flatten = [item for sublist in len_h for item in sublist]
        
    if len(len_h_flatten) > 0:
        diff_h = (max(len_h_flatten) - min(len_h_flatten))/max(len_h_flatten)
        if diff_h == 0.0:
            print('All heating runs have the same length.')
        elif  1e-5 < diff_h < 0.01:
            print('All heating runs have the same length within 1%.')
        elif diff_h < 0.05:
            W_counter += 1
            print('Warning {}: Length of heating runs differs by more than {}%.'.format(W_counter, diff_h*100))
        else:
            raise Exception('Heating run lengths differ by more than 5% to be threated at the same time. Evaluate if analysing them separately.') 

#Checks weather the cooling files have all the same length. 
    len_c =  list(filter(None, [[np.shape(data[i])[1] for i in files[key]] for key in files if 'cooling' in key]))
    len_c_flatten = [item for sublist in len_c for item in sublist]
    if len(len_c_flatten) > 0:
        diff_c = (max(len_c_flatten) - min(len_c_flatten))/max(len_c_flatten)
        if diff_c == 0.0:
            print('All cooling runs have the same length.')
        elif  1e-5 < diff_c < 0.01:
            print('All cooling runs have the same length within 1%.')
        elif diff_c < 0.05:
            W_counter += 1
            print('Warning {}: Length of cooling runs differs by more than {:.1g}%.'.format(W_counter, diff_c*100))
        else:
            raise Exception('Cooling run lengths differ by more than 5% to be threated at the same time. Evaluate if analysing them separately.') 

#Checks that the peak is defined within the region of interest
    if float(params['ROP_h'][0]) < float(params['ROI_h'][0]) or float(params['ROP_h'][1]) >  float(params['ROI_h'][1]):
        raise Exception('Peak in heating run falls out of region of interest. Verify the regions of interest and the region of peak.')
    if float(params['ROP_c'][0]) <  float(params['ROI_c'][0]) or float(params['ROP_c'][1]) >  float(params['ROI_c'][1]):
        raise Exception('Peak in cooling run falls out of region of interest. Verify the regions of interest and the region of peak.')
            
    for key in header_heating:
        header_heating[key] += '# Data between {} and {} degC were analyzed. \n'.format(params['ROI_h'][0], params['ROI_h'][1])
        header_heating[key] += '# Peak is located between {} and {} degC. \n'.format(params['ROP_h'][0], params['ROP_h'][1])
    for key in header_cooling:
        header_cooling[key] += '# Data between {} and {} degC were analyzed. \n'.format(params['ROI_c'][0], params['ROI_c'][1])
        header_cooling[key] += '# Peak is located between {} and {} degC. \n'.format(params['ROP_c'][0], params['ROP_c'][1])
        
    if W_counter == 0 and D_counter == 0:
        print('Check performed sucessfully. No errors encountered!')    
    else:
        print('\n', 5*'*', '{} Warnings have arisen during file check!'.format(W_counter), 5*'*')
        print(5*'*', '{} Files will be ignored in the calculations!'.format(D_counter), 5*'*')
    
    
    return None
    
    
def average_refs(data, files):
    ''' Function which averages the reference measurements of buffer and empty cell. 
    If the size of the reference measurements do not match, the longest only is considered.'''
    print()
    print(15*'*', 'Reference averaging', 15*'*')    
    refs = {'EC_heating': [], 
            'EC_cooling': [], 
            'B_heating': [], 
            'B_cooling': []} #dictionary containing the avergaed reference measurements. 
    if files['EC_heating']: #verifies if EC heatings were measured. 
        len_ref = list(filter(None, [np.shape(data[i])[1] for i in files['EC_heating']]))
        if all(x==len_ref[0] for x in len_ref):
            print('All empty cell heating files are averaged.')
            refs['EC_heating'] = np.average(np.stack([np.asarray(data[i]) for i in files['EC_heating']]), axis=0)
        else:
            for i in files['EC_heating']:
                if np.shape(data[i])[1] == max(len_ref):
                    print('Longest Empty cell heating file, {}, is considered for successive corrections.'.format(i))
                    refs['EC_heating'] = data[i]
                    
    if files['EC_cooling']: #verifies if EC heatings were measured. 
        len_ref = list(filter(None, [np.shape(data[i])[1] for i in files['EC_cooling']]))
        if all(x==len_ref[0] for x in len_ref):
            print('All empty cell cooling files are averaged.')
            refs['EC_cooling'] = np.average(np.stack([np.asarray(data[i]) for i in files['EC_cooling']]), axis=0)
        else:
            for i in files['EC_cooling']:
                if np.shape(data[i])[1] == max(len_ref):
                    print('Longest empty cell cooling file, {}, is considered for successive corrections.'.format(i))
                    refs['EC_cooling'] = data[i]

    
    if files['B_heating']: #verifies if Buffer heatings were measured. 
        len_ref = list(filter(None, [np.shape(data[i])[1] for i in files['B_heating']]))
        if all(x==len_ref[0] for x in len_ref):
            print('All buffer heating files are averaged.')
            refs['B_heating'] = np.average(np.stack([np.asarray(data[i]) for i in files['B_heating']]), axis=0)
        else:
            for i in files['B_heating']:
                if np.shape(data[i])[1] == max(len_ref):
                    print('Longest Buffer heating file, {}, is considered for successive corrections.'.format(i))
                    refs['B_heating'] = data[i]
    
    if files['B_cooling']: #verifies if Buffer coolings were measured. 
        len_ref = list(filter(None, [np.shape(data[i])[1] for i in files['B_cooling']]))
        if all(x==len_ref[0] for x in len_ref):
            print('All buffer cooling files are averaged.')
            refs['B_cooling'] = np.array(np.average(np.stack([np.asarray(data[i]) for i in files['B_cooling']]), axis=0))
        else:
            for i in files['B_cooling']:
                if np.shape(data[i])[1] == max(len_ref):
                    print('Longest Buffer cooling file, {}, is considered for successive corrections.'.format(i))
                    refs['B_cooling'] = data[i]
    
    for key in refs: refs[key] = np.array(refs[key])   #converts also the empty strings into numpy arrays
    return refs


def correction(data, refs, files, params):
    ''' Function which corrects the sample runs for the empty cells and the buffer buffer titrations. 
    If no reference files are provided, this function will simple return the sample raw data.'''
    print(15*'*', 'Sample data correction', 15*'*')  
    data_c = {}

    if np.shape(refs['EC_cooling'])[0]:
        tck_EC = interpolate.interp1d(refs['EC_cooling'][1,:], refs['EC_cooling'][2,:], fill_value='extrapolate')
        if np.shape(refs['B_cooling'])[0] and float(params['mass_bb'][0]) > 0.0:
            print('Correcting the Buffer cooling run for the Empty cell cooling run')
            EC_interpol = tck_EC(refs['B_cooling'][1,:])  #linear interpolation of the heatflow as a function of the temperature of the buffer run.
            Buffer_corrected = np.array((refs['B_cooling'][0,:], refs['B_cooling'][1,:], refs['B_cooling'][2,:]-EC_interpol))
            tck_B = interpolate.interp1d(Buffer_corrected[1,:], Buffer_corrected[2,:], fill_value='extrapolate')
            for i in files['S_cooling']:
                print('Correcting file {} for EC and Buffer measurement'.format(i))
                B_interpol = tck_B(data[i][1,:])  #linear interpolation of the heatflow of the buffer as a function of the temperature of the sample run. 
                EC_interpol = tck_EC(data[i][1,:])  #linear interpolation of the heatflow of the EC as a function of the temperature of the sample run. 
                sf_c = (float(params['mass_s'][0])*(1.-float(params['s_wt'][0])) - float(params['mass_r'][0]))/float(params['mass_bb'][0])  #scaling factor used for correcting cooling sample run. 
                data_corrected = data[i][2,:] - EC_interpol - B_interpol * sf_c  #corrects the data for the empty and for the buffer signal, calculated from the buffer-buffer experiment and reweighted for the buffer difference in sample and reference cell. 
                data_c[i] = np.array([data[i][0,:], data[i][1,:], data_corrected, data[i][3,:], data[i][4,:]])
        else:  #if empty cell was measured but not the buffer/buffer. 
            for i in files['S_cooling']:
                   print('Correcting file {} for EC measurement'.format(i))
                   EC_interpol = tck_EC(data[i][1,:])
                   data_corrected = data[i][2,:] - EC_interpol #corrects the sample data for the empty cell measurement. 
                   data_c[i] = np.array([data[i][0,:], data[i][1,:], data_corrected, data[i][3,:], data[i][4,:]])
    else: #if the empty cell was not measured
        if np.shape(refs['B_cooling'])[0] and float(params['mass_bb'][0]) > 0.0: #if buffer was measured
            tck_B = interpolate.interp1d(refs['B_cooling'][1,:], refs['B_cooling'][2,:], fill_value='extrapolate')
            for i in files['S_cooling']:
                print('Correcting file {} for Buffer measurement'.format(i))
                B_interpol = tck_B(data[i][1,:])  #linear interpolation of the heatflow of the buffer as a function of the temperature of the sample run.       
                sf_c = (float(params['mass_s'][0])*(1.-float(params['s_wt'][0])) - float(params['mass_r'][0]))/float(params['mass_bb'][0])
                data_corrected = data[i][2,:] - B_interpol * sf_c  #corrects the data for the empty and for the buffer signal, calculated from the buffer-buffer experiment and reweighted for the buffer difference in sample and reference cell. 
                data_c[i] = np.array([data[i][0,:], data[i][1,:], data_corrected, data[i][3,:], data[i][4,:]])
        else: #if no empty cell nor buffer were measured. 
            for i in files['S_cooling']:
                print('File {} was not corrected for buffer or emty cell measurement'.format(i))
                data_c[i] = np.array([data[i][0,:], data[i][1,:], data[i][2,:], data[i][3,:], data[i][4,:]])
                
    
    if np.shape(refs['EC_heating'])[0]:
        tck_EC = interpolate.interp1d(refs['EC_heating'][1,:], refs['EC_heating'][2,:], fill_value='extrapolate')
        if np.shape(refs['B_heating'])[0] and float(params['mass_bb'][0]) > 0.0:
            print('Correcting the Buffer heating run for the Empty cell heating run')
            EC_interpol = tck_EC(refs['B_heating'][1,:])  #linear interpolation of the heatflow as a function of the temperature of the buffer run.
            Buffer_corrected = np.array((refs['B_heating'][0,:], refs['B_heating'][1,:], refs['B_heating'][2,:]-EC_interpol))
            print('Buffer heating run was corrected for the Empty cell heating run')
            tck_B = interpolate.interp1d(Buffer_corrected[1,:], Buffer_corrected[2,:], fill_value='extrapolate')
            for i in files['S_heating']:
                print('Correcting file {} for EC and Buffer measurement'.format(i))
                B_interpol = tck_B(data[i][1,:])  #linear interpolation of the heatflow of the buffer as a function of the temperature of the sample run. 
                EC_interpol = tck_EC(data[i][1,:])  #linear interpolation of the heatflow of the EC as a function of the temperature of the sample run. 
                sf_h = (float(params['mass_s'][0])*(1-float(params['s_wt'][0])) - float(params['mass_r'][0]))/float(params['mass_bb'][0]) #scaling factor used for correcting heating sample run. 
                data_corrected = data[i][2,:] - EC_interpol - B_interpol *sf_h  #corrects the data for the empty and for the buffer signal, calculated from the buffer-buffer experiment and reweighted for the buffer difference in sample and reference cell. 
                data_c[i] = np.array([data[i][0,:], data[i][1,:], data_corrected, data[i][3,:], data[i][4,:]])
        else:  #if empty cell was measured but not the buffer/buffer. 
            for i in files['S_heating']:
                   print('Correcting file {} for EC measurement'.format(i))
                   EC_interpol = tck_EC(data[i][1,:])
                   data_corrected = data[i][2,:] - EC_interpol*0.73 #corrects the sample data for the empty cell measurement. 
                   data_c[i] = np.array([data[i][0,:], data[i][1,:], data_corrected, data[i][3,:], data[i][4,:]])
    else: #if the empty cell was not measured
        if np.shape(refs['B_heating'])[0] and float(params['mass_bb'][0]) > 0.0: #if buffer was measured
            tck_B = interpolate.interp1d(refs['B_heating'][1,:], refs['B_heating'][2,:], fill_value='extrapolate')
            for i in files['S_heating']:
                print('Correcting file {} for Buffer measurement'.format(i))
                B_interpol = tck_B(data[i][1,:])  #linear interpolation of the heatflow of the buffer as a function of the temperature of the sample run.       
                sf_h = (float(params['mass_s'][0])*(1.-float(params['s_wt'][0])) - float(params['mass_r'][0]))/float(params['mass_bb'][0]) #scaling factor used for correcting heating sample run. 
                data_corrected = data[i][2,:] - B_interpol * sf_h  #corrects the data for the empty and for the buffer signal, calculated from the buffer-buffer experiment and reweighted for the buffer difference in sample and reference cell. 
                data_c[i] = np.array([data[i][0,:], data[i][1,:], data_corrected, data[i][3,:], data[i][4,:]])
        else: #if no empty cell nor buffer were measured. 
            for i in files['S_heating']:
                print('File {} was not corrected for buffer or emty cell measurement'.format(i))
                data_c[i] = np.array([data[i][0,:], data[i][1,:], data[i][2,:], data[i][3,:], data[i][4,:]])      

    return data_c



def normalize_sampleruns(files, data, params):
    ''' Normalizes the samples for the sample mass, or eventually molar mass'''
    print('\n', 15*'*', 'Data normalization', 15*'*')
    data_norm = dict()
    sample_norm = params['mass_s']*params['s_wt']/1000*1000   #Normalization factor given by the sample mass in grams and from mW to W
    if 'Mw' in params:
        sample_norm /= float(params['Mw'])  #if Mw is provided, the data will be normalized by the moles of compound. 
    
    for i in files['S_heating']:
        hr = np.average(data[i][4,:])
        if 'Mw' in params:
            print('File {} is normalized by a heating rate of {:.2g} K/s, equivalent to {:.2f} K/min, and by {:.2e} moles of sample.'.format(i, hr, hr*60, sample_norm/1000))
        else:
            print('File {} is normalized by a heating rate of {:.2g} K/s, equivalent to {:.2f} K/min, and by {:.2e} grams of sample.'.format(i, hr, hr*60, sample_norm/1000))
        #print(i, np.average(data[i][4,:])*60)
        data_norm[i] = np.column_stack((data[i][1,:], data[i][2,:]/(hr*sample_norm)))
    
    for i in files['S_cooling']:
        hr = -np.average(data[i][4,:])
        if 'Mw' in params:
            print('File {} is normalized by a heating rate of {:.2g} K/s, equivalent to {:.2f} K/min, and by {:.2e} moles of sample.'.format(i, hr, hr*60, sample_norm/1000))
        else:
            print('File {} is normalized by a heating rate of {:.2g} K/s, equivalent to {:.2f} K/min, and by {:.2e} grams of sample.'.format(i, hr, hr*60, sample_norm/1000))
        #print(i, np.average(data[i][4,:])*60)
        data_norm[i] = np.column_stack((data[i][1,:], data[i][2,:]/(hr*sample_norm)))
    return data_norm

def baseline(data_norm, params, files):
    print('\n', 15*'*', 'Baseline substraction', 15*'*')
    data_baseline = dict()
    
    def roundError(N,E):
        '''Function used to format the values of DH and its error according to the error'''
        p=10**round(log(E,10)-0.5)
        return p*round(N/p),p*round(E/p)

    for key in header_heating:
        header_heating[key] += 50*'#' + '\n'
    for key in header_cooling:
        header_cooling[key] += 50*'#' + '\n'
        
    def base(pre_s, pre_i, post_s, post_i, alpha, T):
        '''Calculates the baseline according to the linear interpolation of the region before the peak and after the peak'''
        return pre_i + pre_s*T - alpha*((pre_i-post_i) + (pre_s-post_s)*T)
        
    for i in files['S_heating']:
        #liner fit of the regions before (pre) and after (post) the peak is performed. 
        pre = data_norm[i][float(params['ROP_h'][0]) > data_norm[i][:,0], :]
        post = data_norm[i][float(params['ROP_h'][1]) < data_norm[i][:,0], :]
        pre_s, pre_i, _, _, _ = linregress(pre)
        post_s, post_i, _, _, _ = linregress(post)
        #first baseline is calculated as the spline connecting all the points before and the after the peak. 
        tmp =  data_norm[i][np.logical_or(float(params['ROP_h'][0]) > data_norm[i][:,0], float(params['ROP_h'][1]) < data_norm[i][:,0]), :]
        tck = interpolate.interp1d(tmp[:,0], tmp[:,1])
        base1 = tck(data_norm[i][:,0])
        #first integration using the spline as first baseline. H is the cumulative integral, the area under the curve will be given by H[-1]
        H = integrate.cumtrapz(data_norm[i][:,1]-base1, data_norm[i][:,0], initial=0.0) 
        #Standard deviation in the region before and after the peak, used to limit the loops for optimizing the baseline. 
        B_pre = data_norm[i][float(params['ROP_h'][0]) > data_norm[i][:,0],:1]*pre_s + pre_i
        B_post = data_norm[i][float(params['ROP_h'][1]) < data_norm[i][:,0],:1]*post_s + post_i
         ### Evaluation of uncertainty in the DH ###
        Hst1 = data_norm[i][float(params['ROP_h'][0]) > data_norm[i][:,0]][:,1] - B_pre[:,0] #standard deviation before peak region
        Hst2 = data_norm[i][float(params['ROP_h'][1]) < data_norm[i][:,0]][:,1] - B_post[:,0] #standard deviation after peak region
        Hst = np.std(np.append(Hst1, Hst2)) #standard deviation of Cp calculated in baseline regions. 
        Ns = len(data_norm[i][float(params['ROP_h'][0]) > data_norm[i][:,0],:1])  +  len(data_norm[i][float(params['ROP_h'][1]) < data_norm[i][:,0],:1]) #number of points in the two regions
        delta = np.average(np.diff(data_norm[i][float(params['ROP_h'][1]) < data_norm[i][:,0]][:,0]))
        errH = Hst*delta/2*np.sqrt(2.*(len(data_norm[i][:,0])-Ns))
#        print('Error is', errH)
        DH = H[-1] #variation in area between sucessive loops. The first value is set to the total area. 
        itermax = 0
        newbase = base1
        s = '\nBaseline substraction for file {}'.format(i)
        print(s)
        while itermax < 100:
            itermax += 1
            newbase = base(pre_s, pre_i, post_s, post_i, H/H[-1], data_norm[i][:,0])
            newH = integrate.cumtrapz(data_norm[i][:,1]-newbase, data_norm[i][:,0], initial=0.0)
            DH = H[-1] - newH[-1]
            H = newH
        if 'Mw' in params:
            print('Iteration number {}, enthalpy variation of {:3g} J/mol, final value of DH is {:.5g} +- {:.2g} kJ/mol'.format(itermax, abs(DH/H[-1]), H[-1]/1e3, abs(errH)/1e3))
            header_heating[i] += '# DH of the heating run is {:.5g} +- {:.2g} kJ/mol. \n'.format(*roundError(H[-1]/1e3, abs(errH/1e3)))
        else:
            print('Iteration number {}, enthalpy variation of {:3g} J/g, final value of DH is {:.5g} +- {:.2g} J/g'.format(itermax, abs(DH/H[-1]), H[-1], abs(errH)))
            header_heating[i] += '# DH of the heating run is {:.5g} +- {:.2g} J/g. \n'.format(H[-1], abs(errH))
            
        j = np.column_stack([data_norm[i][:,0], data_norm[i][:,1]-newbase, data_norm[i][:,1], newbase, H])
        data_baseline[i] = j
        
        #determination of maximum or minimum of temperature and Delta CP at Tmax (or Tmin)
        if H[-1] > 0:
            Tmax = data_norm[i][np.argmax(data_norm[i][:,1]-newbase),0]
            header_heating[i] += '# Peak position is at {:.1f} degC. \n'.format(Tmax)
            DCp = (post_i - pre_i) + (post_s-pre_s)*Tmax
            print('Peak position is at {:.1f} degC'.format(Tmax))
            if 'Mw' in params:
                print('Calculated Delta Cp at the peak position is {:.2g} J/K/mol'.format(DCp))
                header_heating[i] += '# Calculated Delta Cp at the peak position is {:.2g} J/K/mol. \n'.format(DCp)
            else:
                print('Calculated Delta Cp at the peak position is {:.2g} J/K/g'.format(DCp))
                header_heating[i] += '# Calculated Delta Cp at the peak position is {:.2g} J/K/g. \n'.format(DCp)
        if H[-1] < 0:
            Tmin = data_norm[i][np.argmin(data_norm[i][:,1]-newbase),0]
            header_heating[i] += '# Peak position is at {:.1f} degC'.format(Tmin)
            DCp = (post_i - pre_i) + (post_s-pre_s)*Tmin
            print('Peak position is at {:.1f} degC'.format(Tmin))
            if 'Mw' in params:
                print('Calculated Delta Cp at the peak position is {:.2g} J/K/mol'.format(DCp))
                header_heating[i] += '# Calculated Delta Cp at the peak position is {:.2g} J/K/mol. \n'.format(DCp)
            else:
                print('Calculated Delta Cp at the peak position is {:.2g} J/K/g'.format(DCp))
                header_heating[i] += '# Calculated Delta Cp at the peak position is {:.2g} J/K/g. \n'.format(DCp)
        header_heating[i] += 50*'#' + '\n'
                
    for i in files['S_cooling']:
        #liner fit of the regions before (pre) and after (post) the peak is performed. 
        pre = data_norm[i][float(params['ROP_c'][0]) > data_norm[i][:,0], :]
        post = data_norm[i][float(params['ROP_c'][1]) < data_norm[i][:,0], :]
        pre_s, pre_i, _, _, _ = linregress(pre)
        post_s, post_i, _, _, _ = linregress(post)
        #first baseline is calculated as the spline connecting all the points before and the after the peak. 
        tmp =  data_norm[i][np.logical_or(float(params['ROP_c'][0]) > data_norm[i][:,0], float(params['ROP_c'][1]) < data_norm[i][:,0]), :]
        tck = interpolate.interp1d(tmp[:,0], tmp[:,1])
        base1 = tck(data_norm[i][:,0])
        #first integration using the spline as first baseline. H is the cumulative integral, the area under the curve will be given by H[-1]
        H = integrate.cumtrapz(data_norm[i][:,1]-base1, data_norm[i][:,0], initial=0.0) 
        #Standard deviation in the region before and after the peak, used to limit the loops for optimizing the baseline. 
        B_pre = data_norm[i][float(params['ROP_c'][0]) > data_norm[i][:,0],:1]*pre_s + pre_i
        B_post = data_norm[i][float(params['ROP_c'][1]) < data_norm[i][:,0],:1]*post_s + post_i


        Hst1 = data_norm[i][float(params['ROP_c'][0]) > data_norm[i][:,0]][:,1] - B_pre[:,0] #standard deviation before peak region
        Hst2 = data_norm[i][float(params['ROP_c'][1]) < data_norm[i][:,0]][:,1] - B_post[:,0] #standard deviation after peak region
        Hst = np.std(np.append(Hst1, Hst2)) #standard deviation of Cp calculated in baseline regions. 
        Ns = len(data_norm[i][float(params['ROP_c'][0]) > data_norm[i][:,0],:1])  +  len(data_norm[i][float(params['ROP_c'][1]) < data_norm[i][:,0],:1]) #number of points in the two regions
        delta = np.average(np.diff(data_norm[i][float(params['ROP_c'][1]) < data_norm[i][:,0]][:,0]))
        errH = Hst*delta/2*np.sqrt(2.*(len(data_norm[i][:,0])-Ns))
        
        
        DH = H[-1] #variation in area between sucessive loops. The first value is set to the total area. 
        itermax = 0
        if 'Mw' in params:
            s = '\nBaseline substraction for file {}:'.format(i)
        else: 
            s = '\nBaseline substraction for file {}:'.format(i)
        print(s)
        while  itermax < 100:
            itermax += 1
            newbase = base(pre_s, pre_i, post_s, post_i, H[::-1]/H[-1], data_norm[i][:,0])
            newH = integrate.cumtrapz(data_norm[i][:,1]-newbase, data_norm[i][:,0], initial=0.0)
            DH = H[-1] - newH[-1]
            H = newH
        if 'Mw' in params:
            print('Iteration number {}, enthalpy variation of {:.3g} J/mol, final value of DH is {:.5g} +- {:.2g} J/mol'.format(itermax, abs(DH/H[-1]), H[-1], abs(errH)))
            header_cooling[i] += '# DH of the cooling run is {:.5g} +- {:.2g} J/mol. \n'.format(H[-1], abs(errH))
        else:
            print('Iteration number {}, enthalpy variation of {:.3g} J/g, final value of DH is {:.5g} +- {:.2g} J/g'.format(itermax, abs(DH/H[-1]), H[-1], abs(errH)))
            header_cooling[i] += '# DH of the cooling run is {:.5g} +- {:.2g} J/g. \n'.format(H[-1], abs(errH))
        
        
        j = np.column_stack([data_norm[i][:,0], data_norm[i][:,1]-newbase, data_norm[i][:,1], newbase, H])
        data_baseline[i] = j       
        
        #determination of maximum or minimum of temperature and Delta CP at Tmax (or Tmin)
        if H[-1] < 0: #if process is endothermic
            Tmax = data_norm[i][np.argmax(data_norm[i][:,1]-newbase),0] 
            header_cooling[i] += '# Peak position is at {:.1f} degC. \n'.format(Tmax)
            DCp = (post_i - pre_i) + (post_s-pre_s)*Tmax
            print('Peak position is at {:.1f} degC'.format(Tmax))
            if 'Mw' in params:
                print('Calculated Delta Cp at the peak position is {:.2g} J/K/mol'.format(DCp))
                header_cooling[i] += '# Calculated Delta Cp at the peak position is {:.2g} J/K/mol. \n'.format(DCp)
            else:
                print('Calculated Delta Cp at the peak position is {:.2g} J/K/g'.format(DCp))
                header_cooling[i] += '# Calculated Delta Cp at the peak position is {:.2g} J/K/g. \n'.format(DCp)
                
        if H[-1] > 0: #if process is exothermic
            Tmin = data_norm[i][np.argmin(data_norm[i][:,1]-newbase),0]
            header_cooling[i] += '# Peak position is at {:.1f} degC'.format(Tmin)
            DCp = (post_i - pre_i) + (post_s-pre_s)*Tmin
            print('Peak position is at {:.1f} degC'.format(Tmin))
            if 'Mw' in params:
                print('Calculated Delta Cp at the peak position is {:.2g} J/K/mol'.format(DCp))
                header_cooling[i] += '# Calculated Delta Cp at the peak position is {:.2g} J/K/mol. \n'.format(DCp)
            else:
                print('Calculated Delta Cp at the peak position is {:.2g} J/K/g'.format(DCp))
                header_cooling[i] += '# Calculated Delta Cp at the peak position is {:.2g} J/K/g. \n'.format(DCp)
                
        header_cooling[i] += 50*'#' + '\n'
    
    return data_baseline

def export_final_data(files, data, params):
    ''' Function which exports the final data-set.'''
    print('\n', 15*'*', 'Exporting the treated data-set', 15*'*')
    
    
    write_header(header_heating, header_cooling, files)
    
    def export(file, data, params):
        filename = os.path.join(os.path.join(params['Folder'],'Output'), 'exp-' + str(file) + '.dat') 
        if 'Mw' in params:
            s = 'Temp/ [degC] \t CP-baseline / [J/K/mol] \t CP [J/K/mol] \t baseline [J/K/mol] \t H [J/mol]'
        else:
            s = 'Temp/ [degC] \t CP-baseline / [J/K/g] \t CP [J/K/g] \t baseline [J/K/g] \t H [J/g]'
        
        with open(filename, 'ab') as f:
            np.savetxt(f, data[i], delimiter='\t', header=s)
        
        
    for i in files['S_heating']:
        export(i, data, params)
    for i in files['S_cooling']:
        export(i, data, params)
        
    return None
    
