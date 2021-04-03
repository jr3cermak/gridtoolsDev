# Change Log

# 2021-04-03

 - BUG: add ccrs.SouthPolarStereo() to projCarto
 - Remove plotExtentX0,X1 checks for lon>180
 - Moving the boilerplate into its own module works

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

