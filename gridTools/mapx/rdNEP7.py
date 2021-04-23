#!/usr/bin/env python3

import numpy as np
import xarray as xr
import pdb

xnp = 685
ynp = 1633
sz = 8
filename = "nep7.1633x685x2.double"
file = open(filename, mode='rb')

lon = np.frombuffer(file.read(sz*xnp*ynp), dtype=np.float64)
lat = np.frombuffer(file.read(sz*xnp*ynp), dtype=np.float64)

file.close()

print(lon)
print(lat)

nlon = np.reshape(lon,(-1,xnp))
nlat = np.reshape(lat,(-1,xnp))

pdb.set_trace()
