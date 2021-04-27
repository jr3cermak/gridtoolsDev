# conda

This explains some things about how to utilize conda to
manage python environments.  To learn much more details about
conda, we suggest visiting the 
[conda documentation](https://docs.conda.io/projects/conda/en/latest/index.html) website.

A YAML specification file is to configurate a python environment.  We have prepared
a few specification files, please see the conda directory.

These instructions assume you have conda/miniconda installed.  If conda is not installed,
please consult this
[webpage](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

There is a generic YAML file that pulls together a development environment.  To
expidite the conda environment solver, a YAML\_export file is also provided for
quicker recovery of a generic environment.

Initialization:
```
$ conda env create -f conda/pyroms.yml
$ conda env export > conda/pyroms_export.yml
```

For a quicker recovery of a conda environment, use the exported YAML file:
```
$ conda env remove --name pyroms
$ conda env create conda/pyroms_export.yaml
```

NOTE: Initialization of holoviz from the generic YAML file took over an hour.
It only took a couple of minutes from the resolved export YAML file.

AND: Sometimes it is faster to slowly bootstrap an environment and then
capture the result.

Example:
```
$ conda env create -f gridtools/conda/gridTools.yml
$ conda activate gridTools
(gridTools) $ conda install -c conda-forge geopandas matplotlib ipympl cartopy netcdf4 conda
(gridTools) $ conda env export -n gridTools > gridtools/conda/gridTools_export.yml
```

You can capture the time it takes to run the creation of an enviroment as well
as set a timeout so you can tune the YAML file.  In this example, the timeout
is set to 5 minutes to allow resolution of the environment.
```
$ time timeout 5m conda env create -f gridtools/conda/gridTools.yml
```

## xesmfTools

This is the main enviroment for utilizing the grid generation libraries.

Some of the main libraries within this environment:
 * cartopy
 * xarray
 * xesmf

# Environments

Current operational environment for the grid toolset: ***xesmfTools***

## Initialization

Initialization times:
 * bokeh: 9m 17s
 * gridTools: 11m 47s
 * legacyTools: 4m 53s
 * pangeo: 10m 41s
 * pyroms: 1m 43s
 * xesmfTools: 5m 5s(!)

(!) Requires post installation step to solve environment

## gridTools

After installing the initial environment, two jupyter lab extensions may need
to be installed before you can use interactive bokeh elements.  You can check
to see if extensions are installed first and install extensions as needed.

```
$ conda env create -f gridtools/conda/gridTools.yml
$ conda activate gridTools
(gridTools) $ jupyter labextension list
(gridTools) $ jupyter labextension install @jupyter-widgets/jupyterlab-manager
(gridTools) $ jupyter labextension install @bokeh/jupyter_bokeh
```

## legacyTools

NOTE: This is a very limited environment with netcdf4 and matplotlib's basemap
to review former functionality of older libraries and software.

This environment supported investigation into the following libraries:
  * [leaflet](../development/python/libraries/leaflet.md)
  * [pyroms](../development/python/libraries/pyroms.md)

