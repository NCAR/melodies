#!/bin/bash
export PYTHONPATH=/glade/u/home/fillmore/MELODIES-MONET_develop_forecast:$PYTHONPATH
export PYTHONPATH=/glade/u/home/fillmore/monet:$PYTHONPATH
export PYTHONPATH=/glade/u/home/fillmore/monetio:$PYTHONPATH

yesterday_str=$(date --date=yesterday '+%Y%m%d')
today_str=$(date '+%Y%m%d')
tomorrow_str=$(date --date=tomorrow '+%Y%m%d')
echo $today_str $tomorrow_str
/glade/u/home/fillmore/miniconda3/envs/melodies-monet/bin/melodies-monet get-airnow --start-date $today_str --end-date $tomorrow_str -o /glade/work/fillmore/Data/AirNow/AirNow_$today_str.nc
