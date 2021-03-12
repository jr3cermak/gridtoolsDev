# gridtools

A generic set of grid manipulation tools for computer models.  These tools are
adapted from the ROMS ocean model and for specific use in the MOM6 ocean model.
One could hope it can be kept generic enough to support any model.

# grid generation

I am currently following an example by Niki Zadeh.  The hope is to make this 
interactive within Jupyter lab.  It may be worthy to continue to operate in several modes.

https://github.com/nikizadehgfdl/grid_generation/blob/dev/jupynotebooks/regional_grid_spherical.ipynb

Currently targeting a mix of holoviz and bokeh modules.

## Design elements

### Requirements

These are MUST HAVE elements.

The ocean grids are conformal.  This means the angles between the
horizontal and vertical intersections are 90 degress.

Long term view is to be able to create nested grids within an existing
global grid.

Must work with these conformal projections:
 * Mercator
 * Lambert Conformal Conic
 * Polar Stereographic

Grid operation:
 * Set, increase, decrease number of grid points (x, y)
 * Set, increase, decrease cell size (dx, dy)
 * Set or unset the requirement that dx = dy
 * Zoom in/out
 * Draw, adjust or delete the drawn grid

### Features

This is a list of elements that would be nice to have.

Grid operation:
 * Adjust the drawn box with a fixed boundary or point
 * Grid rotation

## Operational modes

Desired operational modes
 * Command line
 * Command line widget mode (ipython --pylab mode)
 * jupyter notebook
 * jupyter lab

# Directories

## conda

YAML specification files for different python environments.

This assumes you have conda/miniconda installed.

There is a generic YAML file that pulls together a development environment. 
To expidite the conda environment solver, a YAML_export file is also provided for
quicker recovery of a generic environment.

Initialization:
```
$ conda env create conda/pyroms.yml
$ conda env export > conda/pyroms_export.yml
```

For a quicker recovery of a conda environment, use the exported YAML file:
```
$ conda env remove --name pyroms --all
$ conda env create conda/pyroms_export.yaml
```

NOTE: Initialization of holoviz from the generic YAML file took over an hour.
It only took a couple of minutes from the resolved export YAML file.

AND: Sometimes it is faster to slowly bootstrap an environment and then
capture the result.

Example:
```
$ conda env create -f gridtools/conda/gridToolsGeopandas.yml
$ conda activate gridToolsGeopandas
(gridToolsGeopandas) $ conda install -c conda-forge geopandas matplotlib ipympl cartopy netcdf4 conda
(gridToolsGeopandas) $ conda env export -n gridToolsGeopandas > gridtools/conda/gridToolsGeopandas_export.yml
```

You can capture the time it takes to run the creation of an enviroment as well
as set a timeout so you can tune the YAML file.  In this example, the timeout
is set to 5 minutes to allow resolution of the environment.
```
$ time timeout 5m conda env create -f gridtools/conda/gridToolsGeopandas.yml
```

## gridTools

Collection of python code and python notebooks

Exploring various display/grid manipulation options at the moment:
 * cartopy/geopandas/bokeh
 * ipyleaflet

Exporing various data/grid manipulation and visualization options:
 * holoviz
 * pangeo
 * xgcm
 * xesmf

# Environments

## gridToolsGeopandas

After installing the initial environment, two jupyter lab extensions need to be installed
before you can use interactive bokeh elements.

```
$ conda env create -f gridtools/conda/gridToolsGeopandas.yml
$ conda activate gridToolsGeopandas
(gridToolsGeopandas) $ jupyter labextension install @jupyter-widgets/jupyterlab-manager
(gridToolsGeopandas) $ jupyter labextension install @bokeh/jupyter_bokeh
```

## leaflet

If panning of maps fails or freezes, it usually requires a full reload of the
entire web page and the contents of JupyterLab to restore.

## pyroms

NOTE: This is a very limited environment with netcdf4 and matplotlib's basemap
to review former functionality.  This should be migrated ASAP to utilize modern
libraries.

```
# The current path is your SRC directory
$ git clone https://github.com/ESMG/pyroms.git
# The cloned directory is ${SRC}/pyroms
```

Install the pyroms conda environment. This installs the
appropriate fortran compiler for netcdf.

If you need scrip.so:
```
$ cd ${SRC}/pyroms/pyroms/external/scrip/source
# edit makefile
# change PREFIX = /usr/local
# to     PREFIX ?= /usr/local
$ export PREFIX=$CONDA_PREFIX
$ make DEVELOP=1
$ cp scrip.cpython-38-x86_64-linux-gnu.so ${SRC}/pyroms/pyroms/pyroms/
```

Using pyroms:
```
# define the location of gridid.txt
# edit gridid.txt to point to Arctic6 nc file
$ export PYROMS_GRIDID_FILE=/home/cermak/gridGen/configs/Arctic6/roms/gridid.txt
```

For now the only known working way to run editmask.py is via:
```
$ ipython --pylab
```

Cut and paste line by line into the interactive command above.  The last line in
editmask.py saves any edits made to the grid.

However, this should also work in jupyterlab via ipympl which is untested at the
moment.

# jupyterlab

I currently run a Oracle VirtualBox on a MacOS and have the network setting for 
Adapter 1 set as bridged over the wifi interface (en0).  Doing so, I get a DHCP
address for my local network at the same level as the MacOS computer.  This allows
me to use that IP for sharing the jupyter and bokah servers from the VM to a local
browser on the MacOS.   In this documentation, I assume the VM is on the address
192.168.131.54.

Launching a jupyterlab session, I prefer not to have it try and start a browser
from the VM.  The default port is 8888.
```
$ conda activate <env>
(env) $ jupyter lab --ip=192.168.131.54 --no-browser
```

A jupyterlab can be started for each conda enviroment, but do not attempt
to open the same notebook between two jupyterlab instances.  It will do it,
but will cause odd things to happen.

To enable multiple environments, use separate ports via (--port).
```
(env) $ jupyter lab --ip=192.168.131.34 --port=8889 --no-browser
```

To test bokeh to make sure it can be embedded in a jupyter lab notebook with
working interactive widgets, use this example script:
https://github.com/bokeh/bokeh/blob/2.3.0/examples/howto/server_embed/notebook_embed.ipynb

Using the above launching of jupyter lab, the last line of the notebook should be:
```
show(bkapp, notebook_url="http://192.168.131.54:8888")
```

My example is stored in:
gridTools/bokeh/bokehJupyterStandaloneTest.ipynb

## shortcuts

You can install the shortcuts within JupyterLab web interface through Settings, Advanced
Setting Editor and Keyboard Shortcuts and edit the "User Preferences" pane.  Or copy
"shortcuts.jupyterlab-settings" to:

${HOME}/.jupyter/lab/user-settings/@jupyterlab/shortcuts-extension/shortcuts.jupyterlab-settings

The current shortcuts add two keyboard shortcuts to the notebook editor:
 * Ctrl Shift ArrowUp: move cell up
 * Ctrl Shift ArrowDown: move cell down

You must not be editing the cell. The cell to move must be selected just to the left and is
denoted by a vertical bar highlighting the cell.
