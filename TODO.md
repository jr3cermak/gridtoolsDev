# Planned work

A milestone for version 1.0 has yet to be established.

# TASKS

 - [ ] grid creation/editor
   - [ ] grid metrics
     - [X] Spherical solution is complete via ROMS to MOM6 converter
     - [ ] Mercator (might be 0? lined up along latitude lines)
     - [ ] Polar (might be the same as spherical?)
   - [X] make Lambert Conformal Grids; needs global testing
   - [ ] grid generation in other projections
 - [ ] grid mask editor (land, etc)
 - [ ] integration of bathymetric sources and apply to grids
       Niki: https://github.com/nikizadehgfdl/ocean_model_topog_generator
 - [ ] add nbserverproxy to conda software stacks
 - [ ] see if xgcm can be added to the xesmf software stack
 - [ ] xarray \_FillValue needs to be turned off somehow
 - [ ] place display(dashboard) as a separate notebook cell
 - [ ] on load of a grid
   - [ ] calculate R
   - [ ] calculate tilt
   - [ ] update any tool metadata that is appropriate for that grid

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
