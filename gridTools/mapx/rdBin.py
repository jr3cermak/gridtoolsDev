#!/usr/bin/env python3

import numpy as np
import xarray as xr
import pdb

xnp = 3
ynp = 3
sz = 8
filename = "test.3x3x2.double"
file = open(filename, mode='rb')

lon = np.frombuffer(file.read(sz*xnp*ynp), dtype=np.float64)
lat = np.frombuffer(file.read(sz*xnp*ynp), dtype=np.float64)

file.close()

print(lon)
print(lat)

nlon = np.reshape(lon,(-1,3))
nlat = np.reshape(lat,(-1,3))

pdb.set_trace()
