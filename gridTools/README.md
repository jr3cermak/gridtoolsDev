# Grids

For showing a grid not in its native projection, you have to
plot every line between grid box nodes to form the vertices.

A simple bounding box, extent, may be used for a grid shown
in its native projection.  You can plot from outer grid edges
to form the vertices.  This also seems to hold true for tilted
grids in Lambert Conformal Conic.

# Grid notes

```
# Both ROMS and MOM6 horizontal grids use an Arakawa C-grid, with four
# types of points:
#   rho: the centers of the cells
#   psi: the corners of the cells, located diagonally between the
#        'rho' points
#   u:   the u-velocity points, located between 'rho' points in the
#        east/west direction
#   v:   the v-velocity points, located between 'rho' points in the
#        north/south direction

# The main differences between the two grids are:
#  * the outermost points of the ROMS grid are the 'rho' points, while
#    the outermost points of the MOM6 grid are the 'psi' points (both
#    with interspersed 'u' and 'v' points); and
#  * the MOM6 grid interleaves all four types of points into a single
#    "supergrid", while ROMS stores them as separate grids.

# The ROMS grid looks like this, with an extra layer of 'rho' points
# around the outside:
# (see https://www.myroms.org/wiki/Numerical_Solution_Technique)
#
#       p - p - p - p - p
#    3  | + | + | + | + |     p = rho (center) points
#       p - p - p - p - p     + = psi (corner) points
#    2  | + | + | + | + |     - = u points
#       p - p - p - p - p     | = v points
#    1  | + | + | + | + |
#       p - p - p - p - p
#
#         1   2   3   4

# The MOM6 grid has 'psi' points on the outside, not 'rho':
#
#    3    + | + | + | +       p = rho (center) points
#         - p - p - p -       + = psi (corner) points
#    2    + | + | + | +       - = u points
#         - p - p - p -       | = v points
#    1    + | + | + | +
#
#         1   2   3   4
```

## MOM6 notes

  nx, ny : grid centers
  nxp, nxp : grid verticies
    
## ROMS

  Has an extra grid box around the regular grid.

# Grid examples

## Niki's example

The code creates a grid in spherical coordinates.  It appears the final
grid is in Lambert Conformal Conic.  The code allows a tilt to be provided
as input.

## Arctic6

This grid is North Polar Stereo.
This grid has a central longitude of 160.0 West.
The true scale latitude is unknown.  Kate thinks it might be 90N?
Having true scale latitude unset for plotting seems to work.

## NEP7

This grid is Lambert Conformal Conic.
Grid resolution is 10km (10000 meters)
The LCC attributes are:
    Standard parallel latitudes: 40.0 and 60.0 North (lat_1, lat_2)
    Central longitude: -91.0 West (lon_0)
    Central latitude: unknown (seems ok for plotting)
    Corner points: (-130,0N) (-220,70N)

# Other grids

## IBCAO bathymetry

This grid is North Polar Stereo.
The true scale latitude is 75 North.

# Useful Web Mapping Services

https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/
https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/mapserv?

Layers:
 * GEBCO_Latest - shaded relief imagery
 * GEBCO_Latest_2 - colour-shaded for elevation imagery
 * GEBCO_Lastest_TID - imagery based on the TID grid with grid cells based on interpolation transparent

# Links

Mathmatica notebook library: 
  http://mathworld.wolfram.com

Article about matplotlib's extents only work if limits are set:
https://stackoverflow.com/questions/6999621/how-to-use-extent-in-matplotlib-pyplot-imshow

# Documentation/Sphinx/Python

https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html
https://devguide.python.org/documenting/

of course there are differences of opinion!

https://docs.python-guide.org/writing/documentation/

# Panel application notes

Any control without a callback function feature like "on\_click" for the button can gain
a callback function using the param.watch method.  For example, a Checkbox.  Suppose, you
would like to have an event when the checkbox is toggled.  

Here is the code to create the checkbox control:
```
logEnableControl = pn.widgets.Checkbox(name="Enable file logging")
```

To setup a watch for a change in the "value" property, use:
```
logEnableControl.param.watch(logEnableCallback, 'value')
```

The callback function should trap the emitted event:
```
def logEnableCallback(event):
    print(event)
```

Which will result in something like:
```text
Event(what='value', name='value', obj=Checkbox(name='Enable file logging', value=True), cls=Checkbox(name='Enable file logging', value=True), old=False, new=True, type='changed')
```
