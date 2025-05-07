from library.structures import Grid, Edge, Node


for step in range(num_steps):
    grid.compute_fluxes()
    grid.update_nodes(dt)
    grid.swap_fields()

