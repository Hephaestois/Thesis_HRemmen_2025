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
nperday=20
offset=0

dx=0.04
dy=0.04
dt=0.025


### 2016
year=2016
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
year=2018
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
year=2019
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
year=2020
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
year=2021
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
year=2022
python "discrete_model/RWinVF-${year}.py" $ndays $nperday
year=2023
python "discrete_model/RWinVF-${year}.py" $ndays $nperday

# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both


# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 100 both &
# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 200 both &
# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 300 both &
# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 100 rw &
# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 200 rw &
# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 300 rw &
# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 100 pde &
# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 200 pde &
# python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 300 pde &


wait
exit 0



