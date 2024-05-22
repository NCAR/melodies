import os
import numpy as np
import xarray as xr
from analysis_plots import plot_seasonal_climos
from analysis_plots import plot_lon_lat

def monthly_to_seasonal(ds):

    print(ds.coords)

    da = xr.DataArray(
        coords={'lat': ds.coords['lat'], 'lon': ds.coords['lon']},
        dims=['lat', 'lon'])
    print(da.coords)
    ds_season = xr.Dataset(
        coords={'lat': ds.coords['lat'], 'lon': ds.coords['lon'],
                'season': np.arange(4)})
    print(ds_season.coords)
    da_season = xr.DataArray(
         coords=ds_season.coords, dims=['lat', 'lon', 'season'])

    for varname in ds:
        if '_n' not in varname:
            print(varname)
            # MAM, JJA, SON, DJF
            ds_season[varname] = xr.zeros_like(da_season)
            ds_season[varname + '_n'] = xr.zeros_like(da_season, dtype=int)

            for i_season in range(4):

                data = xr.zeros_like(da)
                count = xr.zeros_like(da, dtype=int)
                for i in [(3 * i_season + 2) % 12, (3 * i_season + 3) % 12, (3 * i_season + 4) % 12]:
                    data.values += ds[varname].values[:,:,i] * ds[varname + '_n'].values[:,:,i]
                    count.values += ds[varname + '_n'].values[:,:,i]
                mask = np.greater(count.values, 0)
                data.values[mask] /= count.values[mask]
                mask = np.equal(count.values, 0)
                data.values[mask] = np.nan

                ds_season[varname].values[:,:,i_season] = data.values
                ds_season[varname + '_n'].values[:,:,i_season] = count.values

    return ds_season

climo_dir = os.path.join(os.getenv('HOME'), 'Data', 'Climos')
plot_dir = os.path.join(os.getenv('HOME'), 'Plots', 'CARMA')
file_carma = os.path.join(climo_dir, 'CARMA_climo.nc')
file_mam4 = os.path.join(climo_dir, 'MAM4_climo.nc')
file_merra2 = os.path.join(climo_dir, 'MERRA2_climo.nc')
file_mod08_m3 = os.path.join(climo_dir, 'MOD08_M3_climo.nc')

ds_carma = xr.open_dataset(file_carma)
ds_mam4 = xr.open_dataset(file_mam4)
ds_merra2 = xr.open_dataset(file_merra2)
ds_mod08_m3 = xr.open_dataset(file_mod08_m3)

ds_carma_season = monthly_to_seasonal(ds_carma)
ds_carma_season.to_netcdf(file_carma.replace('climo', 'seasonal_climo'))
ds_mam4_season = monthly_to_seasonal(ds_mam4)
ds_mam4_season.to_netcdf(file_mam4.replace('climo', 'seasonal_climo'))
ds_merra2_season = monthly_to_seasonal(ds_merra2)
ds_merra2_season.to_netcdf(file_merra2.replace('climo', 'seasonal_climo'))
ds_mod08_m3_season = monthly_to_seasonal(ds_mod08_m3)
ds_mod08_m3_season.to_netcdf(file_mod08_m3.replace('climo', 'seasonal_climo'))

plot_params = dict()
plot_params['outdir'] = plot_dir
plot_params['range_min'] = 0.0
plot_params['range_max'] = 0.8
plot_params['nlevel'] = 17
plot_params['augment_levels'] = [0.01, 0.02, 0.03, 0.04]
plot_params['ticks'] = [0.01, 0.03, 0.05,
    0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
plot_params['tick_labels'] = ['0.01', '0.03', '0.05',
    '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8']

plot_seasonal_climos('CARMA', 'CARMA AOD 550 nm  2001-2019',
    plot_params, ds_carma_season)
plot_seasonal_climos('MAM4', 'MAM4 AOD 550 nm  2001-2019',
    plot_params, ds_mam4_season)
plot_seasonal_climos('MERRA2', 'MERRA2 AOD 550 nm  2001-2019',
    plot_params, ds_merra2_season)
plot_seasonal_climos('MOD08_M3', 'Terra MODIS AOD 550 nm  2001-2019',
    plot_params, ds_mod08_m3_season)

plot_params = dict()
plot_params['outdir'] = plot_dir
plot_params['range_min'] = -0.4
plot_params['range_max'] = 0.4
plot_params['nlevel'] = 17

plot_params_relerr = dict()
plot_params_relerr['outdir'] = plot_dir
plot_params_relerr['range_min'] = -100
plot_params_relerr['range_max'] = 100
plot_params_relerr['nlevel'] = 21

for i_season in range(4):
    season_abbr = ['Mar-Apr-May', 'Jun-Jul-Aug', 'Sep-Oct-Nov', 'Dec-Jan-Feb']

    field = ds_carma_season['AODVIS'][:,:,i_season] \
        - ds_mod08_m3_season[
        'AOD_550_Dark_Target_Deep_Blue_Combined_Mean_Mean'][:,:,i_season]
    plot_lon_lat('CARMA-MOD08_M3-' + season_abbr[i_season],
        'CARMA - Terra MODIS AOD 550 nm',
        plot_params, field, symmetric=True)
    field_relerr = 100 * field / ds_mod08_m3_season[
        'AOD_550_Dark_Target_Deep_Blue_Combined_Mean_Mean'][:,:,i_season]
    field_relerr = np.clip(field_relerr, -100, 100)
    plot_lon_lat('percent_diff_CARMA-MOD08_M3-' + season_abbr[i_season],
        'Percent Diff CARMA - Terra MODIS AOD 550 nm',
        plot_params_relerr, field_relerr, symmetric=True)

    field = ds_mam4_season['AODVISdn'][:,:,i_season] \
        - ds_mod08_m3_season[
        'AOD_550_Dark_Target_Deep_Blue_Combined_Mean_Mean'][:,:,i_season]
    plot_lon_lat('MAM4-MOD08_M3-' + season_abbr[i_season],
        'MAM4 - Terra MODIS AOD 550 nm',
        plot_params, field, symmetric=True)
    field_relerr = 100 * field / ds_mod08_m3_season[
        'AOD_550_Dark_Target_Deep_Blue_Combined_Mean_Mean'][:,:,i_season]
    field_relerr = np.clip(field_relerr, -100, 100)
    plot_lon_lat('percent_diff_MAM4-MOD08_M3-' + season_abbr[i_season],
        'Percent Diff MAM4 - Terra MODIS AOD 550 nm',
        plot_params_relerr, field_relerr, symmetric=True)

    field \
        = ds_merra2_season['TOTEXTTAU'][:,:,i_season] \
        - ds_mod08_m3_season[
        'AOD_550_Dark_Target_Deep_Blue_Combined_Mean_Mean'][:,:,i_season]
    plot_lon_lat('MERRA2-MOD08_M3-' + season_abbr[i_season],
        'MERRA2 - Terra MODIS AOD 550 nm',
        plot_params, field, symmetric=True)
    field_relerr = 100 * field / ds_mod08_m3_season[
        'AOD_550_Dark_Target_Deep_Blue_Combined_Mean_Mean'][:,:,i_season]
    field_relerr = np.clip(field_relerr, -100, 100)
    plot_lon_lat('percent_diff_MERRA2-MOD08_M3-' + season_abbr[i_season],
        'Percent Diff MERRA2 - Terra MODIS AOD 550 nm',
        plot_params_relerr, field_relerr, symmetric=True)

