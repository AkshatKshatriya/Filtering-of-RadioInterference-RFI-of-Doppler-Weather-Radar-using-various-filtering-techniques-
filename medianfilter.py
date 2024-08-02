import netCDF4 as nc
import numpy as np
import shutil
from scipy.ndimage import median_filter

def medianfilter(reflectivity,rfis):
    window_size=7
    for i in range(len(rfis)):
        row=rfis[i]
        for j in range(len(reflectivity[i])):
             start_row = max(row - (window_size // 2), 0)
             end_row = min(row + (window_size // 2) + 1, reflectivity.shape[0])
             start_col = max(j - (window_size // 2), 0)
             end_col = min(j + (window_size // 2) + 1, reflectivity.shape[1])
             mat = reflectivity[start_row:end_row,start_col:end_col]
             filtered_mat=median_filter(mat,(7,7))
             for i in range(start_row,end_row):
                 for j in range(start_col,end_col):
                     reflectivity[i][j]=filtered_mat[i-start_row][j-start_col]

    return reflectivity

ncfile=nc.Dataset('copy.nc','a')
reflectivity= ncfile.variables['Reflectivity_Horizontal'][0]
parameter_list= ['Reflectivity_Horizontal']
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
reflectivity= ncfile.variables['Reflectivity_Horizontal'][0]
rfis=[250,285,304,5,210]
filtered_reflectivity= medianfilter(reflectivity, rfis)
