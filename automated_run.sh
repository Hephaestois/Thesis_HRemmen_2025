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


### 2016
year=2016
offset=0

python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
python plotting/combined_plot_video.py $year $ndays $dx $dy $dt $nperday $offset


### 2018
offset=360
year=2018

python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
python plotting/combined_plot_video.py $year $ndays $dx $dy $dt $nperday $offset

### 2020
year=2020

python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
python plotting/combined_plot_video.py $year $ndays $dx $dy $dt $nperday $offset

### 2022
year=2022

python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
python plotting/combined_plot_video.py $year $ndays $dx $dy $dt $nperday $offset


### 2024
# year=2024

# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python "discrete_model/RWinVF-${year}.py" $ndays $nperday
# python plotting/combined_plot_video.py $year $ndays $dx $dy $dt $nperday $offset




