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

samples['Sample1'] = {'Folder': '/rawdata',
                      'Heating_runs': ['PDMAEMA_1.5wt.dat'], #['run1.dat', 'run2.dat', 'run3.dat'],
                      'Cooling_runs': [], #['run4.dat', 'run5.dat', 'run6.dat'],
                      'Empty_cell_heat_runs': ['PBS_in_D2O.dat'], #['EC1.dat', 'EC2.dat', 'EC3.dat'],
                      'Empty_cell_cool_runs': [], #['EC4.dat', 'EC5.dat', 'EC6.dat'],
                      'Buffer_heat_runs': [],
                      'Buffer_cool_runs': [],
                      'Dataformat': 'TA_temp_power_time', 
                      'Header_length': 3,
                      'mass_s': 554.3,
                      'mass_r': 534.3,
                      'mass_bb': 0.0,
                      's_wt': 0.015,
                      'Mw': 157.21, #optional, comment out if not needed
                      'ROI_h': [30.0, 90.0],
                      'ROI_c': [15.0, 70.0],
                      'ROP_h': [35.0, 75.0],
                      'ROP_c': [25.0, 55.0],
                      'Scanrate_h': 1.8,
                      'Scanrate_c': 1.2,
                      'bins': 10,
                      'Input': 'exo-down',
                      'Output': 'exo-down',
                      'Exo_in_plot': True, #or False	
                      'unit_time': 's',		
                      'unit_temp': 'degC',
                      'unit_power': 'mW'		
                      }
