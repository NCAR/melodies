#!/bin/bash
export PYTHONPATH=/glade/u/home/fillmore/MELODIES-MONET_develop_forecast:$PYTHONPATH
export PYTHONPATH=/glade/u/home/fillmore/monet:$PYTHONPATH
export PYTHONPATH=/glade/u/home/fillmore/monetio:$PYTHONPATH

start_str="20200601"
end_str="20210101"
date_str=$start_str

while [ $date_str != $end_str ]; do
    next_str="$(date -d "$date_str + 1 day" +%Y%m%d)"
    echo $date_str $next_str
    /glade/u/home/fillmore/miniconda3/envs/melodies-monet/bin/melodies-monet get-airnow --start-date $date_str --end-date $next_str -o /glade/work/fillmore/Data/AirNow/AirNow_$date_str.nc
    date_str="$(date -d "$date_str + 1 day" +%Y%m%d)"
done
