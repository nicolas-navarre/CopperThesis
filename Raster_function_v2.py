#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:03:06 2019

@author: nicolasnavarre
"""

import rasterio
import rasterio.plot
import pyproj

def k_factor_pull(lat, lng):
    with rasterio.open('Kst_correct.tif') as src:
        # Use pyproj to convert point coordinates
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        #print(lng, lat)
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)

        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')

        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)

        value = src.read()
        try:
            k_factor = value[0][row][col]
            if k_factor > 0:
                print('K-factor (t ha h/MJ ha mm) =', round(k_factor,3))
            else:
                print('Erosion data not available in your region.')
                k_factor = 'No DATA'
        except IndexError:
            print('Erosion data not available in your region.')
            k_factor = 'NO DATA'

    return k_factor, utm,  value

def ls_factor_pull(lat, lng):
    with rasterio.open('EU_LS_Mosaic_100m.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            ls_factor = value[0][row][col]
            if ls_factor > 0:
                print('LS-factor (dimensionless) =',round(ls_factor,3))
            else:
                print('No LS-factor data at your location.')
                ls_factor = 'NO DATA'
        except IndexError:
            print('Erosion data not available in your region.')
            ls_factor = 'NO DATA'

    return ls_factor


def p_factor_pull(lat, lng):
    with rasterio.open('EU_PFactor_V2.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            p_factor = value[0][row][col]
            if p_factor > 0:
                print('P-factor (dimensionless) =',round(p_factor,3))
            else:
                print('No recorded practices in your region. P-factor assumed to be = 1.')
                p_factor = 1
        except IndexError:
            print('Erosion data not available in your region.')
            p_factor = 'NO DATA'

    return p_factor


def Cu_concentration_pull(lat, lng):
    with rasterio.open('copper_map_fill.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            cu_conc = value[0][row][col]
            if cu_conc > 0:
                print('Cu concentration (mgCu/kgSoil)=',round(cu_conc,2))
            else:
                print('No recorded copper concentration at your location.')
                cu_conc = 'NO DATA'
        except IndexError:
            print('Copper concentration data not available in your region.')
            cu_conc = 'NO DATA'

    return cu_conc

def Bulk_density_pull(lat, lng):
    with rasterio.open('Bulk_density.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            bulk_p = value[0][row][col]
            if bulk_p > 0:
                print('Soil bulk density (T/m3)=',round(bulk_p,2))
            else:
                print('No recorded soil bulk density values in your region.')
                bulk_p = 'NO DATA'
        except IndexError:
            print('Soil bulk density data not available in your region.')
            bulk_p = 'NO DATA'

    return bulk_p

def Soil_pH_pull(lat, lng):
    with rasterio.open('pH_Europe.tif') as src:
        #utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            soil_pH = value[0][row][col]
            if soil_pH > 0:
                print('Soil pH =',round(soil_pH,2))
            else:
                print('No recorded soil pH values in your region.')
                soil_pH = 'NO DATA'
        except IndexError:
            print('Soil pH data not available in your region.')
            soil_pH = 'NO DATA'

    return soil_pH

def Soil_OC_pull(lat, lng):
    with rasterio.open('ocCont_snap.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            soil_OC = value[0][row][col]
            if soil_OC > 0:
                soil_OM = soil_OC/10 * 1.724
                print('Soil OM =',round(soil_OM,2))
            else:
                print('No recorded soil OC values in your region.')
                soil_OM = 'NO DATA'
        except IndexError:
            print('Soil OC data not available in your region.')
            soil_OM = 'NO DATA'

    return soil_OM

def Soil_sand_pull(lat, lng):
    with rasterio.open('sand1.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            soil_sand = value[0][row][col]
            if soil_sand > 0:
                print('Soil Sand Content =',round(soil_sand,2))
            else:
                print('No recorded soil OC values in your region.')
                soil_sand = 'NO DATA'
        except IndexError:
            print('Soil OC data not available in your region.')
            soil_sand = 'NO DATA'

    return soil_sand

def Soil_clay_pull(lat, lng):
    with rasterio.open('clay.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            soil_clay = value[0][row][col]
            if soil_clay > 0:
                print('Soil Clay Content =',round(soil_clay,2))
            else:
                print('No recorded soil clay values in your region.')
                soil_clay = 'NO DATA'
        except IndexError:
            print('Soil OC data not available in your region.')
            soil_clay = 'NO DATA'

    return soil_clay

def Soil_AWC_pull(lat, lng):
    with rasterio.open('AWC.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            soil_AWC = value[0][row][col]
            if soil_AWC > 0:
                print('Soil AWC Content =',round(soil_AWC,2))
            else:
                print('No recorded AWC values in your region.')
                soil_AWC = 'NO DATA'
        except IndexError:
            print('Soil OC data not available in your region.')
            soil_AWC = 'NO DATA'

    return soil_AWC

def Soil_hydro_pull(lat, lng):
    with rasterio.open('ths_fao_octop.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            soil_hydro = value[0][row][col]
            if soil_hydro > 0:
                print('Soil hydraulic cond. cm/day =',round(soil_hydro,2))
            else:
                print('No recorded AWC values in your region.')
                soil_hydro = 'NO DATA'
        except IndexError:
            print('Soil OC data not available in your region.')
            soil_hydro = 'NO DATA'

    return soil_hydro

def Soil_wcfc_pull(lat, lng):
    with rasterio.open('fc_fao.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            soil_wcfc = value[0][row][col]
            if soil_wcfc > 0:
                print('Soil water content @ field cap. cm3/cm3 =',round(soil_wcfc,2))
            else:
                print('No recorded AWC values in your region.')
                soil_wcfc = 'NO DATA'
        except IndexError:
            print('Soil OC data not available in your region.')
            soil_wcfc = 'NO DATA'

    return soil_wcfc

def Soil_wcwp_pull(lat, lng):
    with rasterio.open('wp_fao.tif') as src:
        utm = pyproj.Proj(src.crs) # Pass CRS of image from rasterio
        lonlat = pyproj.Proj(init='epsg:4326')
        lon, lat = (lng, lat)
        #temp = pyproj.Proj(init='epsg:3857')
        #print(lonlat)
        utm = pyproj.Proj(init='epsg:3035')
        east,north = pyproj.transform(lonlat, utm, lon, lat)
        #print(east,north)
        #east,north = pyproj.transform(temp, utm, east, north)
        #print('K-factor\n-------')
        #print(f'lon,lat=\t\t({lon:.2f},{lat:.2f})')
        #print(f'easting,northing=\t({east:g},{north:g})')
        
        row, col = src.index(east, north) # spatial --> image coordinates
        #print(f'row,col=\t\t({row},{col})')
        #print(row,col)
        
        value = src.read()
        try:
            soil_wcwp = value[0][row][col]
            if soil_wcwp > 0:
                print('Soil water content @  wil point. cm3/cm3 =',round(soil_wcwp,2))
            else:
                print('No recorded AWC values in your region.')
                soil_wcwp = 'NO DATA'
        except IndexError:
            print('Soil OC data not available in your region.')
            soil_wcwp = 'NO DATA'

    return soil_wcwp