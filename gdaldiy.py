#!/usr/bin/env python
# coding: utf-8

# In[2]:


from osgeo import gdal


# In[3]:


import numpy as np


# In[4]:


list1 = ["byte","uint8","uint16","int16","uint32","int32","float32","float64","cint16","cint32","cfloat32","cfloat64"]


# In[5]:


list2 = [gdal.GDT_Byte,gdal.GDT_Byte,gdal.GDT_UInt16,gdal.GDT_Int16,gdal.GDT_UInt32,gdal.GDT_Int32,gdal.GDT_Float32,gdal.GDT_Float64,gdal.GDT_CInt16,gdal.GDT_CInt32,gdal.GDT_CFloat32,gdal.GDT_CFloat64]


# In[6]:


def imgread(path):
    img = gdal.Open(path)
    # col = img.RasterXSize #col
    # row = img.RasterYSize #row
    # img_arr = img.ReadAsArray(0,0,col,row) 
    c = img.RasterCount
    img_arr = img.ReadAsArray() 
    if c>1:
        img_arr = img_arr.swapaxes(1,0)
        img_arr = img_arr.swapaxes(2,1)
    del img
    return img_arr
def imgwrite(path,narray,compress="None"):
    s=narray.shape
    dt_name=narray.dtype.name
    for i in range(len(list1)):
        if list1[i] in dt_name.lower():
            datatype=list2[i]
            break
        else:
            datatype=list2[0]
    if len(s)==2:
        row,col,c=s[0],s[1],1
        driver = gdal.GetDriverByName('GTiff')
        dataset = driver.Create(path,col,row,c,datatype,options=["COMPRESS="+compress])
        dataset.GetRasterBand(1).WriteArray(narray)
        del dataset
    elif len(s)==3:
        row,col,c = s[0], s[1], s[2]
        driver = gdal.GetDriverByName('GTiff')
        dataset = driver.Create(path,col,row, c, datatype)
        for i in range(c):
            dataset.GetRasterBand(i + 1).WriteArray(narray[:,:,i])
        del dataset


# In[ ]:




