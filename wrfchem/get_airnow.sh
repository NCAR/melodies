#!/bin/bash
export PYTHONPATH=/glade/u/home/fillmore/MELODIES-MONET:$PYTHONPATH
export PYTHONPATH=/glade/u/home/fillmore/MONET:$PYTHONPATH
export PYTHONPATH=/glade/u/home/fillmore/MONETIO:$PYTHONPATH

yesterday_str=$(date --date=yesterday '+%Y%m%d')
today_str=$(date '+%Y%m%d')
echo $today_str
/glade/u/home/fillmore/miniconda3/bin/melodies-monet get-airnow --start-date $yesterday_str --end-date $today_str -o /glade/work/fillmore/Data/AirNow/AirNow_$yesterday_str.nc
