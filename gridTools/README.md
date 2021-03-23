# Grids

For showing a grid not in its native projection, you have to
plot every line between grid box nodes to form the vertices.

For a grid to be shown in the native projection, you can simply
plot from grid point extents to get the bounding box.  You can
plot from outer grid edges to form the vertices.

## Arctic6

This grid is North Polar Stereo.
This grid has a central longitude of 160.0 West.
The true scale latitude is unknown.  Kate thinks it might be 90N?

## NEP7

This grid is Lambert Conformal Conic.
The LCC attributes are:
    Standard parallel latitudes: 40.0 and 60.0 North
    Central longitude: 91.0 West
    Central longitude: unknown

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

