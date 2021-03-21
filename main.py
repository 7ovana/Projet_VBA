from BM_trajectories_generator import *
from BM_database_sqlite3 import *

N = 5  # number of trajectories
m = 20  # number of jumps in a trajectory

# Generate brownian motion
space, B = brownian_trajectory_onedimensional(N, m)

# Create an sqlite3 database containing the generated brownian motion
db = BM_database('brownian_trajectories.db')
db.connect()
db.create_table_data()
db.reinitialize_table_data()
for i in range(N):
    db.add_trajectory_to_table_data(i+1, space, B[i, ], m)
db.display_data('all')  # optional
db.disconnect()
