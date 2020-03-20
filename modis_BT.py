# -*- coding: utf-8 -*-

# Редактор Spyder

# Это временный скриптовый файл.



from pyhdf.SD import SD, SDC
import pprint
import numpy as np
from matplotlib import pyplot as plt



file_name = "F:/0nti_modis/MODIS/20191125_101530_AQUA_MOD021KM.hdf"
print(f'reading {file_name}')
the_file = SD(file_name, SDC.READ)
stars='*'*50
print((f'\n{stars}\nnumber of datasets, number of attributes'
       f'={the_file.info()}\n{stars}\n'
       f'\nHere is the help file for the info funtion:\n'))
help(SD.info)

datasets_dict = the_file.datasets()

for idx,sds in enumerate(datasets_dict.keys()):
    print(idx,sds)


longwave_data = the_file.select('EV_1KM_Emissive') # select sds
print(longwave_data.info())
help(longwave_data.info)


data_row = longwave_data[0,0,:] # get sds data
print(data_row.shape,data_row.dtype)

longwave_data[0,:,:]

pprint.pprint(longwave_data.attributes() )


pprint.pprint(the_file.attributes()['StructMetadata.0'][:1000])

longwave_bands = the_file.select('Band_1KM_Emissive')

longwave_bands.attributes()

band_nums=longwave_bands.get()
print(f'here are the modis channels in the emissive dataset \n{band_nums}')

ch31_index=np.searchsorted(band_nums,31.)
print(ch31_index.dtype)
ch31_index = int(ch31_index)
print(f'channel 31 is located at index {ch31_index}')

ch31_data = longwave_data[ch31_index,:,:]
print(ch31_data.shape)
print(ch31_data.dtype)


fig,ax = plt.subplots(1,1,figsize = (10,14))

# CS=ax.imshow(ch31_data)
# cax=fig.colorbar(CS)
# ax.set_title('uncalibrated counts')
#
# add a label to the colorbar and flip it around 270 degrees
#
# out=cax.ax.set_ylabel('Chan 31 raw counts')
# out.set_verticalalignment('bottom')
# out.set_rotation(270)
# print(ch31_data.shape)


scales=longwave_data.attributes()['radiance_scales']
offsets=longwave_data.attributes()['radiance_offsets']
ch31_scale=scales[ch31_index]
ch31_offset=offsets[ch31_index]
print(f'scale: {ch31_scale}, offset: {ch31_offset}')

ch31_calibrated =(ch31_data - ch31_offset)*ch31_scale




# CS=ax.imshow(ch31_calibrated)
# cax=fig.colorbar(CS)
# ax.set_title('Channel 31 radiance')

#
# add a label to the colorbar and flip it around 270 degrees

# out=cax.ax.set_ylabel('Chan radiance $(W\,m^{-2}\,\mu m^{-1}\,sr^{-1})$')
# out.set_verticalalignment('bottom')
# out.set_rotation(270)
# ch31_calibrated.shape

chisl=(1.4387752*(10**4))/11.030
chisl1=(1.19104282*(10**8)) * (11.030**(-5))
rez=np.divide(chisl1, ch31_calibrated)
znam=np.log(1+rez)
ch31_temp=np.divide(chisl, znam)
#ch31_temp=np.subtract(ch31_temp, 273.15)
print(type(ch31_temp))
ch31_temp_rot= np.rot90(ch31_temp, 2)

Temp=ax.imshow(ch31_temp_rot)
cax=fig.colorbar(Temp)


ax.set_title('Channel 31 Brightness temperature ')
out=cax.ax.set_ylabel('Temperature Kelvin')
out.set_verticalalignment('bottom')
out.set_rotation(270)

print(ch31_temp_rot.shape)



# Create an HDF file
outname="F:/0nti_modis/ch31_out.hdf"
sd = SD(outname, SDC.WRITE | SDC.CREATE)

# Create a dataset
sds = sd.create("ch31", SDC.FLOAT64, ch31_temp_rot.shape)

# Fill the dataset with a fill value
sds.setfillvalue(0)

# Set dimension names
dim1 = sds.dim(0)
dim1.setname("col")
dim2 = sds.dim(1)
dim2.setname("row")

# Assign an attribute to the dataset
sds.units = 'K'

# Write data
sds[:,:] = ch31_temp_rot

# Close the dataset
sds.endaccess()

# Flush and close the HDF file
sd.end()
