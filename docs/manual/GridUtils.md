# GridUtils

Welcome to the user manual for the GridUtils python library.  This library
provides a one stop shop for grid preparation and manipulation software.
The [design](../development/Design.md) for this library is to keep it
simple and provide a variety of usage patterns.  Work is ongoing with a
laundry list of [TODO](../development/TODO.md) items.

# Under the hood

The library makes use of xarray for input and output (IO).  Several
open source libraries are used for manipulation of grid and
associated grid fields (boundary files and forcing fields).  The
primary storage format is netCDF.  The dask library is leveraged
where possible.  The library also leverages the geospatial
library pyproj where possible.

# Getting Started

This project assumes the user is familiar with using python as a
programming language.  To get started with using this library, the
first step is [instantiation](https://www.tutorialspoint.com/Explain-Inheritance-vs-Instantiation-for-Python-classes)
of the library's class with a python variable that will point to
the python object.  This also assumes the library has been installed
and is accessible.

```
from gridtools import GridUtils

grd = GridUtils()
```

The `grd` variable or object's functions and methods can not be
used to create or load the users grid and leverage the library's
tools for other available operations.

If working with more than one grid at one time, it is advised to
create or instantiate more than one object.  Use one object for
each grid in use in a single program.

The user manual and examples will refer to this `grd` object
frequently.

In the application form of this library, once all the notebook
cells have run, there is a `grd` object that can be accessed by
adding cells at the bottom of the notebook.  Manipulation of the
`grd` object outside the application can have unexpected
consequences.  The application can only work with one grid at
one time.

Additional details about the application not covered by the
internal application help menu can be found in the
[application](Application.md) portion of the user manual.

Additional details may be gleamed from the internal python
documentation using the built-in
[help()](https://docs.python.org/3/library/functions.html#help)
function.  After importing GridUtils or any library, the internal
help is displayed by using `help(GridUtils)` in a python script or
in a notebook cell.  This also works for individual methods or
functions.

## Feedback

The library provides feedback to the user and the developers by
providing messages back to the screen or logging them to files.
As the library is utilized, it will emit warnings or error as
needed.  If you want to increase or decrease the verbosity
of these messages, please see the [logging](Logging.md) portion
of the user manual.

# Terminology

**grid**: This refers to the entire grid.

**grid cell**: This refers to a grid cell within a grid.

## MOM6

**supergrid**: This refers a denser grid where
there are not only the grid verticies of the **grid cells** but additional
verticies through the center points of the **grid cells** in both the i
and j direction.  This grid is twice the nominal resolution of the model.

Grid orientation, with **no rotation**, is from the lower left to the upper
right.  The i direction increases from lower to upper portion of the grid.
The j direction incrases from left to right.

More grid specifics for MOM6 can be found at these locations:
  * [Cheat sheet for using a Moasic grid with MOM6 output](https://gist.github.com/adcroft/c1e207024fe1189b43dddc5f1fe7dd6c)
  * [Discrete Horizontal and Vertical Grids](https://mom6.readthedocs.io/en/dev-gfdl/api/generated/pages/Discrete_Grids.html)

# Parameters

The library acts on user provided grid and plot parameters.

The user must specify projection information for both the grid and plot
parameters if the grid is to be used on a geographic surface.  In most
cases, the grid and plot projections will be the same unless you wish
to see the grid in a different projection.

# Grid Creation

The library supports one mode of grid creation at present.  The user
must provide:
  * Size of the grid in the i(dy) and j(dx) direction in degrees or meters.
  * Grid center in degrees or meters.
  * Grid resolution in degrees or meters.

The number of grid cells depends on the total size of the grid
and selected grid resolution.  The library may automatically
adjust number of grid points in the i and j direction.  Automatic
adjustment can be disabled.

## Projections

The user may select from three available projections:
  * Mercator
  * Lambert Conformal Conic
  * Stereographic

Since `pyproj` is utilized by this library, the
default ellipsoids for [projections](https://proj.org/operations/projections/index.html)
is GRS80.  If `proj` is installed, use `proj -le` to produce a
list of available ellipoids.

# Defaults

This section shows all available grid and plot parameters.  Parameter
definitions are provided.

All the available parameters are shown for completeness.  Not all
parameters are needed to create a grid or request a plot.  It some
cases, it does not make sense to mix parameters.  Some parameters
are only available for specific grid types.

## Grid

Grid parameters may be changed through the `setGridParameters` function by
passing a python dictionary.  The order of the parameters does not matter.
The parameter names are case sensitive.

```
grd.setGridParameters({
	'centerUnits': 'degrees',
	'centerX': 0.0,
	'centerY': 0.0,
	'dx': 0.0,
	'dy': 0.0,
	'dxUnits': 'degrees',
	'dyUnits': 'degrees',
	'nx': 0,
	'ny': 0,
	'tilt': 0.0,
	'gridResolution': 0.0,
	'gridResolutionX': 0.0,
	'gridResolutionY': 0.0,
	'gridResolutionUnits': 'degrees',
	'gridResolutionXUnits': 'degrees',
	'gridResolutionYUnits': 'degrees',
	'projection': {
		'name': 'Mercator',
		'lat_0': 0.0,
		'lat_1': 0.0,
		'lat_2': 0.0,
		'lat_ts': 0.0,
		'lon_0': 0.0,
		'ellps': 'GRS80',
		'R': 6378137.0,
		'x_0': 0.0,
		'y_0': 0.0,
		'k_0': 1.0
	},
	'gridMode': 2,
	'ensureEvenJ': True
})
```

Parameter definitions:

Parameter | Definition | Type | Valid Values | Default
--------- | ---------- | ---- | ------------ | -------
centerUnits | units for center grid point | string | 'degrees', 'meters' | 'degrees'
centerX | grid center in j direction | float | +0.0 to +360.0 | n/a
centerY | grid center in i direction | float | -90.0 to +90.0 | n/a
dx | grid length in the j direction | float | **(1)** | n/a
dy | grid length in the i direction | float | **(1)** | n/a
dxUnits | grid length units | string | 'degrees', 'meters' | 'degrees'
dyUnits | grid length units | string | 'degrees', 'meters' | 'degrees'
nx | number of grid points in the j direction | integer | **(2)** | n/a
ny | number of grid points in the i direction | integer | **(2)** | n/a
tilt | degree to rotate the grid | float | 0.0 to 360.0 | 0.0 **(3)**
gridResolution | grid cell size in the i and j direction | float | **(4)** | n/a
gridResolutionX | grid cell size in the j direction | float | **(4)** | n/a
gridResolutionY | grid cell size in the i direction | float | **(4)** | n/a
gridResolutionUnits | grid cell size units in the i and j direction | string | 'degrees', 'meters' | 'degrees'
gridResolutionXUnits | grid cell size units in the j direction | string | 'degrees', 'meters' | 'degrees'
gridResolutionYUnits | grid cell size units in the i direction | string | 'degrees', 'meters' | 'degrees'

NOTES:
 * **(1)** This is a reasonable float number representing degrees or meters.
 * **(2)** This feature has not been implemented yet.
 * **(3)** This parameter only applies to the Lambert Conformal Conic projection.
 * **(4)** Specifying gridResolutionX and/or gridResolutionY will override the value
specified for gridResolution

MOM6 parameter definitions:

Parameter | Definition | Type | Valid Values | Default
--------- | ---------- | ---- | ------------ | -------
gridMode | grid generation mode | integer | **(1)** | 2
ensureEvenJ | ensure even number of grid points in the j direction | boolean | True, False | True

NOTES:
 * **(1)** Valid values are 1 and 2.  Grid mode one (1) generates only the specified grid with
grid cell distances given by the grid resolution.  Grid metrics will NOT be computed.  Grid
mode two (2) generates a standard MOM6 grid with supergrid.  Grid metrics will be computed.
 * `ensureEvenJ` flag allows the grid generator clip the grid if the number of points in
the j direction is uneven.

Projection definitions:

Parameter | Definition | Type | Valid Values | Default
--------- | ---------- | ---- | ------------ | -------
name | projection name | string | 'LambertConformalConic', 'Mercator', 'Stereographic' | n/a
lat\_0 | latitude of projection center | degrees | -90.0 to +90.0 | 0.0
lat\_1 | first standard parallel latitude | degrees | -90.0 to +90.0 | 0.0
lat\_2 | second standard parallel latitude | degrees | -90.0 to +90.0 | 0.0
lat\_ts | latitude of true scale | degrees | -90.0 to +90.0 | 0.0
lon\_0 | longitude of projection center | degrees | +0.0 to +360.0 | 0.0
ellps | ellipsoid | string | **(1)** | 'GRS80'
R | radius of the earth sphere | float | **(2)** | n/a
x\_0 | false easting | float | meters | 0.0
y\_0 | false northing | float | meters | 0.0
k\_0 | scale factor for natural origin or the ellipsoid | float | **(1)** | 1.0

## Plot

The projection definitions for plot parameters are
the same as the grid parameters and will not be 
repeated here.
