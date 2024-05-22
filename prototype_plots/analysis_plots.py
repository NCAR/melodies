import os
import logging

import numpy as np
from scipy import stats

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point


def plot_scatter(config, time_series):

    plotdir = os.path.expandvars(config['analysis']['output_dir'])

    plt.figure(figsize=(6,4))

    for group_name in config['regional_scatter_plots']:

        range_min = config['regional_scatter_plots'][group_name]['plot_params']['range_min']
        range_max = config['regional_scatter_plots'][group_name]['plot_params']['range_max']

        for region in config['regions']:

            ds_obs_name \
                = list(config['regional_scatter_plots'][group_name]['obs'].keys())[0]
            obs_label = config['regional_scatter_plots'][group_name]['obs'][ds_obs_name]['name']
            series_obs_name = '-'.join([group_name, ds_obs_name, region])

            series_obs = time_series[series_obs_name].values

            lon_bounds = config['regions'][region]['lon_bounds']
            lat_bounds = config['regions'][region]['lat_bounds']
            if lon_bounds[0] > 180.0:
                lon_bounds[0] -= 360.0
            if lon_bounds[1] > 180.0:
                lon_bounds[1] -= 360.0

            for ds_model_name in config['regional_scatter_plots'][group_name]['model']:

                plotfile = os.path.join(plotdir,
                    'scatter_' + ds_model_name + '_' + group_name + '_' + region)
                logging.info(plotfile)
                color = config['regional_scatter_plots'][group_name]['model'][ds_model_name]['color']

                series_model_name = '-'.join([group_name, ds_model_name, region])
                series_model = time_series[series_model_name].values

                fit = stats.linregress(series_obs, series_model)
                # slope, intercept, rvalue (correlation), pvalue, stderr, intercept_stderr

                ax = plt.axes()
                ax.set_xlim(range_min, range_max)
                ax.set_ylim(range_min, range_max)
                ax.set_xlabel(obs_label)
                ax.set_ylabel(ds_model_name)
                ax.set_title(config['regional_scatter_plots'][group_name]['plot_params']['name']
                    + '    ' + region.replace('_', ' '))

                ax_region = plt.axes([0.15, 0.57, 0.3, 0.3],
                    projection=ccrs.PlateCarree())
                ax_region.coastlines()
                ax_region.set_xlim(-180, 180)
                ax_region.set_ylim(-90, 90)
                ax_region.plot(
                    [lon_bounds[0], lon_bounds[1]], [lat_bounds[0], lat_bounds[0]],
                    linewidth=1, color='m')
                ax_region.plot(
                    [lon_bounds[1], lon_bounds[1]], [lat_bounds[0], lat_bounds[1]],
                    linewidth=1, color='m')
                ax_region.plot(
                    [lon_bounds[1], lon_bounds[0]], [lat_bounds[1], lat_bounds[1]],
                    linewidth=1, color='m')
                ax_region.plot(
                    [lon_bounds[0], lon_bounds[0]], [lat_bounds[1], lat_bounds[0]],
                    linewidth=1, color='m')
                # ax_region.text(-160, 80, r'%.4g $< \phi <$ %.4g, %.4g $< \lambda <$ %.4g'
                #     % (lat_bounds[0], lat_bounds[1], lon_bounds[0], lon_bounds[1]), fontsize=8, color='m')
                ax_region.set_title(r'%.4g < $\phi$ < %.4g N, %.4g < $\lambda$ < %.4g E'
                    % (lat_bounds[0], lat_bounds[1], lon_bounds[0], lon_bounds[1]), fontsize=8)

                """
                ax_timeseries = plt.axes([0.15, 0.55, 0.3, 0.1])
                ax_timeseries.set_xlim(1, len(series_model))
                ax_timeseries.set_ylim(range_min, range_max)
                ax_timeseries.set_xticks([])
                ax_timeseries.set_yticks([0.2, 0.4, 0.6, 0.8])
                ax_timeseries.tick_params(axis='x', labelsize=8)
                ax_timeseries.tick_params(axis='y', labelsize=8)
                ax_timeseries.xaxis.tick_top()
                ax_timeseries.yaxis.tick_right()
                ax_timeseries.plot(series_model, linewidth=1, color='m')
                ax_timeseries.plot(series_obs, linewidth=0.7, color='k')
                """

                delta = range_max - range_min
                ax.text(range_min + 0.45 * delta, range_min + 0.9 * delta,
                    r'Slope %.2g $\pm$ %.2g' % (fit.slope, fit.stderr))
                ax.text(range_min + 0.45 * delta, range_min + 0.85 * delta,
                    r'Intercept %.2g $\pm$ %.2g'
                    % (fit.intercept, fit.intercept_stderr))
                ax.text(range_min + 0.45 * delta, range_min + 0.8 * delta,
                    r'Correlation %.2g' % fit.rvalue)

                ax.plot([range_min, range_max], [range_min, range_max], color='k')
                ax.scatter(series_obs, series_model, marker='.',
                    color=mcolors.CSS4_COLORS[color])
                # y = m x + b
                ax.plot([range_min, range_max],
                    [fit.slope * range_min + fit.intercept,
                     fit.slope * range_max + fit.intercept], color='grey')
                ax.plot([range_min, range_max],
                    [(fit.slope + fit.stderr) * range_min + fit.intercept + fit.intercept_stderr,
                     (fit.slope + fit.stderr) * range_max + fit.intercept + fit.intercept_stderr],
                     linestyle='--', color='grey')
                ax.plot([range_min, range_max],
                    [(fit.slope - fit.stderr) * range_min + fit.intercept - fit.intercept_stderr,
                     (fit.slope - fit.stderr) * range_max + fit.intercept - fit.intercept_stderr],
                     linestyle='--', color='grey')

                plt.savefig(plotfile + '.png', bbox_inches='tight', dpi=1000)
                plt.clf()


def plot_time_series(config, time_series):

    plotdir = os.path.expandvars(config['analysis']['output_dir'])

    plt.figure(figsize=(10,4))

    for group_name in config['regional_time_series']:
        for region in config['regions']:

            plotfile = os.path.join(plotdir, 'time_series_' + group_name + '_' + region)
            logging.info(plotfile)
            labels = []

            ax = plt.axes()

            for ds_name in config['regional_time_series'][group_name]['datasets']:
                series_name = '-'.join([group_name, ds_name, region])
                color = config['regional_time_series'][group_name]['datasets'][ds_name]['color']

                labels.append(ds_name)
                time_series[series_name].plot(ax=ax, color=mcolors.CSS4_COLORS[color])

            ax.set_title(config['regional_time_series'][group_name]['plot_params']['name']
                + '    ' + region.replace('_', ' '))
            ax.legend(labels)
            plt.savefig(plotfile + '.png', bbox_inches='tight', dpi=1000)
            # plt.savefig(plotfile + '.pdf', bbox_inches='tight')
            # plt.savefig(plotfile + '.ps', bbox_inches='tight')
            plt.clf()


def plot_lon_lat(plotfile, plotname,
    plot_params, field, symmetric=False):

    logging.info(plotfile)

    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

    ax = plt.axes(projection=ccrs.PlateCarree())

    lon_values = field.lon.values
    lat_values = field.lat.values

    levels = np.linspace(
        plot_params['range_min'], plot_params['range_max'],
        plot_params['nlevel'], endpoint=True)
    if 'augment_levels' in plot_params:
        levels = sorted(np.append(
            levels, np.array(plot_params['augment_levels'])))

    if field.ndim == 3: 
        # field_values = np.clip(field.values[0,:,:], levels[0], levels[-1])
        field_values = field.values[0,:,:]
    else:
        # field_values = np.clip(field.values[:,:], levels[0], levels[-1])
        field_values = field.values[:,:]

    field_values, lon_values \
        = add_cyclic_point(field_values, coord=lon_values)

    lon_mesh, lat_mesh \
        = np.meshgrid(lon_values, lat_values)

    print(np.nanmin(field_values), np.nanmax(field_values))
    field_mean = np.nanmean(field_values)

    extend_option = 'both' if symmetric else 'max' 
    cmap_option = plt.cm.bwr if symmetric else plt.cm.turbo

    cp = ax.contourf(lon_mesh, lat_mesh, field_values,
        levels, cmap=cmap_option, extend=extend_option,
        transform=ccrs.PlateCarree())

    # ax.gridlines()
    ax.set_facecolor('gray')
    ax.coastlines()
    # ax.add_feature(cfeature.BORDERS)
    # ax.add_feature(states_provinces)

    plt.title(plotname + ('  Mean %.2g' % field_mean))

    cbar = plt.colorbar(cp, orientation='horizontal', pad=0.05)

    if 'ticks' in plot_params:
        cbar.set_ticks(plot_params['ticks'])
    if 'tick_labels' in plot_params:
        cbar.ax.set_xticklabels(plot_params['tick_labels'])
    cbar.ax.tick_params(labelsize=6)

    png_file = os.path.join(plot_params['outdir'], plotfile) + '.png'
    pdf_file = os.path.join(plot_params['outdir'], plotfile) + '.pdf'
    ps_file = os.path.join(plot_params['outdir'], plotfile) + '.ps'
    plt.savefig(png_file, bbox_inches='tight', dpi=300)
    plt.savefig(pdf_file, bbox_inches='tight')
    command = 'pdf2ps ' + pdf_file + ' ' + ps_file
    os.system(command)
    plt.clf()


def plot_seasonal_climos(ds_name, plotname, plot_params, ds):

    season_abbr = ['Mar-Apr-May', 'Jun-Jul-Aug', 'Sep-Oct-Nov', 'Dec-Jan-Feb']

    for varname in ds:
        if '_n' not in varname:
            for i_season in range(4):
                plotfile = ds_name + '_' + varname + '_' + season_abbr[i_season]
                field = ds[varname][:,:,i_season]
                plot_lon_lat(plotfile, plotname + ' ' + season_abbr[i_season],
                    plot_params, field)

