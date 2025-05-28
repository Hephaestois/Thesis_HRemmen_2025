#!/bin/bash

# PDE and Discrete contain year in their filename!
# PDE:      <ndays> <dx> <dy> <dt>
# Discrete: <ndays> <nperday>
# Plotter:  <year> <ndays> <dx> <dy> <dt> <nperday> <offset> 

# For 2016, 2017: Offset=0
# For >2017: offset = 360

ndays=500
dx=0.1
dy=0.1
dt=0.01
nperday=2
offset=360

### 2019
year=2019
python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
python plotting/combined_plot_video.py $year $ndays $dx $dy $dt $nperday $offset

### 2021
year=2021
python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
python plotting/combined_plot_video.py $year $ndays $dx $dy $dt $nperday $offset

### 2023
year=2023
python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
python plotting/combined_plot_video.py $year $ndays $dx $dy $dt $nperday $offset




