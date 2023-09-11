# pyDSC
Set of python scripts for the correction of DSC data. 


The program normalizes the rawdata, corrects for the empty cell and buffer contributions (if provided), and performs a baseline subtraction. Values like enthalpy change, heat capacity change are autamically calculated. For further informations please refer to the manual of the program. 

## Usage

To run the program, you need to download the files *'DSC1.py'*, *'dsc_plot.py'*, *'dsc_input.py'*, and *'pyDSC.py'*. In the same folder, save the files 'Files.txt' and 'Input_params.txt'.  Modify the file 'dsc_input.py' according to your needs. Please refer to the Handbook for further details. 

To run the program, execute the python script pyDSC.py with:

```
python3 pyDSC_vx.x.x..py
```

The script is based on python3 and requires the numpy and scipy packages. 

## Feedback
The format of the rawdata read by the script is still relatively limited. The suggestion of new formats is highly welcomed. Please mail to chiappisil@ill.eu. Also, feedback from the users is very welcome. 

