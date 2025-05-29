#!/bin/bash

# PDE and Discrete contain year in their filename!
# PDE:      <ndays> <dx> <dy> <dt>
# Discrete: <ndays> <nperday>
# Plotter:  <year> <ndays> <dx> <dy> <dt> <nperday> <offset> 

# For 2016, 2017: Offset=0
# For >2017: offset = 360

ndays=100
dx=0.1
dy=0.1
dt=0.01
nperday=2
offset=0

### 2016
year=2016
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python "discrete_model/RWinVF-${year}.py" $ndays $nperday
# python plotting/combined_plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset


python plotting/plot_image.py $year $ndays $dx $dy $dt $nperday $offset 100 both
python plotting/plot_video.py $year $ndays $dx $dy $dt $nperday $offset both

dx=0.04
dy=0.04
dt=0.025
python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday $offset 100 both
python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

