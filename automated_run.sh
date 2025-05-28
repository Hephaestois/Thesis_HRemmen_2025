#!/bin/bash

ndays=100
dx=0.1
dy=0.1
dt=0.01

python pde_model/FVM2016.py $ndays $dx $dy $dt
python plotting/combined_plot_video.py 2016 $ndays $dx $dy $dt





