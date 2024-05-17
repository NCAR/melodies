#!/bin/bash
export PYTHONPATH=/glade/u/home/fillmore/MELODIES-MONET_develop_forecast:$PYTHONPATH
export PYTHONPATH=/glade/u/home/fillmore/monet:$PYTHONPATH
export PYTHONPATH=/glade/u/home/fillmore/monetio:$PYTHONPATH

yesterday_str=$(date --date=yesterday '+%Y%m%d')
today_str=$(date '+%Y%m%d')
echo $today_str
/glade/u/home/fillmore/miniconda3/envs/melodies-monet/bin/melodies-monet get-airnow --start-date $yesterday_str --end-date $today_str -o /glade/work/fillmore/Data/AirNow/AirNow_$yesterday_str.nc
