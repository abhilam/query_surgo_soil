# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:57:58 2017

@author: abhilam
"""

"""
###########################################################
#Author: Abhishes lamsal
#Purpose: Extract the mapunit, musymbol, and areasymbol of any given lattitude and longitude
#necessasry packages

import json
import requests

lon = -90
lat = 42
def MUextract(lat,lon):
    
    ##### Converting Lat long to mukey (Map unit key)
    f ="&lon="+ str(lon)+"&lat="+ str(lat)
    ## I use a API from UCDAVIS convert latlong to mukey
    the_url = "http://casoilresource.lawr.ucdavis.edu/soil_web/api/ssurgo.php?what=mapunit"+ f
    data=requests.get(the_url)
    datacontent=json.loads(data.content)[0]
    mukey=int(datacontent['mukey'])
    musym=datacontent['musym']
    areasymbol=datacontent['areasymbol']
    return [mukey,musym,areasymbol]

print MUextract(lat,lon)

###############################################
"""