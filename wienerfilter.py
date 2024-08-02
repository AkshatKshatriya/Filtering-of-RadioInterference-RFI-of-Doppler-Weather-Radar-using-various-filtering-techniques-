import netCDF4 as nc
import numpy as np
import shutil
from scipy.signal import wiener

def wienerfilter(reflectivity,rfis):
  for i in range(len(rfis)):
    row = rfis[i]
    for j in range(len(reflectivity[i])):
      row_start=max(row-3,0) #range can't be less than 0
      col_start=max(j,0) #range can't be less than 0
      row_end=min(row+4,reflectivity.shape[0])
      col_end=min(j+7,reflectivity.shape[1])
      mat = reflectivity[row_start:row_end,col_start:col_end] #7x7 window

      for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
          filtered_mat = wiener(mat[i][j])
          mat[i][j] = filtered_mat

      reflectivity[row_start:row_end,col_start:col_end] = filtered_mat
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
filtered_reflectivity= wienerfilter(reflectivity, rfis)
