samples = {}   
'''A dictionary which contains all the relevant information of the samples to be threated. 
All samples defined here in will be analysed by pyDSC.
- Folder:                    relative path to pyDSC.py where datafiles are stored.
- Heating_runs:              list containing the filenames of the ASCII files with raw heating data.
- Cooling_runs:              list containing the filenames of the ASCII files with raw cooling data.
- Empty_cell_heat_runs:      list containing the filenames of the ASCII files with raw heating data of the empty cell measurement.
- Empty_cell_cool_runs:      list containing the filenames of the ASCII files with raw cooling data of the empty cell measurement.
- Buffer_heat_runs:          list containing the filenames of the ASCII files with raw heating data of the buffer measurement.
- Buffer_cool_runs:          list containing the filenames of the ASCII files with raw cooling data of the buffer measurement.
///
Dataformat: TA_temp_power_time  	#Dataformat in which data are saved. See the readme for all possibilities and examples. 
Header_length: 3	#Length of the file header, needed only for the dataformat which need to have the header length to be specified. 
ROI_h: 30.0, 90.0 	#Region of interest for the heating runs, please indicate the range of temperatures probed by the program. 
ROI_c: 10.0, 60.0 	#Region of interest for the cooling runs, please indicate the range of temperatures probed by the program. 
mass_s: 552 		#mass of the sample solution, in mg
mass_r: 0.0 		#mass of the solution in the reference cell, in mg
mass_bb: 0.0 		#[needed for buffer correctoion] mass difference between the buffer solution in the sample cell and in the reference (sample-reference) in the buffer-buffer experiment, in mg. If no buffer-buffer experiment was performed, this line will be ignored.
s_wt: 0.015 		#Concentration of the sample, in weight percent. 1% will be 0.01; 100% is 1.0
Scanrate_h: 1.0		#Scanrate for the heating experiments, in K/min. If the data contain the time and temperature information, this line will be ignored. 
Scanrate_c: 1.2 	#Scanrate for the cooling experiments, in K/min. If the data contain the time and temperature information, this line will be ignored.
bins: 10 		#Size of the bins used to reduce the file size. i.e., a file of length N is reduced to N/bins, whereby bins number of points are averaged.
ROP_h: 36.0, 85.0	#region where the peak is found in the heating scans
ROP_c: 15.0, 42.0	#region where the peak is found in the cooling scans
Mw: 157.21	#[optional]Provide Mw in g/mol for data in J/mol instead of J/g. 
Input: exo-down		#Convention used for input files, can be exo-up or exo-down. 	
Output: exo-down	#Convention used for output files, can be exo-up or exo-down. 
Exo_in_plot: true	#(True or False) If True, an arrow indicating the Exo-up or Exo-down convention will be put in the DSC output plots. 	
unit_time: s		#Unit in which the time is given, can be either min or s
unit_temp: degC		#Unit in which the temperature is given, can be K or degC
unit_power: mW		#Unit in which the heatflow is given, can be uW (microWatt), mW (milliWatt), or W (Watt)
'''


# samples['Myoglobin_cell1_first_run'] = {'Folder': 'rawdata/John_White',
#                       'Heating_runs': ['myoglobin_cell1_scan2.txt'],
#                       'Cooling_runs': ['myoglobin_cell1_scan3.txt'], 
#                       'Empty_cell_heat_runs': [], 
#                       'Empty_cell_cool_runs': [], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       # 'Header_length': 1,
#                       'mass_s': 502.8,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.0072,
#                       # 'Mw': 157.2, #optional, comment out if not needed
#                       'ROI_h': [35, 56],
#                       'ROI_c': [62, 82],
#                       'ROP_h': [46 , 53],
#                       'ROP_c': [70, 78],
#                       'Scanrate_h': 0.5,
#                       'Scanrate_c': 0.5,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': True, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'uW'
#                       }

# samples['Myoglobin_cell1_other_runs'] = {'Folder': 'rawdata/John_White',
#                       'Heating_runs': ['myoglobin_cell1_scan4.txt', 'myoglobin_cell1_scan6.txt', 'myoglobin_cell1_scan8.txt', 'myoglobin_cell1_scan10.txt'],
#                       'Cooling_runs': ['myoglobin_cell1_scan5.txt', 'myoglobin_cell1_scan7.txt', 'myoglobin_cell1_scan9.txt', 'myoglobin_cell1_scan11.txt'],
#                       'Empty_cell_heat_runs': [], 
#                       'Empty_cell_cool_runs': [], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       # 'Header_length': 1,
#                       'mass_s': 502.8,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.0072,
#                       # 'Mw': 157.2, #optional, comment out if not needed
#                       'ROI_h': [78, 94],
#                       'ROI_c': [62, 82],
#                       'ROP_h': [82 , 90],
#                       'ROP_c': [65, 75],
#                       'Scanrate_h': 0.5,
#                       'Scanrate_c': 0.5,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': True, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'uW'
#                       }

samples['Myoglobin_cell2_runs'] = {'Folder': 'rawdata/John_White',
                      'Heating_runs': ['myoglobin_cell2_scan2.txt', 'myoglobin_cell2_scan4.txt', 'myoglobin_cell2_scan6.txt', 'myoglobin_cell2_scan8.txt', 'myoglobin_cell2_scan10.txt'],
                      'Cooling_runs': ['myoglobin_cell2_scan3.txt', 'myoglobin_cell2_scan5.txt', 'myoglobin_cell2_scan7.txt', 'myoglobin_cell2_scan9.txt', 'myoglobin_cell2_scan11.txt'],
                      'Empty_cell_heat_runs': [], 
                      'Empty_cell_cool_runs': [], 
                      'Buffer_heat_runs': [],
                      'Buffer_cool_runs': [],
                      'Dataformat': 'TA_temp_power_time', 
                      # 'Header_length': 1,
                      'mass_s': 502.8,
                      'mass_r': 0.0,
                      'mass_bb': 0.0,
                      's_wt': 0.0072,
                      # 'Mw': 157.2, #optional, comment out if not needed
                      'ROI_h': [78, 94],
                      'ROI_c': [60, 80],
                      'ROP_h': [82 , 90],
                      'ROP_c': [65, 75],
                      'Scanrate_h': 0.5,
                      'Scanrate_c': 0.5,
                      'bins': 10,
                      'Input': 'exo-down',
                      'Output': 'exo-down',
                      'Exo_in_plot': True, #or False	
                      'unit_time': 's',		
                      'unit_temp': 'degC',
                      'unit_power': 'uW'
                      }


# samples['Sample2_normal'] = {'Folder': 'C2',
#                       'Heating_runs': ['C2_2Heat_mid.txt', 'C2_4Heat_mid.txt', 'C2_6Heat_mid.txt'],
#                       'Cooling_runs': ['C2_1Cool_mid.txt', 'C2_3Cool_mid.txt', 'C2_5Cool_mid.txt'], 
#                       'Empty_cell_heat_runs': ['EC2_2Heat_rate0.5.txt', 'EC2_4Heat_rate0.5.txt', 'EC2_6Heat_rate0.5.txt'], 
#                       'Empty_cell_cool_runs': ['EC2_1Cool_rate1.txt', 'EC2_3Cool_rate1.txt', 'EC2_5Cool_rate1.txt'], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       'Header_length': 1,
#                       'mass_s': 225.3,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.8741,
#                       #'Mw': 4600, #optional, comment out if not needed
#                       'ROI_h': [-18.0, -6.0],
#                       'ROI_c': [-20.0, -13.8],
#                       'ROP_h': [-9.1 , -9.0],
#                       'ROP_c': [-17.1 , -17.0],
#                       'Scanrate_h': 0.5,
#                       'Scanrate_c': 1.0,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': False, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'W'		#EIGENTLICH uW
#                       }

#COOL Scan1 und Heat2 raus, da sehr anders: 'C3_2Heat_rate0.5.txt', 
# samples['Sample3_normal'] = {'Folder': 'C3',
#                       'Heating_runs': ['C3_4Heat_mid.txt', 'C3_6Heat_mid.txt'],
#                       'Cooling_runs': ['C3_3Cool_mid.txt', 'C3_5Cool_rate1.txt'], 
#                       'Empty_cell_heat_runs': ['EC3_2Heat_rate0.5.txt', 'EC3_4Heat_rate0.5.txt', 'EC3_6Heat_rate0.5.txt'], 
#                       'Empty_cell_cool_runs': ['EC3_1Cool_rate1.txt', 'EC3_3Cool_rate1.txt', 'EC3_5Cool_rate1.txt'], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       'Header_length': 1,
#                       'mass_s': 287.1,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.5638,
#                       #'Mw': 4600, #optional, comment out if not needed
#                       'ROI_h': [-20.0, -6.0],
#                       'ROI_c': [-23.0, -14.8],
#                       'ROP_h': [-13.1 , -13.0],
#                       'ROP_c': [-17.1 , -17.0],
#                       'Scanrate_h': 0.5,
#                       'Scanrate_c': 1.0,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': False, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'W'		#EIGENTLICH uW
#                       }

# samples['Sample1_slow'] = {'Folder': 'C1',
#                       'Heating_runs': ['C1_8Heat_rate0.1.txt', 'C1_10Heat_rate0.1.txt', 'C1_12Heat_rate0.1.txt'],
#                       'Cooling_runs': ['C1_7Cool_rate0.1.txt', 'C1_9Cool_rate0.1.txt', 'C1_11Cool_rate0.1.txt'], 
#                       'Empty_cell_heat_runs': ['EC1_8Heat_rate0.1.txt', 'EC1_10Heat_rate0.1.txt', 'EC1_12Heat_rate0.1.txt'], 
#                       'Empty_cell_cool_runs': ['EC1_7Cool_rate0.1.txt', 'EC1_9Cool_rate0.1.txt', 'EC1_11Cool_rate0.1.txt'], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       'Header_length': 1,
#                       'mass_s': 203.5,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.9835,
#                       #'Mw': 4600, #optional, comment out if not needed
#                       'ROI_h': [-23.0, -6.0],
#                       'ROI_c': [-23.0, -6.0],
#                       'ROP_h': [-10.1 , -10.0],
#                       'ROP_c': [-15.1 , -15.0],
#                       'Scanrate_h': 0.1,
#                       'Scanrate_c': 0.1,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': False, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'W'		#EIGENTLICH uW
#                       }

# samples['Sample2_slow'] = {'Folder': 'C2',
#                       'Heating_runs': ['C2_8Heat_rate0.1.txt', 'C2_10Heat_rate0.1.txt', 'C2_12Heat_rate0.1.txt'],
#                       'Cooling_runs': ['C2_7Cool_rate0.1.txt', 'C2_9Cool_rate0.1.txt', 'C2_11Cool_rate0.1.txt'], 
#                       'Empty_cell_heat_runs': ['EC2_8Heat_rate0.1.txt', 'EC2_10Heat_rate0.1.txt', 'EC2_12Heat_rate0.1.txt'], 
#                       'Empty_cell_cool_runs': ['EC2_7Cool_rate0.1.txt', 'EC2_9Cool_rate0.1.txt', 'EC2_11Cool_rate0.1.txt'], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       'Header_length': 1,
#                       'mass_s': 225.3,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.8741,
#                       #'Mw': 4600, #optional, comment out if not needed
#                       'ROI_h': [-23.0, -6.0],
#                       'ROI_c': [-23.0, -8.0],
#                       'ROP_h': [-17.1 , -17.0],
#                       'ROP_c': [-16.1 , -16.0],
#                       'Scanrate_h': 0.1,
#                       'Scanrate_c': 0.1,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': False, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'W'		#EIGENTLICH uW
#                       }

# samples['Sample3_slow'] = {'Folder': 'C3',
#                       'Heating_runs': ['C3_8Heat_rate0.1.txt', 'C3_10Heat_rate0.1.txt', 'C3_12Heat_rate0.1.txt'],
#                       'Cooling_runs': ['C3_7Cool_rate0.1.txt', 'C3_9Cool_rate0.1.txt', 'C3_11Cool_rate0.1.txt'], 
#                       'Empty_cell_heat_runs': ['EC3_8Heat_rate0.1.txt', 'EC3_10Heat_rate0.1.txt', 'EC3_12Heat_rate0.1.txt'], 
#                       'Empty_cell_cool_runs': ['EC3_7Cool_rate0.1.txt', 'EC3_9Cool_rate0.1.txt', 'EC3_11Cool_rate0.1.txt'], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       'Header_length': 1,
#                       'mass_s': 287.1,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.5638,
#                       #'Mw': 4600, #optional, comment out if not needed
#                       'ROI_h': [-23.0, -6.0],
#                       'ROI_c': [-23.0, -10.0],
#                       'ROP_h': [-15.1 , -15.0],
#                       'ROP_c': [-16.1 , -16.0],
#                       'Scanrate_h': 0.1,
#                       'Scanrate_c': 0.1,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': False, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'W'		#EIGENTLICH uW
#                       }

#entweder cool auf hohere Temp
# samples['Sample1_fast'] = {'Folder': 'C1',
#                       'Heating_runs': ['C1_14Heat_rate2.txt', 'C1_16Heat_rate2.txt', 'C1_18Heat_rate2.txt'],
#                       'Cooling_runs': ['C1_13Cool_rate2.txt', 'C1_15Cool_rate2.txt', 'C1_17Cool_rate2.txt'], 
#                       'Empty_cell_heat_runs': ['EC1_14Heat_rate2.txt', 'EC1_16Heat_rate2.txt', 'EC1_18Heat_rate2.txt'], 
#                       'Empty_cell_cool_runs': ['EC1_13Cool_rate2.txt', 'EC1_15Cool_rate2.txt', 'EC1_17Cool_rate2.txt'], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       'Header_length': 1,
#                       'mass_s': 203.5,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.9835,
#                       #'Mw': 4600, #optional, comment out if not needed
#                       'ROI_h': [-23.0, -6.0],
#                       'ROI_c': [-22.0, -17.0],
#                       'ROP_h': [-10.1 , -10.0],
#                       'ROP_c': [-18.1 , -18.0],
#                       'Scanrate_h': 2.0,
#                       'Scanrate_c': 2.0,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': False, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'W'		#EIGENTLICH uW
#                       }

# samples['Sample2_fast'] = {'Folder': 'C2',
#                       'Heating_runs': ['C2_14Heat_rate2.txt', 'C2_16Heat_rate2.txt', 'C2_18Heat_rate2.txt'],
#                       'Cooling_runs': ['C2_13Cool_rate2.txt', 'C2_15Cool_rate2.txt', 'C2_17Cool_rate2.txt'], 
#                       'Empty_cell_heat_runs': ['EC2_14Heat_rate2.txt', 'EC2_16Heat_rate2.txt', 'EC2_18Heat_rate2.txt'], 
#                       'Empty_cell_cool_runs': ['EC2_13Cool_rate2.txt', 'EC2_15Cool_rate2.txt', 'EC2_17Cool_rate2.txt'], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       'Header_length': 1,
#                       'mass_s': 225.3,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.8741,
#                       #'Mw': 4600, #optional, comment out if not needed
#                       'ROI_h': [-17.0, -6.0],
#                       'ROI_c': [-23.0, -16.0],
#                       'ROP_h': [-10.1 , -10.0],
#                       'ROP_c': [-18.1 , -18.0],
#                       'Scanrate_h': 2.0,
#                       'Scanrate_c': 2.0,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': False, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'W'		#EIGENTLICH uW
#                       }

# samples['Sample3_fast'] = {'Folder': 'C3',
#                       'Heating_runs': ['C3_14Heat_rate2.txt', 'C3_16Heat_rate2.txt', 'C3_18Heat_rate2.txt'],
#                       'Cooling_runs': ['C3_13Cool_rate2.txt', 'C3_15Cool_rate2.txt', 'C3_17Cool_rate2.txt'], 
#                       'Empty_cell_heat_runs': ['EC1_14Heat_rate2.txt', 'EC1_16Heat_rate2.txt', 'EC1_18Heat_rate2.txt'], 
#                       'Empty_cell_cool_runs': ['EC1_13Cool_rate2.txt', 'EC1_15Cool_rate2.txt', 'EC1_17Cool_rate2.txt'], 
#                       'Buffer_heat_runs': [],
#                       'Buffer_cool_runs': [],
#                       'Dataformat': 'TA_temp_power_time', 
#                       'Header_length': 1,
#                       'mass_s': 287.1,
#                       'mass_r': 0.0,
#                       'mass_bb': 0.0,
#                       's_wt': 0.5638,
#                       #'Mw': 4600, #optional, comment out if not needed
#                       'ROI_h': [-17.0, -6.0],
#                       'ROI_c': [-23.0, -16.0],
#                       'ROP_h': [-10.1 , -10.0],
#                       'ROP_c': [-18.1 , -18.0],
#                       'Scanrate_h': 2.0,
#                       'Scanrate_c': 2.0,
#                       'bins': 10,
#                       'Input': 'exo-down',
#                       'Output': 'exo-down',
#                       'Exo_in_plot': False, #or False	
#                       'unit_time': 's',		
#                       'unit_temp': 'degC',
#                       'unit_power': 'W'		#EIGENTLICH uW
#                       }

