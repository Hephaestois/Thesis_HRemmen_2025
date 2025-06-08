## Using the Code

Hello! If you’re curious to re-run our models or experiment with them, this README is for you. We encourage you to engage with the code, which accompanies our thesis.

---

### Project Structure

The repository is organized into directories corresponding to different topics:

- `/discrete_model`: The individual-based (IB) model.
- `/pde_model`: The PDE model.
- `/library`: A shared library with core data structures (e.g., walkers, FVM grid).
- `/data`: A shared location for data reading and writing.
- `/plotting`: Scripts for creating figures and videos.
- Output directories for plots and videos.

All data flows through `/data`, and **no Python file directly calls both a model and the plotting routines**—these must be executed separately. While this may seem tedious, it enables flexible and automated workflows. For example, you can generate data once and create multiple plots afterward.

---

### Important Note on Data Handling

Currently, there is no shared function to retrieve flow data for a specific date. Instead, each year has its own file, with dataset calls hardcoded. Consequently:

- Adjustments (like parameter changes or bug fixes) must be made in each year’s script.
- Flow datasets differ by year, and coordinate systems may vary (some using `[-180°, 180°]`, others `[0°, 360°]`). An `offset` parameter in the plotting scripts handles this.

---

### Running the Models

Each Python file is structured for terminal execution. Example usage for years 2016–2023:

- **PDE MODEL**  

  ```python pde_model/FVM<year>.py <sim_days> <dx> <dy> <dt>```
- **IB MODEL**

  ```python discrete_model/RWinVF-<year>.py <sim_days> <n_per_day>```

where:
- `sim_days`: Number of simulation days (usually 500).
- `dx`, `dy`, `dt`: Spatial and temporal step sizes (PDE model only).
- `n_per_day`: Number of agents released daily (IB model only).

Each run saves output data to `/data`.

---

### Automating runs

Given that models can take tens of minutes to run, automation is recommended. You can use a simple Bash script, like this:

```
#!/bin/bash
ndays=500
dx=0.04
dy=0.04
dt=0.025
nperday=2
year=2016
frame=100
mode=both
offset=0

python discrete_model/RWinVF-${year}.py $ndays $nperday
python pde_model/FVM${year}.py $ndays $dx $dy $dt

python plotting/plot_image_fine.py $year $ndays $dx $dy $dt $nperday \
$offset $frame $mode
python plotting/plot_video_fine.py $year $ndays $dx $dy $dt $nperday \
$offset $mode

exit 0
```
where:
- `frame`: The day index for plots.
- `mode`: Can be rw, pde, or both to specify which model’s data to plot.
- `offset`: Adjusts for longitude coordinate differences in flow data files.
- 'fine': Some plotting routines (like plot_image_fine.py) handle higher-resolution data output (0.04° × 0.04°). In principle, plotting code could infer resolution directly from dx and dy, but this feature was not implemented.

---





