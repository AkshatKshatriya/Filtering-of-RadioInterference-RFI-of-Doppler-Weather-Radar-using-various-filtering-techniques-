import netCDF4 as nc
import numpy as np
import shutil

def thresholdfilter(rfis,rxpower_horizontal,threshold):
    big_rfi = [] # including a time-window
    for i in range(len(rfis)):
        for j in range(rfis[i]-6,rfis[i]+6):
            big_rfi.append(j%360) #if angles goes beyond 360
            
    big_threshold = []
    for i in range(len(threshold)):
        for j in range(12):
            big_threshold.append(threshold[i])
            
    for j in range(len(big_rfi)):
        for i in range(len(rxpower_horizontal[big_rfi[j]])):
            if rxpower_horizontal[big_rfi[j]][i] < big_threshold[j]:
                rxpower_horizontal[big_rfi[j]][i] = np.nan
       
    return rxpower_horizontal
    
shutil.copy('DWRIGCAR-Level1A-IGCAR_OPERATIONAL1-13-IGCAR_OPERATIONAL_400KM-2024-05-06-114730-ELE-0.2.nc','thresholdfilter.nc')
ncfile = nc.Dataset('thresholdfilter.nc','a')

parameter_list= ['RxPower_Horizontal']
angles = ncfile.variables['Azimuth_Info'][0]
starting_angle = int(angles[0])
starting_index = 360 - starting_angle
angles = np.roll(angles,-starting_index)
ncfile.variables['Azimuth_Info'][0] = angles 
for parameter in parameter_list:
    mat = ncfile.variables[parameter][0] 
    for j in range(mat.shape[1]):
        col = mat[:,j]
        col = np.roll(col, -starting_index)
        mat[:,j] = col  
    ncfile.variables[parameter][0] = mat  

rxpower_horizontal= ncfile.variables['RxPower_Horizontal'][0]
rfis = [250,343,356,4,304,285]
threshold = [-114,-116,-118,-105,-116,-123]
filtered_rxpower= thresholdfilter(rfis,rxpower_horizontal,threshold)
ncfile.variables['RxPower_Horizontal'][0] = filtered_rxpower
ncfile.close()

