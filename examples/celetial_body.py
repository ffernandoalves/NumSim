from numsim import init_verlet, load_data_generated, start_animation

data_in  = "examples/data/sun_system.csv"
data_out = "examples/data/output.csv"

init_verlet(data_in, data_out, delta_t=0.05, t_end=30.5)
df = load_data_generated(data_out)
start_animation(df)