# gridtools.app()

# Modules

import numpy as np
import cartopy.crs as ccrs
import os, sys, io
import cartopy
import matplotlib.pyplot as plt
import netCDF4 as nc
import warnings
import xarray as xr
import xgcm
from io import BytesIO

# This is called by GridTools() and can't be
# called by itself.

class App:

    def __init__(self, grd=None):
        # Globals
        
        # Applications own copy of GridTools() object
        self.grd = grd

        # Default grid filename
        self.defaultGridFilename = 'gridFile.nc'

        # How we grow the grid from the specified latitude (lat0) or longitude (lon0)
        # TODO: If 'Center' is not chosen then the controls for Central Latitude and Central Longitude no longer make sense.
        # For now: we assume Center/Center for making grids.
        self.xGridModes = ['Left', 'Center', 'Right']
        self.yGridModes = ['Lower', 'Center', 'Upper']

        # For now only MOM6 works.  It could work for other grids!
        #gridTypes = ["MOM6", "ROMS", "WRF"]
        self.gridTypes = ["MOM6"]

        # Available plot projections
        self.plotProjections = ["Nearside Perspective", "Mercator", "Lambert Conformal Conic", "North Polar Stereographic", "South Polar Stereographic"]
        self.plotProjectionsGridTools = ["NearsidePerspective", "Mercator", "LambertConformalConic", "NorthPolarStereo", "SouthPolarStereo"]
        self.plotProjectionsDict = dict(zip(plotProjections, plotProjectionsGridTools))

        # Supported grid projections
        self.projNames = ["Mercator", "Lambert Conformal Conic", "North Polar Stereographic", "South Polar Stereographic"]
        self.gridToolNames = ["Mercator", "LambertConformalConic", "NorthPolarStereo", "SouthPolarStereo"]
        self.projNamesGridTools = dict(zip(projNames, gridToolNames))
        self.projCarto = [ccrs.Mercator(), ccrs.LambertConformal(),  ccrs.NorthPolarStereo()]
        self.projDict = dict(zip(projNames,projCarto))

        # Plot grid modes
        # gridExtent, gridCells, superGrid
        self.plotGridModes = ['gridExtent', 'gridCells', 'superGrid']
        self.plotGridModesDescriptions = ['Grid Extent', 'Grid Cells', 'Supergrid Cells']
        self.plotGridModeDict = dict(zip(plotGridModesDescriptions, plotGridModes))

        self.plotColors = ['b', 'c', 'g', 'k', 'm', 'r', 'y']
        self.plotColorsDescriptions = ['Blue', 'Cyan', 'Green', 'Black', 'Magenta', 'Red', 'Yellow']
        self.plotColorDict = dict(zip(plotColorsDescriptions, plotColors))

        self.plotLineStyles = ['solid', 'dotted', 'dashed', 'dashdot']
        self.plotLineStylesDescriptions = ['Solid', 'Dotted', 'Dashed', 'DashDot']
        self.plotLineStyleDict = dict(zip(plotLineStylesDescriptions, plotLineStyles))

        # This controls the default figure size of the plot in the panel application
        # TODO: Improve integration
        # aspect 4:3, default dpi=144
        self.widthIn = 5.0
        self.heightIn = (widthIn * 3.0) / 4.0
        self.defaultPlotFigureSize = (widthIn, heightIn)

        # plotWidgetWidth and plotWidgetHeight
        # used by other controls
        self.plotWidgetWidth = 800
        self.plotWidgetHeight = 600
        
        self.initializeWidgets()
        self.initializeTabs()
        self.initializeDashboard()

    # Panel application functions

    def updateDataView(self):
        dataView[0] = grd.grid
        return

    def updateFilename(self, newFilename):
        gridFilenameLocal.value = newFilename
        gridFilenameRemote.value = newFilename
        return

    def downloadNetCDF(self):
        # See if we have a race condition
        saveLocalGridButton.filename = gridFilenameLocal.value
        bout = grd.grid.to_netcdf(encoding=grd.grid.removeFillValueAttributes())
        bio = BytesIO()
        bio.write(bout)
        bio.seek(0)
        return bio

    def loadLocalGrid(self, event):

        if localFileSelection.value == None:
            statusWidget.value = "A grid file has not been selected in the Local File tab."
            return

        # Test to see if xarray can load the selected file
        try:
            ncTest = xr.load_dataset(localFileSelection.value)
            statusWidget.value = "The grid file %s was loaded." % (localFileSelection.filename)
            grd.clearGrid()
            grd.readGrid(local=ncTest, localFilename=localFileSelection.filename)
            updateDataView()
            updateFilename(localFileSelection.filename)
        except:
            statusWidget.value = "The grid file %s was not loadable." % (localFileSelection.filename)

        return
    
    def loadRemoteGrid(self, event):

        ct = len(remoteFileSelection.value)

        if ct == 0:
            statusWidget.value = "A grid file has not been selected in the Remote File tab."
            return

        try:
            fileToOpen = remoteFileSelection.value[0]
            grd.openDataset(remoteFileSelection.value[0])
            grd.readGrid()
            statusWidget.value = "The grid file %s was loaded." % (fileToOpen)
            updateDataView()
            updateFilename(fileToOpen)
        except:
            statusWidget.value = "Failed to load grid file: %s" % (fileToOpen)

        return

    def saveRemoteGrid(self, event):
        '''Attempt to save grid to remote filesystem using last known grid filename.'''
        grd.saveGrid(filename=gridFilenameRemote.value)

    def make_grid(self, event):
        updateMessage = "No additional information."
        statusWidget.value = "Running make_grid()"
        grd.clearGrid()
        grd.setGridParameters({
            'projection': {
                'name': projNamesGridTools[gridProjection.value],
                'lon_0': float(glon0.value),
                'lat_0': float(glat0.value)
            },
            'dx': int(dx.value),
            'dy': int(dy.value),
            'dxUnits': 'degrees',
            'dyUnits': 'degrees',    
            'gridResolution': float(gridResolution.value),
            'gridMode': float(gridMode.value),
            'tilt': float(gtilt.value)
        })
        grd.makeGrid()

        # Update the plot if we updated the grid
        plotWindow.object = make_plot()

        # Update grid info
        updateDataView()

        if projNamesGridTools[gridProjection.value] == 'LambertConformalConic':
            # For this projection LCC sets lat_1 and lat_2 based on grid inputs.
            updateMessage = "NOTICE: Grid first and second parallels (lat_1, lat_2) have been changed to (%s, %s)." %\
                (grd.gridInfo['gridParameters']['projection']['lat_1'], grd.gridInfo['gridParameters']['projection']['lat_2'])
            glat1.value = grd.gridInfo['gridParameters']['projection']['lat_1']
            glat2.value = grd.gridInfo['gridParameters']['projection']['lat_2']

        statusWidget.value = "Make grid succeeded: %s" % (updateMessage)

        return

    def make_plot(self):
        statusWidget.value = "Running make_plot()"

        if plotTitle.value != "":
            mp_title = plotTitle.value
        else:
            selectedProjection = plotProjection.value
            mp_title = "%s: " % (selectedProjection) + str(dx.value) + "x" + str(dy.value) + " with " + str(gtilt.value) + " degree tilt"

        # Check plotGridMode.value to set plot parameter showGridCells
        showGridCellsState = False
        pGridMode = plotGridModeDict[plotGridMode.value]
        if pGridMode == 'gridCells':
            showGridCellsState = True

        # Determine plot extent (this may vary depending on selected projection)
        plotExtentState = []
        # If we are not using the global projection, use the user supplied extents
        if not(plotUseGlobal.value):
            x0pt = plotExtentX0.value
            # May or maynot need this?
            if x0pt > 180.0:
                x0pt = x0pt - 360.0
            x1pt = plotExtentX1.value
            if x1pt > 180.0:
                x1pt = x1pt - 360.0

            plotExtentState = [x0pt, x1pt,
                              plotExtentY0.value, plotExtentY1.value]

        # These inputs will have to change based on selected projection
        grd.setPlotParameters(
            {
                'figsize': defaultPlotFigureSize,
                'projection' : {
                    'name': plotProjectionsDict[plotProjection.value],
                    'lat_0': float(plat0.value),
                    'lon_0': float(plon0.value)
                },
                'extent': plotExtentState,
                'iLinewidth': plotXLineWidth.value,
                'jLinewidth': plotYLineWidth.value,
                'showGridCells': showGridCellsState,
                'title': mp_title,
                'iColor': plotColorDict[plotXColor.value],
                'jColor': plotColorDict[plotYColor.value]
            }
        )
        if grd.xrOpen:
            (figure, axes) = grd.plotGrid()
        else:
            figure = grd.newFigure()
            statusWidget.value = "Running make_plot(): plotting failure"
            return figure

        statusWidget.value = "Running make_plot(): done"       
        return figure

    def plotRefresh(self, event):
        plotWindow.object = make_plot()
        return

    def showManual(self):
        manualTabs = pn.Tabs()

        pageMain = pn.WidgetBox('''
        # Instructions
        This will be the eventual location for the instruction manual.
        ''', width=plotWidgetWidth)

        pageGrids = pn.WidgetBox('''
        # Grids
        ***We love grids!***
        ## Grid Reference
        This controls how the grid is grown from the selected latitude (lat0) and longitude (lon0) using
        degrees or x (x0) or y (y0) using meters.  By default, the grid is grown from the center point
        in both directions based on the size (dy, dx) and grid resolution.  In the future, grids may
        be build with other fixed points of reference.

        ## Grid Type
        For now, only MOM6 is supported.  Other grid types may be possible in the future.

        ## Grid Mode
        Internally, this mode is 2 which really means computations
        are done to compute vertices for the grid cells and vertices through the center points of the
        grid cells.  At present, this mode should not be anything other than 2 for MOM6 grids.

        ## Grid Representation
        Here is a representation of a (2,3) MOM6 grid from convert_ROMS_grid_to_MOM6.py
        by Mehmet Ilicak and Alistair Adcroft.

        ```
         3    + | + | + | +
              - p - p - p -
         2    + | + | + | +
              - p - p - p -
         1    + | + | + | +

              1   2   3   4

        KEY: p = rho (center) points
             + = psi (corner) points
             - = u points
             | = v points
        ```

        A MOM6 grid of (ny, nx) will have (ny\*2+1, nx\*2+1) points on the supergrid.
        ''', width=plotWidgetWidth)

        manualTabs.extend([
            ('Main', pageMain),
            ('Grids', pageGrids)
        ])

        return manualTabs
    
    def initializeWidgets(self):
        # Widgets
        statusWidget = pn.widgets.TextAreaInput(name='Information', value="", background="skyblue", height=100)

        # Grid Controls
        # Use: Niki's defaults for rapid testing
        # 30x20 tilt 30 deg lat_0 40.0 lon_0 230.0 Res 1.0
        gridProjection = pn.widgets.Select(name='Projection', options=projNames, value=projNames[1])
        gridType = pn.widgets.Select(name="Grid Type", options=gridTypes, value=gridTypes[0])
        gridType.disabled = True
        gridResolution = pn.widgets.Spinner(name="Grid Resolution", value=1.0, step=0.1, start=0.0, end=10.0, width=80)
        gridMode = pn.widgets.Spinner(name="Grid Mode", value=2, step=1, start=1, end=2, width=80)
        gridMode.disabled = True
        unitNames = ['degrees','meters']
        dxdyUnits = pn.widgets.Select(name='Units', options=unitNames, value=unitNames[0])
        dx = pn.widgets.Spinner(name="dx", value=20, step=1, start=0, end=100, width=100)
        dy = pn.widgets.Spinner(name="dy", value=30, step=1, start=0, end=100, width=100)
        glon0 = pn.widgets.Spinner(name="Central Longitude(lon_0) (0 to 360)", value=230.0, step=1.0, start=0.0, end=360.0, width=100)
        glat0 = pn.widgets.Spinner(name="Central Latitude(lat_0) (-90 to 90)", value=40.0, step=1.0, start=-90.0, end=90.0, width=100)
        glat1 = pn.widgets.Spinner(name="First Parallel(lat_1) (-90 to 90)", value=40.0, step=1.0, start=-90.0, end=90.0, width=100)
        glat2 = pn.widgets.Spinner(name="Second Parallel(lat_2) (-90 to 90)", value=40.0, step=1.0, start=-90.0, end=90.0, width=100)
        glatts = pn.widgets.Spinner(name="Latitude of True Scale(lat_ts) (-90 to 90)", value=40.0, step=1.0, start=-90.0, end=90.0, width=100)
        gtilt = pn.widgets.Spinner(name="Tilt (-90 to 90)", value=30.0, step=0.1, start=-90.0, end=90.0, width=100)
        gridControlUpdateButton = pn.widgets.Button(name='Make Grid', button_type='primary')
        gridControlUpdateButton.on_click(make_grid)
        xGridControl = pn.widgets.Select(name='X grid mode', options=xGridModes, value=xGridModes[1])
        yGridControl = pn.widgets.Select(name='Y grid mode', options=yGridModes, value=yGridModes[1])

        # Plot Controls
        # Use Niki's defaults for rapid testing
        # extent: -160, -100, 60, 20

        # Projection
        plotProjection = pn.widgets.Select(name='Projection', options=plotProjections, value=plotProjections[0])
        plon0 = pn.widgets.Spinner(name="Central Longitude(lon_0) (0 to 360)", value=230.0, step=1.0, start=0.0, end=360.0, width=100)
        plat0 = pn.widgets.Spinner(name="Central Latitude(lat_0) (-90 to 90)", value=40.0, step=1.0, start=-90.0, end=90.0, width=100)
        plat1 = pn.widgets.Spinner(name="First Parallel(lat_1) (-90 to 90)", value=40.0, step=1.0, start=-90.0, end=90.0, width=100)
        plat2 = pn.widgets.Spinner(name="Second Parallel(lat_2) (-90 to 90)", value=40.0, step=1.0, start=-90.0, end=90.0, width=100)
        platts = pn.widgets.Spinner(name="Latitude of True Scale(lat_ts) (-90 to 90)", value=40.0, step=1.0, start=-90.0, end=90.0, width=100)

        # Extent
        # CARTOPY: (x0, x1, y0, y1)
        #  https://scitools.org.uk/cartopy/docs/latest/matplotlib/geoaxes.html
        plotExtentX0 = pn.widgets.Spinner(name="Longitude(x0) (-180 to 180)", value=-160.0, step=1.0, start=-180.0, end=180.0, width=100)
        plotExtentX1 = pn.widgets.Spinner(name="Longitude(x1) (-180 to 180)", value=-100.0, step=1.0, start=-180.0, end=180.0, width=100)
        plotExtentY0 = pn.widgets.Spinner(name="Latitude(y0) (-90 to 90)", value=20.0, step=1.0, start=-90.0, end=90.0, width=100)
        plotExtentY1 = pn.widgets.Spinner(name="Latitude(y1) (-90 to 90)", value=60.0, step=1.0, start=-90.0, end=90.0, width=100)
        plotUseGlobal = pn.widgets.Checkbox(name="Use global extent (disables custom extent)")

        # Style
        plotTitle = pn.widgets.TextInput(name='Plot title', value="", width=250)
        plotGridMode = pn.widgets.Select(name='Grid Style', options=plotGridModesDescriptions, value=plotGridModesDescriptions[1])
        plotXColor = pn.widgets.Select(name='x Color', options=plotColorsDescriptions, value=plotColorsDescriptions[3])
        plotYColor = pn.widgets.Select(name='y Color', options=plotColorsDescriptions, value=plotColorsDescriptions[3])
        plotXLineWidth = pn.widgets.Spinner(name="x Line Width", value=1.0, step=0.1, start=0.01, end=10.0, width=80)
        plotYLineWidth = pn.widgets.Spinner(name="y Line Width", value=1.0, step=0.1, start=0.01, end=10.0, width=80)

        # Grid Save/Load controls

        # Grid file name
        # NOTE: Sharing a text field is not recommended.  It will display
        # more than once, but only one will actually update.
        gridFilenameLocal = pn.widgets.TextInput(name='Grid filename', value=defaultGridFilename, width=200)
        gridFilenameRemote = pn.widgets.TextInput(name='Grid filename', value=defaultGridFilename, width=200)

        # File download button and call back function
        # We can't put a variable in the filename= argument below.  It isn't updated
        # when the assigned variable is updated.  Any updates need to be done to
        # saveLocalGridButton.filename when the local file name is changed.  We
        # also discovered if we updated in the callback it also works.  Might
        # encounter a race condition later.  Watch for it.
        saveLocalGridButton = pn.widgets.FileDownload(
            label="Download Grid",
            button_type='success',
            callback=downloadNetCDF,
            filename=defaultGridFilename)

        # Local file selection
        localFileSelection = pn.widgets.FileInput(accept='.nc')

        # Remote file selection
        remoteFileSelection = pn.widgets.FileSelector('~', file_pattern='*.nc')

        # Load grid buttons
        loadLocalGridButton = pn.widgets.Button(name='Load Local Grid', button_type='primary')
        loadLocalGridButton.on_click(loadLocalGrid)

        loadRemoteGridButton = pn.widgets.Button(name='Load Remote Grid', button_type='primary')
        loadRemoteGridButton.on_click(loadRemoteGrid)

        saveRemoteGridButton = pn.widgets.Button(name='Save Remote Grid', button_type='success')
        saveRemoteGridButton.on_click(saveRemoteGrid)

        # Plot controls
        plotControlUpdateButton = pn.widgets.Button(name='Plot', button_type='primary')
        plotControlUpdateButton.on_click(plotRefresh)

        # The plot itself wrapped in a widget
        # Use panel.pane.Matplotlib(matplotlib.figure)
        plotWindow = pn.pane.Matplotlib(make_plot(), width=plotWidgetWidth, height=plotWidgetHeight)

        # This presents a data view summary of the xarray object
        dataView = pn.Column(grd.grid, width=plotWidgetWidth)
        
    def initializeTabs(self):
        # Tabs

        # Plot and Grid controls
        controlTabs = pn.Tabs()
        plotControlTabs = pn.Tabs()
        gridControlTabs = pn.Tabs()

        # If the Alt layout works, we can replace the existing.
        displayTabs = pn.Tabs()
        displayTabsAlt = pn.Tabs()
        saveLoadTabs = pn.Tabs()

        # Pull controls together

        # Plot controls
        plotProjectionControls = pn.WidgetBox('# Plot Projection', plotProjection, plon0, plat0, plat1, plat2, platts, plotControlUpdateButton)
        plotExtentControls = pn.WidgetBox('# Plot Extent', plotExtentX0, plotExtentX1, plotExtentY0, plotExtentY1, plotUseGlobal)
        plotStyleControls = pn.WidgetBox('# Plot Style', plotTitle, plotGridMode, plotXColor, plotYColor, plotXLineWidth, plotYLineWidth)

        # Grid controls
        gridProjectionControls = pn.WidgetBox('# Grid Projection', gridProjection, glon0, glat0, glat1, glat2, glatts, gtilt, gridControlUpdateButton)
        gridSpacingControls = pn.WidgetBox('# Grid Spacing', dx, dy, gridResolution, dxdyUnits, gridControlUpdateButton)
        gridAdvancedControls = pn.WidgetBox(
            """
            See Grids in the Manual tab for details about these controls.
            ## Grid Reference
            """, xGridControl, yGridControl, """    
            ## Grid Type
            For now, only MOM6 grids are supported.
            """, gridType, """
            ## Grid Mode
            For now, MOM6 grids require grid mode 2.
            """, gridMode)

        # Place controls into respective tabs

        # Control hierarchy (left panel)
        # Plot
        #  Projection
        #  Extent
        #  Style
        # Grid
        #  Projection
        #  Spacing
        #  Reference
        plotControlTabs.extend([
            ('Projection', plotProjectionControls),
            ('Extent', plotExtentControls),
            ('Style', plotStyleControls)
        ])

        gridControlTabs.extend([
            ('Projection', gridProjectionControls),
            ('Spacing', gridSpacingControls),
            ('Advanced', gridAdvancedControls)
        ])

        controlTabs.extend([
            ('Plot', plotControlTabs),
            ('Grid', gridControlTabs)
        ])

        displayTabs.extend([
            ('Grid Plot', plotWindow),
            ('Grid Info', dataView),
            ('Manual', showManual)
        ])

        localFilesWindow = pn.WidgetBox(
            '''
            # Local Files
            If you are running this notebook on the same computer as your web browser, accessing files
            from the Local Files tab and the Remote Files tab should look the same.  If you are running
            this notebook on a remote system, you may need to use the Remote Files tab to load grids on
            the remote system.  There may be size limit for loading/downloading files via the web
            browser (Local Files). You may change the grid filename prior to saving the grid.  Do not
            use it for file selection.  At this time, we only accept NetCDF file formats. 
            ''', '''### Upload Grid''', localFileSelection, loadLocalGridButton,
            ''' ### Download Grid''', gridFilenameLocal, saveLocalGridButton)

        remoteFilesWindow = pn.WidgetBox(loadRemoteGridButton, gridFilenameRemote, saveRemoteGridButton,
            '''
            # Remote Files
            This tab loads and saves grids to the remote system.  If you are running this notebook
            on the same system, either file tab will work.  You may change the grid filename prior
            to saving the grid.  Do not use it for file selection.
            ''', remoteFileSelection)

        saveLoadTabs.extend([
            ('Local Files', localFilesWindow),
            ('Remote Files', remoteFilesWindow)
        ])

        # Plotting area, data view, local/remote file access and manual
        displayTabsAlt.extend([
            ('Grid Plot', plotWindow),
            ('Grid Info', dataView),
            ('Local Files', localFilesWindow),
            ('Remote Files', remoteFilesWindow),
            ('Manual', showManual)
        ])
        
    def initializeDashboard(self):

        # Pull all the final dashboard together in an application
        dashboard = pn.WidgetBox(
            pn.Column(statusWidget, sizing_mode='stretch_width', width_policy='max'),
            pn.Row(controlTabs, displayTabsAlt)
        )
        
        # Attach application to GridUtils for integration into panel, etc
        # Do this just before launching the application
        grd.application(
            app={
                'messages': statusWidget,
                'defaultFigureSize': defaultPlotFigureSize
            }
        )