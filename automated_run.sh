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
# offset=360
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
#python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

year=2020
offset=360
python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

# year=2021
# offset=360
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

# year=2022
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both

# year=2023
# python "pde_model/FVM${year}.py" $ndays $dx $dy $dt
# python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday $offset both



# year=2016
# offset=0
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 100 both &
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 200 both &
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 300 both &
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 100 rw &
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 200 rw &
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 300 rw &
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 100 pde &
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 200 pde &
# python plotting/plot_image_fine_custom.py $year $ndays $dx $dy $dt $nperday $offset 300 pde




wait
exit 0



