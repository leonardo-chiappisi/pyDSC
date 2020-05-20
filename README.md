# pyDSC
Set of python scripts for the correction of DSC data. 


The program normalizes the rawdata, corrects for the empty cell and buffer contributions (if provided), and performs a baseline subtraction. Values like enthalpy change, heat capacity change are autamically calculated. For further informations please refer to the manual of the program. 

## Usage

To run the program, you need to download the files *'DSC1.py'*, *'dsc_plot.py'*, and *'pyDSC.py'*. In the same folder, save the files 'Files.txt' and 'Input_params.txt'. Create a folder called rawdata and Output. In the folder 'rawdata', please save all the files to be analyzed: the samples and eventual reference measurements (buffer-buffer and empty cell runs). Refer to the manual for more detailed information. 

Modify the files 'Files.txt' and 'Input_params.txt' according to your needs. 

To run the program, execute the python script pyDSC.py with:

```
python3 pyDSC.py
```

The script is based on python3 and requires the numpy and scipy packages. 

## Feedback
The format of the rawdata read by the script is still relatively limited. The suggestion of new formats is highly welcomed. Please mail to chiappisil@ill.eu. Also, feedback from the users is very welcome. 

