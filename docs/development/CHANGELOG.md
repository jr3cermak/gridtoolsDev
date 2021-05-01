# Change Log

# 2021-05-01

 - Move generic API demonstrations into mkGridsExample2.py so it
   does not detract from specific grid generation demonstrations
   in mkGridsIterative.ipynb.
 - API CHANGES (incomplete)
   - Enforce grid center parameters: centerX, centerY, centerUnits.
 - mkGridsInterative.ipynb (incomplete)
   - Add Niki's example of a Stereographic grid
   - Add Niki's example of a rotated Mercator grid
 - Added more of Niki's functions for Mercator grid generation
 - NOTE: Grid generation techniques sometimes require projection
   information and sometimes grid generation techniques change
   projection information.  All details should be specifically
   documented.

# 2021-04-30

 - API CHANGES
   - gridResolution is now units based instead of scale based as Niki defined it in his notebook example.
 - gridutils
   - Enforce degrees as units for Mercator and Lambert Conformal Conic.
   - TODO: Niki performs some clipping of points along the j direction.  This should be an expanded feature
     to warn the user about grids with odd number of points in the i and j direction and offer an expansion
     or clipping method.  For supercomputing, it is easier to decompose a grid with even amounts of
     points.
   - Plotting: follow proj convention, when lat_ts is missing, attempt to use lat_0.
   - Plottind defaults: follow proj defaults.
   - drop "+units" from Mercator proj string
   - add lat_ts to Stereographic proj string if available
   - fix proj string bug for Lambert Conformal Conic
   - Allow users to set the verbose Level by name instead of by number
   - makeGrid() refactoring: use a flag to track when a new grid is created and then compute
     grid metrics after attempting to establish a proj string.  Creating a proj string too
     early did not work for the delayed information from the Lambert Conformal Conic grid.  Now
     we compute the proj string at the latest possible moment.  This would break the Spherical
     grid generator for units in meters.  This routine will have to construct the proj string early.
   - Build out of Spherical grid generator begins (not complete)

# 2021-04-29

 - Unify user manual.  The user manual will hold the bulk of the operational details.  Application details
   will be a small subset enough to explain the operational details of the graphical user interface.
 - Merge NorthPolarStero and SouthPolarStereo to Sterographic in which grid generation will
   need to pay attention to lat_0 defined for the projection.
 - Update application to merge North and South polar stereographic to Stereographic.
 - TODO: grab github revision used by each specific mybinder.org instance
 - User can specify ellipsoid (ellps) and earth radius (R) through projection options to grid and plot.
 - Do not forecast milestones past the next logical one; put other major milestones into a generic X milestone.
 - We assume the user is familiar with the python programming language.  We will point the user to helpful
   materials when appropriate.
 - API CHANGES
   - Implementation requires vetting application and examples for proper operation
   - Change user specification of grid center to "centerX" and "centerY" and specify those units in "centerUnits".
 - BUG: Updating grid or plot parameter nested arguments will get clobbered.  Queued to be fixed later.

# 2021-04-28

 - Raphael pointed us code he wrote that allows conversion from XY to LATLON over a 2D field.  It was
   exactly what we needed to get the IBCAO grid working in the polar projection.
 - Unify MOM6/proj defaults for grid generation
   - Default radius is 6.378137e6
   - Default ellipse is GRS80
 - Add warnings to various areas where we create the projection string
 - Add warnings to determiniation of the radius of the earth to use
 - Add three examples on how to create the IBCAO grid.  One example shows how
   things change when a slightly different radius is specified for WGS84.
 - Move some milestones around with polar grids now possibly working
 - Keep milestones under 1.0 for now
 - Add datetime and pyproj to gridutils imports
 - Return a version number for gridutils library
 - Better metadata for xarray/netCDF structures
 - Determine earth radius based on projection string on the fly
 - Move construction of proj string into a function so it will work for grid and
   plot projections as needed
 - TODO: improve documentation for grid and plot parameters and finish implementation work
   for all projections.  For now, keep the grid construction simplified.
 - Added a plotting demo for illustrating unstructured grid interpolation and differences
   between using grid edges and grid center points for plotting.

# 2021-04-26

 - Avoid use of xesmf 0.5.2
   - split xesmfTools environment and move xgcm into its own environment
 - Add xgcmTools environment
 - Remapping an ice field using xesmf regridder
 - Begin rework field flood algorythm that pyroms utilizes
 - Added more bookmarks and sorted them
 - Added xesmf to pangeo environment
 - app.py; gridtools.py updates
   - Add appropriate spacing between items
   - If tilt is zero, remove it from any message or title
   - Split refine into two arguments
   - Update message if regular lat lon grid is being built on the equator or not
 - Move plotBathyArctic6.py into pyroms directory

# 2021-04-22

 - The supergrid plotting would fail if grid type was two(2) and resolution was 0.5.  When
   multiplied together, it results in 1.0 which confused the current system.
 - Add simple mercator grid generation method
 - Add a couple of bathy examples to debug a masking issue.  We can use xarray to display a
   GEBCO 2020 figure and a ROMS figure with bathymetry.
 - Add xmap examples that almost work
 - Fix some spacing in some gridutils functions
 - Update metadata for NEP7 grid in README
 - Disable mercator tilt
 - Separate refine inputs to grid functions that use gridResolution and gridMode
 - Update some messaging

# 2021-04-10

 - Shore up messaging and debugging code in GridUtils().  A lot of missing level= in 2nd arguments
   calls to printMsg and debugMsg.
 - Add a TODO to refactor messaging and debugging into its own package/module.
 - Add an example on how to work with logging levels and debug levels.
 - Add showPlotParameters function.
 - Add more explanation to example1.
 - Testing NSIDC's grid generation software: mapx
   - https://github.com/nsidc/mapx
 - Learn how to read binary and reshape a numpy array after reading a mapx binary grid file
 - FIX: GridUtils: Reformat lon > 180 
 - lcc_grid.gpd almost replicates Niki's example grid; degress vs meters
 - Create a 3rd example that generates a 1x1 grid for testing

# 2021-04-09

 - Fix warning in GridUtils.plotGrid()
 - Change warnings to logging.WARNING messages
 - Moved all print statements to printMsg calls
 - Fix printing to STDOUT when msgBox is not defined
 - Add a function that allows tweaking of noisy python modules that send information to the log.
 - Add Manual documentation
 - Add application Setup tab for other obscure toolset options; add setter and getter methods in GridUtils()
   - Use numpypi: True/False
   - Enable logging: True/False
   - Specify logfile: "filename"
   - Specify logging level
   - Specify verbose level
   - Specify debug level
   - Log erase button
 - Update some important references
 - We can add param.watch to any control to trigger events when certain things happen.
 - We also learned that a lot of python modules leverage the logging module and that some of
   those modules are very verbose.  We setup a function to reduce some of that noise.
 - Once a logger is created, it cannot be deleted.  It can be enabled and disabled.
 - Add a small program example to show all available loggers after a GridUtils object is created.
 - TODO: Creating more small program examples to demonstrate logging and debugging techniques.
 - Use the setter functions in mkGridScripts and examples instead of setting the object variables directly.
   - TODO: consider moving important variables to private/hidden variables.

# 2021-04-08

 - Experimentation with panel.pane.HTML did not work pan out.  No great control over width and height.
   Text updates did not automatically resize the window.  The TextAreaInput automatically adds a
   scrollbar to the box when enough lines are added to the window.
 - Fixed up documentation of Grid Representation in the app manual.
 - Panel markdown honors the usage of options after a link. 
   Ex: [MOM6 User Manual](https://mom6.readthedocs.io/){target="\_blank"}
 - Testing of new printMsg facility is working.
 - Added a clear information button to clear the inforamtion window.

# 2021-04-07

 - Move Spherical.py to spherical.py to match coding standards
 - Use R from GridUtils class in spherical

# 2021-04-03

 - BUG: add ccrs.SouthPolarStereo() to projCarto
 - Remove plotExtentX0,X1 checks for lon>180
 - Moving the boilerplate into its own module works
 - BUG(migration): makeGrid() contained a small bug, parallels were not updating; missing self
 - reworked the way we start the app via show() and display()
 - BUG(migration): Plot button stopped working; missing self 
 - BUG(migration): Saving local files are fixed
 - BUG(migration): Call the showManual method with ()

# 2021-04-02

 - combined xgcmTools with xecmfTools configuration
 - added nbserverproxy to xecmfTools
 - moved documentation around
 - merge code updates from James
   - proj; applied application changes into gridutils so it is available to all
   - applied widget clean up for local file selection
 - add todos: LCC limitations; consider numpypi code
 - initial move to hide application boilerplate; help diff/debugging
 - discovered how to suppress xarray \_FillValue attributes
 - created mkGridScripts.py to demonstrate command line/ipython use
 - more documentation needed
 - document how numpypi and datashader should be installed
 - update extent display to show -180 to +180
 - most spinner widgets updated to numeric values instead of integer
 - establish a global for the defaultGridFilename
 - still need to understand how libraries, modules and packages are handled in python
 - migration of mkMap to mkGrid filename; we started with maps but have moved onto grids

