# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 11:38:19 2017

"""
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

os.chdir('C:\\Users\\abhilam\\Desktop\\Abhi\\KMZ_Data\\')


def MUextract(lat,lon):
    
    ##### Converting Lat long to mukey (Map unit key)
    f             ="&lon="+ str(lon)+"&lat="+ str(lat)
    ## I use a API from UCDAVIS convert latlong to mukey
    the_url      = "http://casoilresource.lawr.ucdavis.edu/soil_web/api/ssurgo.php?what=mapunit"+ f
    data         =requests.get(the_url)
    datacontent  =json.loads(data.content)[0]
    mukey        =int(datacontent['mukey'])
    musym        =datacontent['musym']
    areasymbol   =datacontent['areasymbol']
    return [mukey,musym,areasymbol]


###############################################

# Queries to import data from SURGO
def SolDataExtractor(mukey):
    url="https://sdmdataaccess.nrcs.usda.gov/Tabular/SDMTabularService.asmx"
    #headers = {'content-type': 'application/soap+xml'}
    headers = {'content-type': 'text/xml'}
    body = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
            <RunQuery xmlns="http://SDMDataAccess.nrcs.usda.gov/Tabular/SDMTabularService.asmx">
            <Query>
            SELECT
            saversion, saverest, -- attributes from table "sacatalog"
            l.areasymbol, l.areaname, l.lkey, -- attributes from table "legend"
            musym, muname, museq, mu.mukey, -- attributes from table "mapunit"
            comppct_r, compname, slope_r, c.cokey, -- attributes from table "component"
            hzdept_r, hzdepb_r, ch.chkey,sandtotal_r,silttotal_r,claytotal_r,om_r,dbthirdbar_r,ksat_r,awc_r,caco3_r,cec7_r,ec_r,ph1to1h2o_r -- attributes from table "chorizon"
            FROM sacatalog sac
             INNER JOIN legend l ON l.areasymbol = sac.areasymbol
             INNER JOIN mapunit mu ON mu.lkey = l.lkey
             AND mu.mukey IN
             ('"""+str(mukey)+"""')
             LEFT OUTER JOIN component c ON c.mukey = mu.mukey
             LEFT OUTER JOIN chorizon ch ON ch.cokey = c.cokey 
             </Query>
             </RunQuery>
             </soap:Body>
             </soap:Envelope>"""         
    
    # extract the post request response
    response = requests.post(url,data = body,headers=headers)
    ab=response.content
    root=EM.fromstring(ab)

    """
    ab=root.findall(".//Table")[0]
    children=ab.getchildren
    children.txt  
    """
    abc={}
    i=0
    # Loop over all Table
    for table in root.findall('.//Table'):
        for child in table.getchildren():             # for each table get the children key e.g. soil attributes
            print child.tag,child.text                # for each children key get the value 
            if i==0:abc[child.tag]=[]
            abc[child.tag].append(child.text)
        i+=1
    return abc

def main():
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




