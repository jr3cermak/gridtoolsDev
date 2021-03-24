# Grids

For showing a grid not in its native projection, you have to
plot every line between grid box nodes to form the vertices.

A simple bounding box, extent, may be used for a grid shown
in its native projection.  You can plot from outer grid edges
to form the vertices.  This also seems to hold true for tilted
grids in Lambert Conformal Conic.

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
The LCC attributes are:
    Standard parallel latitudes: 40.0 and 60.0 North
    Central longitude: 91.0 West
    Central latitude: unknown (seems ok for plotting)

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

