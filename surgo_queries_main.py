###########################################################
#Author: Abhishes lamsal
#Purpose: Extract the mapunit, musymbol, and areasymbol of any given lattitude and longitude
# DOne for Precision Agriculture Lab
# COpyright: lamsal abhishes
# Email: abhilam@ksu.edu
#necessasry packages

import json
import requests
import pandas as pd
import xml.etree.ElementTree as EM
import os

from SSURGO_Queries import SolDataExtractor
from Soil_MUKey_Extractor import MUextract

def main():
    os.chdir('C:\\Users\\abhilam\\Desktop\\Abhi\\KMZ_Data\\')
    filename    ='Soil_Data_From_Surgo.csv'
    lon         = -90
    lat         = 42
    [mukey,musym,areasymbol]=MUextract(lat,lon)
    dictionary  =SolDataExtractor(mukey)
    DatatoWrite =pd.DataFrame(dictionary)
    Data        =DatatoWrite[DatatoWrite['comppct_r']==max(DatatoWrite['comppct_r'])]
    Data.to_csv(filename,header=True,index=False)

if __name__ == "__main__":
    main()

