<img src="https://visioterra.fr/telechargement/P317_DEMIX/logos/logo%202-2_white_demix_background.png" style="display: block;  margin-left: auto;  margin-right: auto" height="200px"></img>
<h1> DEMIX library </h1> 

The DEMIX Library that allow you to get scores for specific DEMIX tiles and DEM
You also can download DEMIX Tile associated DEM Layers like SourceMask, Heights, ...

<h2> Table of contents: </h2>

0. <a href="#Installation">Installation</a><br/>
1. <a href="#demix_lib_functions"> DEMIX lib functions</a><br/>
    1.1 <a href="#Getting-Score">Getting Scores</a><br/>
    1.2 <a href="#Getting-Geotiffs">Getting DEM</a><br/>
2. <a href="#dem_and_criterions">Available DEMs and criterions</a><br/>
    2.1 <a href="#Dem">Dem list</a><br/>
    2.2 <a href="#Criterion">Criterion list</a><br/>
3. <a href="#utility">Utility functions</a><br/>
4. <a href="#Usage_example">Usage example</a><br/>

<h2 id='Installation'> Installation</h2>
To install the DEMIX library on your python environment :

```
pip install demix_lib
```



<div id='demix_lib_functions'></div>
<h1>DEMIX lib functions</h1>
This section is a step-by-step guide on how to use the DEMIX lib functions. By getting through this guide, you'll learn how to:<br/>
*   Get a DEMIX tile id from a given longitude and latitude<br/>
*   Apply a criterion to a DEM, over a given DEMIX tile<br/>
*   Retrieve a raster of DEM layer over a DEMIX tile

<h2>Getting DEMIX Tile</h2>
The DEMIX api enables you to get a DEMIX tile id from a given longitude and latitude.

```Python
import demix_lib as dl
lon = 14.44799
lat = 35.81923
print(dl.get_demix_tile_info(lon, lat))
print(dl.get_demix_tile_name(lon, lat))
```

<h2 id='#Getting-Score'>Getting Scores</h2>
First thing first, you can use the demix api to get directly stats from the desired DEMIX Tile and Criterion
<br/>
In order to get scores to specific dem and tile, you need to choose a criterion.
The criterion list is available <a href="#Criterion">here</a>. List of supported dems is also visible <a href="#Dem">here</a>.


```Python
import demix_lib as dl

#getting the list of implemented criterions
criterions = dl.get_criterion_list()
#getting the list of supported dems
dems = dl.get_supported_dem_list()

#defining the wanted DEMIX Tile name 
demix_tile_name = "N35YE014F"

#getting the score of each dem, for the criterion 
for dem in  dems:
    for criterion in criterions:
        print(dl.get_score(demix_tile_name=demix_tile_name, dem=dem, criterion=criterion))
```

<div></div>
<H2 id='Getting-Geotiffs'>Getting DEM</H2>
To go further :
You can always use your own criterions by downloading the wanted layer on your DEMIX tile and apply custom code to it.
<br/>To download a DEM layer for a specific DEMIX Tile :

```Python
import demix_lib as dl
import matplotlib as plt #we use matplotlib to visualise the downloaded layer
from matplotlib import cm #we use cm to make a legend/colormap
from matplotlib.lines import Line2D #to add colored line in the legend

#defining wanted tile
demix_tile_name = "N35YE014F"
#asking for the SourceMask layer for the CopDEM_GLO-30 dem and the tile N64ZW019C
response = dl.download_layer(demix_tile_name=demix_tile_name,dem="CopDEM_GLO-30",layer="SourceMask")

#creating legend for the plot
legend_handle = list(map(int, response['values'].keys()))
legend_label = list(response['values'].values())
#defining the colormap for the layer (the layer has 6 values)
color_map = cm.get_cmap('rainbow',6)
#we use plt to look at the data
plt.imshow(response["data"], interpolation='none', cmap=color_map, vmin=0, vmax=6)
#creating legend values using the color map and the values stored
custom_handles = []
for value in legend_handle:
    custom_handles.append(Line2D([0], [0], color=color_map(value), lw=4))
plt.legend( custom_handles,legend_label)
#show the layer with custom legend and color map
plt.show()
```

<H2 id='Getting-Geotiffs'>Utility functions</H2>
The DEMIX lib give you some utility functions that allow you to get or print informations about currently implemented criterions, available DEMs, layers...

```python
import demix_lib as dl

#get or show the layers that you can ask in a download_layer function
layer_list = dl.get_layer_list()
dl.print_layer_list()
#get or show the full dem list
dem_list = dl.get_dem_list()
dl.print_dem_list()
#get or show the supported dem list
supported_dem_list = dl.get_supported_dem_list()
dl.print_supported_dem_list()
#get or show the implemented criterion list
criterion_list = dl.get_criterion_list()
dl.print_criterion_list()


```


<h2 id='dem_and_criterions'>Available DEMs and criterions</h2>
<h3 id='Dem'>DEMs list</h3>

| DEM name | supported |
| :-------------: | :-------------: |
| ALOS World 3D | <span style="color:red">no</span> |
| ASTER GDEM | <span style="color:red">no</span> |
| CopDEM GLO-30 | <span style="color:green">yes</span> |
| NASADEM | <span style="color:red">no</span> |
| SRTMGL1 | <span style="color:green">yes</span> |

<h3 id='Criterion'>Criterion list</h3>


| Criterion name | Criterion id | version | Date | Category | Target |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Product fractional cover | A01 |  0.1 | 20211103 | A-completeness | <span style="color:green">All</span> |
| Valid data fraction | A02 |  0.1 | 20211103 | A-completeness | <span style="color:green">All</span> |
| Primary data | A03 |  0.1 | 20211103 | A-completeness | <span style="color:green">All</span> |
| Valid land fraction | A04 |  0.1 | 20211103 | A-completeness | <span style="color:green">All</span> |
| Primary land fraction | A05 |  0.1 | 20211103 | A-completeness | <span style="color:green">All</span> |


<h3 id='Layers'>Layer list</h3>

| Layer name |
| :-------------: |
| Height |
| validMask | 
| SourceMask |
| landWaterMask |