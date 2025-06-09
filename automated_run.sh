#!/bin/bash

# PDE and Discrete contain year in their filename!
# PDE:      <ndays> <dx> <dy> <dt>
# Discrete: <ndays> <nperday>
# Plotter:  <year> <ndays> <dx> <dy> <dt> <nperday> <offset> 

# For 2016, 2017: Offset=0
# For >2017: offset = 360

ndays=500
dx=0.04
dy=0.04
dt=0.025
nperday=2

# year=2016
# offset=0
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

# year=2018
# offset=360
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

# year=2019
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

# year=2020
#python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

year=2021
python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

# year=2022
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

# year=2023
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both


wait
exit 0



