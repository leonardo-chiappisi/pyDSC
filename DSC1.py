# -*- coding: utf-8 -*-
"""
All the functions used by the scripts correction1 are stored in this python file. 
File created on december 2018 by Leonardo Chiappisi
"""
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import interpolate, integrate
from scipy.stats import linregress
#from matplotlib import rc

#import warnings

#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)


def read_files():
    ''' Function which imports all needed data: heating and cooling cycles as well as correction files: 
    Buffer-buffer thermograms and empty cell corrections. The name of the files are stored in the input file 'input.txt'. 
    '''
    files = {'S_heating': '',  'EC_heating': '', 'B_heating': '',
             'S_cooling': '', 'EC_cooling': '',  'B_cooling': ''} #files is a dictionary containing all the file names used in the script.    
       
    with open('Files.txt', 'r') as inp:  #the cycles fills the files dictionary with the filenames stored in the file Files.txt
        for line in inp:
            line = line.split('#')[0] #everything after the # is ignored
            if line.split(':')[0] == 'Sample heating cycles':
                files['S_heating'] =  line.split(':')[1].replace('\n','').replace('\t','').replace(' ','').split(',')  #takes the line with Sample heating cycles and creates a list with all the names, once the end of line symbol and the spaces were removed. 
            elif line.split(':')[0] == 'Empty cell heating cycles':
                files['EC_heating'] =  line.split(':')[1].replace('\n','').replace('\t','').replace(' ','').split(',')  #takes the line with Sample heating cycles and creates a list with all the names, once the end of line symbol and the spaces were removed. 
            elif line.split(':')[0] == 'Buffer heating cycles':
                files['B_heating'] =  line.split(':')[1].replace('\n','').replace('\t','').replace(' ','').split(',')  #takes the line with Sample heating cycles and creates a list with all the names, once the end of line symbol and the spaces were removed. 
            elif line.split(':')[0] == 'Sample cooling cycles':
                files['S_cooling'] =  line.split(':')[1].replace('\n','').replace('\t','').replace(' ','').split(',')  #takes the line with Sample heating cycles and creates a list with all the names, once the end of line symbol and the spaces were removed. 
            elif line.split(':')[0] == 'Empty cell cooling cycles':
                files['EC_cooling'] =  line.split(':')[1].replace('\n','').replace('\t','').replace(' ','').split(',')  #takes the line with Sample heating cycles and creates a list with all the names, once the end of line symbol and the spaces were removed. 
            elif line.split(':')[0] == 'Buffer cooling cycles':
                files['B_cooling'] =  line.split(':')[1].replace('\n','').replace('\t','').replace(' ','').split(',')  #takes the line with Sample heating cycles and creates a list with all the names, once the end of line symbol and the spaces were removed. 
    
    for i in files:  #removes empty elements of the files dictionary in case they are. 
        files[i] = list(filter(None, files[i]))

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
    print(15*'*', 'DATA INPUT', 15*'*')
    print(s, '\n')
    
    print(15*'*', 'DATA Correction', 15*'*')
    if len(files['B_heating']) > 0 and len(files['EC_heating']) > 0:
        print('Heating curves will be corrected by empty cell and buffer-buffer experiments')
    if len(files['B_heating']) > 0 and len(files['EC_heating']) == 0:
        print('Heating curves will be corrected by buffer-buffer experiments')
    if len(files['B_heating']) == 0 and len(files['EC_heating']) > 0:
        print('Heating curves will be corrected by empty cell experiments')
    if len(files['B_heating']) == 0 and len(files['EC_heating']) == 0:
        print('Heating curves will not be corrected with reference measurements')
    if len(files['B_cooling']) > 0 and len(files['EC_cooling']) > 0:
        print('Cooling curves will be corrected by empty cell and buffer-buffer experiments')
    if len(files['B_cooling']) > 0 and len(files['EC_cooling']) == 0:
        print('Cooling curves will be corrected by buffer-buffer experiments')
    if len(files['B_cooling']) == 0 and len(files['EC_cooling']) > 0:
        print('Cooling curves will be corrected by empty cell experiments')
    if len(files['B_cooling']) == 0 and len(files['EC_cooling']) == 0:
        print('Cooling curves will not be corrected with reference measurements')
    
    print('\n')
    return files



def read_params():
    '''Function which reads the parameter input firles and extracts all relevant informations, i.e., sample mass, mw, temperature
    region of interests, regions where the baseline will be evaluated, etc.    
    '''
    params = {'ROI_h': '',    #region of interest for the heating runs. Region in temperature analysed by the program.
              'ROI_c': '',    #region of interest for the heating runs. Region in temperature analysed by the program.
              'mass_s': '',   #mass of the sample solution. in mg
              's_wt': '', #concentration of the sample in weight percent. 
              'mass_bb': '', #mass difference between buffers in the buffer-buffer experiment. in mg
              'mass_r': '', #mass of the solution in the reference cell. in mg
              'Dataformat': '', #Format in which the data are saved. Here the number of columns and which columns need to be extracted is defined.
              'Scanrate_h': '', #Scanrate of the heating experiment, if not automatically detected from the time/temperature data. In K/min. 
              'Scanrate_c': '', #Scanrate of the heating experiment, if not automatically detected from the time/temperature data. In K/min. 
              'bins': '', #Size of the bins used to reduce the file size. i.e., a file of length N is reduced to N/bins, whereby bins number of points are averaged. 
              'ROP_h': '',  #region of peak. Region in temperature where the peak is present in the heating runs. 
              'ROP_c': '',   #region of peak. Region in temperature where the peak is present in the cooling runs. 
              'Mw': ''} #molar mass of sample, used to normalize the data from J/g to J/mol. 
    
    print(15*'*', 'Input Parameters', 15*'*')
    with open('Input_params.txt', 'r') as inp:
        for line in inp:
            line = line.split('#')[0] #everything in the input file after the # is ignored
            for key in params:
                if line.split(':')[0] == key:
                    value = line.split(':')[1].replace('\n','').replace('\t','').replace(' ','').split(',')
                    #print(value[0])
                    if value[0]:
                        params[key] = value  #takes the line with ROI and creates a list with the region of interest. 
                        s = 'Input parameter {} read correctly as {}'.format(key, params[key])
                        print(s)
    print('\n')


    if isinstance(params['Mw'], str):  del params['Mw'] #removes the Mw element if no Mw is provided in the input data file. 
    return params


def extract_data(files, params, *args, **kwargs):
    ''' Extract the time, temperature, heatflow data from the data files as experted from the instrument in the ascii format. 
    Returns a dictionary containing all data files within the region of interest and binned according to bins.     
    The user needs to specify the data format (i.e., from setaram with 4 columns  "Index, time, temperature, heatflow") in the settings_files. 
    setaram4--> Index, time, temperature, heatflow in addition of header of variable length. Beginning of data identifies by the word Furnace
    setaram3--> time, temperature, heatflow in addition of header of variable length. Beginning of data identifies by the word Furnace
    At the end, all files will be saves as time, temperature, heatflow. If the time information is not given, the first column will be filled with zeros.
    
    All file definitions are given in the readme file. TODO
    Availabe data formats are: Setaram3, Setaram4, 3cols, Setaram3temptime
    '''
    print(15*'*', 'Reading data files', 15*'*')
    data = {} #Creation of empty dictionary, where the datasets will be stored, indexed by their filename. 
    for key in files: 
        for j in files[key]: #the two for loops run over all files defined in the file_input definition file. 
            if j:  #this if sentence is made to avoid trying to read empty key values. 
                if params['Dataformat'][0] == 'Setaram3':
                    with open(os.path.join('rawdata', str(j)), 'r', errors='replace') as inp:
                        hl = 1 #length of the header of the file to be read. 
                        line = inp.readline()
                        while 'Furnace' not in line.split():
                            line = inp.readline()
                            hl += 1
                    tmp = np.genfromtxt(os.path.join('rawdata', str(j)), skip_header=hl+1, skip_footer=2, unpack=True, usecols=(0,1,2), encoding='latin1') #imports all data stored in files
                
                if params['Dataformat'][0] == 'Setaram3temptime':
                    with open(os.path.join('rawdata', str(j)), 'r', errors='replace') as inp:
                        hl = 1 #length of the header of the file to be read. 
                        line = inp.readline()
                        while 'Furnace' not in line.split():
                            line = inp.readline()
                            hl += 1
                    tmp = np.genfromtxt(os.path.join('rawdata', str(j)), skip_header=hl+1, skip_footer=2, unpack=True, usecols=(1,0,2), encoding='latin1') #imports all data stored in files
                elif params['Dataformat'][0] == 'Setaram4':
                    with open(os.path.join('rawdata', str(j)), 'r', errors='replace') as inp:
                        hl = 1 #length of the header of the file to be read. 
                        line = inp.readline()
                        while 'Furnace' not in line.split():
                            line = inp.readline()
                            hl += 1
                    tmp = np.genfromtxt(os.path.join('rawdata', str(j)), skip_header=hl+1, skip_footer=2, unpack=True, usecols=(1,2,3), encoding='latin1') #imports all data stored in files
                    
                elif params['Dataformat'][0] == '3cols':
                    with open(os.path.join('rawdata', str(j)), 'r', errors='replace') as inp:
                        hl = 1 #length of the header of the file to be read. 
                    tmp = np.genfromtxt(os.path.join('rawdata', str(j)), skip_header=hl, skip_footer=2, unpack=True, usecols=(0,1,2)) #imports all data stored in files
                

                if 'heating' in key:
                    mask = ((float(params['ROI_h'][0]) < tmp[1,:]) & (float(params['ROI_h'][1]) > tmp[1,:])) #defines a mask with the points where the temperature is in the region of interest. 
                elif 'cooling' in key:
                    mask = ((float(params['ROI_c'][0]) < tmp[1,:]) & (float(params['ROI_c'][1]) > tmp[1,:])) #defines a mask with the points where the temperature is in the region of interest. 
                tmp2 = tmp[:,mask] #creates the data array with only the relevant data points. Whatever is outside the region of interest, is not used any longer. 
                data_set = binning(tmp2, params)  #the data are binned according to the size defined by bins. No binning is performed if binsize is 1 or less. 
            data[j] = data_set
            print('Datafile {} read correctly'.format(j))
    print('\n')
    return data #a dictionary containing all data, already cut, binned, and with the heatrate calculated. 


def binning(data, params):
    ''' Function which bins the data array. width points are averaged and an array of length original length//width is retuned.
    No binning is performed when the binsize is smaller or equal to 1. Heatrate is also calculated if the time-temperature data are available. 
    Before binning, if the original file is not a multiple of width, the exceeding points are dropped. '''
    width = int(params['bins'][0])
    if int(params['bins'][0]) > 1:
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
                    raise Exception('Error: {} is not a heating file!'.format(i))
#Verification for a constant heatrate and if it is consistent with the one provided in parameter file. 
                hr, hrstd = data[i][4,:].mean()*60, data[i][4,:].std()*60
                if hrstd/hr > 0.02:
                    W_counter += 1
                    print('Warning {}: the heatrate is not constant and varies by {:.2g}% for file {}.'.format(W_counter, hrstd/hr*100, i))
                if not (0.95 <= (float(params['Scanrate_h'][0])/hr) <= 1.05): #veryfies consistency with input parameter file
                    print('Warning {}: the determined heatrate of file {} is {:.2g} K/min \
and is not consistent with the one provided in the input parameter file of {:.2g} K/min.'.format(W_counter, i, hr, float(params['Scanrate_h'][0])))
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
                if hrstd/hr > 0.02:
                    W_counter += 1
                    print('Warning {}: the heatrate is not constant and varies by {:.2g}% for file {}.'.format(W_counter, hrstd/hr*100, i))
                if not (0.95 <= (-float(params['Scanrate_c'][0])/hr) <= 1.05): #veryfies consistency with input parameter file
                    print('Warning {}: the determined heatrate of file {} is {:.2g} K/min \
and is not consistent with the one provided in the input parameter file of {:.2g} K/min.'.format(W_counter, i, hr, float(params['Scanrate_c'][0])))
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
                    print('File {} will be ignored in all successive calculations.'.format(i))
                    del data[i]
                    files[key].remove(i)
            if 'heating' in key:
                if minT-1.0 > float(params['ROI_h'][0]) or maxT+1.0 < float(params['ROI_h'][1]):
                    D_counter += 1
                    print('Error: temperature range of file {} does not cover the region of interest!'.format(i))
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
    if params['ROP_h'][0] <  params['ROI_h'][0] or params['ROP_h'][1] >  params['ROI_h'][1]:
        raise Exception('Peak in heating run falls out of region of interest. Verify the regions of interest and the region of peak.')
    if params['ROP_c'][0] <  params['ROI_c'][0] or params['ROP_c'][1] >  params['ROI_c'][1]:
        raise Exception('Peak in cooling run falls out of region of interest. Verify the regions of interest and the region of peak.')
            

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
        if np.shape(refs['B_cooling'])[0]:
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
        if np.shape(refs['B_cooling'])[0]: #if buffer was measured
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
        if np.shape(refs['B_heating'])[0]:
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
                   data_corrected = data[i][2,:] - EC_interpol #corrects the sample data for the empty cell measurement. 
                   data_c[i] = np.array([data[i][0,:], data[i][1,:], data_corrected, data[i][3,:], data[i][4,:]])
    else: #if the empty cell was not measured
        if np.shape(refs['B_heating'])[0]: #if buffer was measured
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
    sample_norm = float(params['mass_s'][0])*float(params['s_wt'][0])/1000*1000   #Normalization factor given by the sample mass in grams and from mW to W
    if 'Mw' in params:
        sample_norm /= float(params['Mw'][0])  #if Mw is provided, the data will be normalized by the moles of compound. 
    
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
            print('Iteration number {}, enthalpy variation of {:3g} J/mol, final value of DH is {:2g} +- {:.2g} J/mol'.format(itermax, abs(DH/H[-1]), H[-1], errH))
        else:
            print('Iteration number {}, enthalpy variation of {:3g} J/g, final value of DH is {:2g} +- {:.2g} J/g'.format(itermax, abs(DH/H[-1]), H[-1], errH))
        j = np.column_stack([data_norm[i][:,0], data_norm[i][:,1]-newbase, data_norm[i][:,1], newbase, H])
        data_baseline[i] = j
        

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
            print('Iteration number {}, enthalpy variation of {:.3g} J/mol, final value of DH is {:2g} +- {:.2g} J/mol'.format(itermax, abs(DH/H[-1]), H[-1], errH))
        else:
            print('Iteration number {}, enthalpy variation of {:.3g} J/g, final value of DH is {:2g} +- {:.2g} J/g'.format(itermax, abs(DH/H[-1]), H[-1], errH))
        
        
        j = np.column_stack([data_norm[i][:,0], data_norm[i][:,1]-newbase, data_norm[i][:,1], newbase, H])
        data_baseline[i] = j       
        
    
    return data_baseline

def export_final_data(files, data, params):
    ''' Function which exports the final data-set.'''
    print('\n', 15*'*', 'Exporting the treated data-set', 15*'*')
    
    def export(file, data, params):
        filename = os.path.join('Output', 'exp-' + str(file)) 
        #with open(os.path.join('export', filename), 'w+') as f:
        s = '# Data threated with pyDSC, version xxxx, \n'
        s += '#More information here? \n'
        if 'Mw' in params:
            s += '#Temp/ [degC] \t CP-baseline / [J/K/mol] \t CP [J/K/mol] \t baseline [J/K/mol] \t H [J/mol]'
        else:
            s += '#Temp/ [degC] \t CP-baseline / [J/K/g] \t CP [J/K/g] \t baseline [J/K/g] \t H [J/g]'
        
        np.savetxt(filename, data[i], delimiter='\t', header=s)
            
        
        
        
        
    for i in files['S_heating']:
        export(i, data, params)
    for i in files['S_cooling']:
        export(i, data, params)
    
