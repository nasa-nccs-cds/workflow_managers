import xarray as xa

uri = "https://dataserver.nccs.nasa.gov//thredds/dodsC/bypass/CREATE-IP/reanalysis/MERRA2/mon/atmos/tas.ncml"
dset: xa.Dataset = xa.open_dataset( uri )
variable: xa.Variable = dset.variables['tas']
varData = variable[:, :, :]
print(f"VARIABLE SHAPE= {variable.shape}")