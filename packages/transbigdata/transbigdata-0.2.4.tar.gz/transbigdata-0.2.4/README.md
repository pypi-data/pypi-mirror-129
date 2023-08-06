English [中文版](README-zh_CN.md)

# TransBigData

<img src="https://github.com/ni1o1/transbigdata/raw/main/docs/source/_static/logo-wordmark-dark.png" style="width:550px">

[![Documentation Status](https://readthedocs.org/projects/transbigdata/badge/?version=latest)](https://transbigdata.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/transbigdata.svg)](https://badge.fury.io/py/transbigdata) ![PyPI - Downloads](https://img.shields.io/pypi/dm/transbigdata) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ni1o1/transbigdata) [![bilibili](https://img.shields.io/badge/bilibili-%E5%90%8C%E6%B5%8E%E5%B0%8F%E6%97%AD%E5%AD%A6%E9%95%BF-green.svg)](https://space.bilibili.com/3051484)  


**Main Functions**

TransBigData is a Python package developed for transportation spatio-temporal big data processing and analysis. TransBigData provides fast and concise methods for processing common traffic spatio-temporal big data such as Taxi GPS data, bicycle sharing data and bus GPS data. It includes general methods such as rasterization, data quality analysis, data pre-processing, data set counting, trajectory analysis, GIS processing, map base map loading, coordinate and distance calculation, and data visualization.

**Technical Features**

* Provide a variety of processing methods for each stage of transportation spatio-temporal big data analysis.
* The code with TransBigData is clean, efficient, flexible, and easy to use, allowing complex data tasks to be achieved with concise code.


For more details please see the [documentation](https://transbigdata.readthedocs.io/en/latest/)


## Installation

Before installing TransBigData, make sure that you have installed the available geopandas package: https://geopandas.org/index.html
If you already have geopandas installed, run the following code directly from the command prompt to install it

    pip install -U transbigdata


## Usage

The following example shows how to use the TransBigData to extract Origin-Destination(OD) information of taxi trips from taxi GPS data:

    import transbigdata as tbd
    #Read the data    
    import pandas as pd
    data = pd.read_csv('TaxiData-Sample.csv',header = None) 
    data.columns = ['VehicleNum','time','slon','slat','OpenStatus','Speed'] 
    data

<img src="https://github.com/ni1o1/transbigdata/raw/main/docs/source/_static/WX20211021-192131@2x.png" style="height:300px">

Use the tbd.taxigps_to_od method and pass in the corresponding column name to extract the trip OD:

    #Extract OD information from GPS
    oddata = tbd.taxigps_to_od(data,col = ['VehicleNum','time','slon','slat','OpenStatus'])
    oddata

<img src="https://github.com/ni1o1/transbigdata/raw/main/docs/source/_static/WX20211021-190104@2x.png" style="height:300px">

Aggregate OD into grids:

    #Defining study area
    bounds = [113.6,22.4,114.8,22.9]
    #Input the bounds for the study area and generates the rasterization parameters
    params = tbd.grid_params(bounds = bounds,accuracy = 1500)
    #Rasterized OD and aggregate them into grids, this function will also generates a GeoDataFrame of the OD, which contains the counts of the aggregation.
    od_gdf = tbd.odagg_grid(oddata,params)
    od_gdf.plot(column = 'count')

<img src="https://github.com/ni1o1/transbigdata/raw/main/docs/source/_static/WX20211021-190524@2x.png" style="height:300px">

## Related Links

* Bilibili:  https://space.bilibili.com/3051484
* Data analytics course for beginner https://www.lifangshuju.com/#/introduce/166  
* Transportation Big Data analysis course： https://www.lifangshuju.com/#/introduce/154  
* Data Visualization course： https://www.lifangshuju.com/#/introduce/165  
* Github for this project： https://github.com/ni1o1/transbigdata/  
* Bug report： https://github.com/ni1o1/transbigdata/issues  

## Citation

And if you want to reference this GitHub repository, you can use the following bibtex.

```
@misc{transbigdata,
  author = {Qing Yu},
  title = {TransBigData},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/ni1o1/transbigdata}},
}
```
