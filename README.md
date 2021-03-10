# gridtools

A generic set of grid manipulation tools for computer models.  These tools are
adapted from the ROMS ocean model and for specific use in the MOM6 ocean model.
One could hope it can be kept generic enough to support any model.

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
capture the result.  This was evidenced when trying to load an enviornment
surrounding geopandas.

```
$ conda env create -f gridtools/conda/gridToolsGeopandas.yml
$ conda activate gridToolsGeopandas
$ conda install -c conda-forge geopandas
$ conda install -c conda-forge jupyterlab
$ conda install -c conda-forge pip matplotlib ipympl cartopy
$ conda install -c conda-forge netcdf4
$ conda env export -n gridToolsGeopandas > gridtools/conda/gridToolsGeopandas_export.yml
```

## jupyterlab

A jupyterlab can be started for each conda enviroment, but do not attempt
to open the same notebook between two jupyterlab instances.  It will do it,
but will cause odd things to happen.

To enable multiple environments, use separate ports via (--port).

## gridTools

Collection of python code and python notebooks

Exploring various display/grid manipulation options at the moment:
 * ipyleaflet
 * cartopy/geopandas/bokeh

Exporing various data/grid manipulation and visualization options:
 * holoviz
 * pangeo
 * xgcm
 * xesmf

# pyroms

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
