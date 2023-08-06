# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:15:47 2020

@author: mofarrag
"""
"""
Make sure the working directory is set to the examples folder in the Hapi repo"
currunt_work_directory = Hapi/Example
"""
import os
os.chdir("F:/01Algorithms/Hydrology/HAPI/Examples/")
import geopandas as gpd
# import numpy as np
# import pandas as pd
from Hapi.inputs import Inputs as IN

BasinF = "data/GIS/Hapi_GIS_Data/BasinExtractParameters.shp"
SaveTo = "data/parameters"
#%%
Basin = gpd.read_file(BasinF)
# parameters name with the same order inside the Input module
# ind = ["tt","sfcf","cfmax","cwh","cfr","fc","beta","lp","k0","k1","k2","uzl","perc","maxbas"]
# Par = pd.DataFrame(index = ind)
# extract parameters boundaries
Par = IN.ExtractParametersBoundaries(Basin)

# extract parameters in a specific scenarion from the 10 scenarios
Par['1'] = IN.ExtractParameters(Basin,"10")
"""
zoom to the place where the catchment exist to check if the basin polygon overlay
the right location, if not there is a problem in the coordinate reference system
transformation
"""
#%% save the parameters
Par['UB'].to_csv(SaveTo + "/UB-Extracted.txt", header=None,float_format="%4.3f")
Par['LB'].to_csv(SaveTo + "/LB-Extracted.txt", header=None,float_format="%4.3f")
Par['1'].to_csv(SaveTo + "/scenario1.txt", header=None,float_format="%4.3f")
