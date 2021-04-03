# Planned work

A milestone for version 1.0 has yet to be established.

# TASKS

 - [ ] grid creation/editor
   - [ ] grid metrics
     - [X] Spherical solution is complete via Niki's ROMS to MOM6 converter
     - [ ] Mercator (angle_dx might be 0 as it is lined up along latitude lines; except for tilt?)
     - [ ] Polar (might be the same as spherical?)
   - [ ] make Lambert Conformal Conic Grids; needs testing
     - [ ] LCC cannot take custom lat_1 and lat_2; it generates lat_1 and lat_2 based on grid inputs
     - [X] Update new lat_1 and lat_2 for application once makeGrid() is run
   - [ ] grid generation in other projections
   - [ ] saveGrid() convert lon [+0,+360] to [-180,+180]
 - [ ] grid mask editor (land, etc)
 - [ ] integration of bathymetric sources and apply to grids
       Niki: https://github.com/nikizadehgfdl/ocean_model_topog_generator
 - [X] add nbserverproxy/xgcm to conda software stacks; copied to binder environment.yml
 - [ ] turn numpypi into a loadable package via pip
 - [ ] add datashader and numpypi from github sources
 - [X] xarray \_FillValue needs to be turned off somehow
 - [X] place display(dashboard) as a separate notebook cell
 - [ ] on load of a grid
   - [ ] calculate R
   - [ ] calculate tilt (may not be possible)
   - [ ] update any tool metadata that is appropriate for that grid
 - [ ] Create an application method within the GridTools() class; GridTools().app()

# TODO

 - [ ] Further consolidate matplotlib plotting code
   - [ ] Refactor plotting code.  It is mostly the same except for setting the projection.
 - [ ] Do we have to declare everything in __init__ first or can be push all that to respective reset/clear functions?
 - [ ] refactor refineS and refineR options as Niki had them defined
 - [ ] Pass back an error graphic instead of None for figures that do not render
 - [ ] Add a formal logging/message mechanism.
   - [X] Allow display of important messages and warnings in panel application
   - [ ] Move all this to options.  Interact with message buffer.
   - [ ] Maybe warnings are better? Try some out.
   - [ ] Create a message buffer/system for information 
 - [ ] For now, the gridParameters are always in reference to a center point in a grid
   in the future, one may fix a side or point of the grid and grow out from that point
   instead of the center.
 - [ ] makeGrid assumes degrees at this point.
 - [ ] Use Alistairs numpypi package
 - [ ] Add testing harness using pytest.

# WISH

 - [ ] tripolar grids
 - [ ] Bring in code that converts ROMS grids to MOM6 grids
   - [ ] Allow conversion of MOM6 grids to ROMS grids
 - [ ] grid reading and plot parameter defaults should be dynamic with grid type declaration and potentially
       split out into separate library modules? lib/gridTools/grids/{MOM6,ROMS,WRF}
 - [ ] Place additional projection metadata into MOM6 grid files
   - [X] Added proj string to netCDF file
   - [ ] Tri polar grid description
