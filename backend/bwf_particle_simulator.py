import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import csv
import time
import multiprocessing
from tqdm import tqdm
from personal.js_playground.backend.bwf_utilities import checkPlaneSide, defineGate, drawGate, defineOctahedron, drawOctahedron, samplePointsInASphere, samplePointsInABox

no_of_simulation_steps = 100
perturbation = 0.1
sampling = "cuboid"
dist_type = "3d_euclidean"
# dist_type = "2d_euclidean"
# dist_type = "2d_manhattan"
# dist_type = "2d_manhattan_mixed"
bwf_override = False
bwf_override_val = 1.0
bwf_field_half_strength = 3
position_cost_enabled = True
cost_threshold_enabled = True
visualise_bwf_only = True
cost_threshold_multiplier = 0.25
cost_threshold_override = 0.00
alpha_control = 0.1
spherical_samples = 100
slack_cost = 2000.0
scale_multiplier = 1.0
scale_max = 30
gate_outerside = 2.7
gate_innerside = 1.2
gate_edgelength = gate_outerside/2 - gate_innerside/2


# racetrack_trajectory = np.array(getCsvData("mrs_racetrack1.csv"), dtype=float)
# print(racetrack_trajectory.shape)
# racetrack_trajectory[:,1:4] += np.array([0,0,5])

time_now = time.time()
# make a 3D grid equally sampled
cc = np.array([4.55,-1.77,1.45])
n_vect = np.array([1.5,1.5,0])

points, bounding_planes, mid_plane, gate_vectors = defineGate(cc, n_vect, gate_innerside, gate_outerside)

if sampling == "sphere":
    X, Y, Z = samplePointsInASphere(cc, 5.0, spherical_samples)
else:
    X, Y, Z = samplePointsInABox(cc, [5.0, 5.0, 5.0], 10)

meshshape = X.shape[0]
print("Meshshape: ", meshshape)
# trajectories = np.zeros((no_of_simulation_steps, 3, meshshape))
trajectories_shared = multiprocessing.Array('d', meshshape * no_of_simulation_steps * 3)
perturbation_directions = perturbation*np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1],[1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0],[1,0,1],[-1,0,1],[1,0,-1],[-1,0,-1],[0,1,1],[0,-1,1],[0,1,-1],[0,-1,-1],[1,1,1],[-1,1,1],[1,-1,1],[-1,-1,1],[1,1,-1],[-1,1,-1],[1,-1,-1],[-1,-1,-1]])
costs = np.zeros((meshshape,))

def simulate_trajectories(start_index, end_index, thread_id, progress_bar):
    perturbation_vectos = perturbation_directions 
    # generate random small wiggles through perturbation vectors
    perturbation_vectos = np.random.uniform(-perturbation, perturbation, (perturbation_directions.shape[0], 3))
    traj_np = np.frombuffer(trajectories_shared.get_obj()).reshape((no_of_simulation_steps, 3, meshshape))
    for i in range(start_index, end_index):
        # print("Thread ID: " + thread_id, " finished calculating % = ", 100.0*float(i-start_index)/float(end_index-start_index))
        progress_bar.update(1)
        traj_np[0, :, i] = np.array([X[i], Y[i], Z[i]])
        for j in range(no_of_simulation_steps-1):
            perturbation_vectos = np.random.uniform(-perturbation, perturbation, (perturbation_directions.shape[0], 3))
            perturbation_costs = np.zeros((perturbation_vectos.shape[0],))
            for k in range(perturbation_vectos.shape[0]):
                p = traj_np[j,:,i] + perturbation_vectos[k]
                dist = 0.0
                post_dist = 0.0
                if(dist_type == "3d_euclidean"):
                    dist = np.linalg.norm(p-cc)
                elif(dist_type == "2d_euclidean"):
                    dist = np.sqrt((p[0]-cc[0])**2 + (p[2]-cc[2])**2)
                elif(dist_type == "2d_manhattan"):
                    dist = np.abs(p[0]-cc[0]) + np.abs(p[2]-cc[2])
                elif(dist_type == "2d_manhattan_mixed"):
                    dist = 1.5*np.abs(np.dot(n_vect.T, p-cc)) + np.abs(np.dot(gate_x_diag_vect.T, p-cc)) + np.abs(np.dot(gate_y_diag_vect.T, p-cc))
                post_dist = np.linalg.norm(p-cc)
                if position_cost_enabled:
                    perturbation_costs[k] += post_dist*post_dist*100.0
                bw = 1.0/(1.0 + (dist/3.0)**12.0)
                if bwf_override:
                    bwf = bwf_override_val
                else:
                    bwf = bw
                for pl in range(4):
                    plane_val = checkPlaneSide(bounding_planes[pl], p)*checkPlaneSide(bounding_planes[pl], cc)*bwf
                    if plane_val < 0:
                        temp_cost = plane_val * plane_val * slack_cost
                        perturbation_costs[k] += temp_cost
            # if i == 0:
            #     print("Perturbation costs: ", perturbation_costs)
            lowest_cost_index = np.argmin(perturbation_costs)
            # if i == 0:
            #     print("Picking lowest cost of: ", perturbation_costs[lowest_cost_index])
            traj_np[j+1, :, i] = traj_np[j,:,i] + perturbation_vectos[lowest_cost_index]
                # print("particle at: ", trajectories[j+1, :, i])
    # print("Thread ID: " + thread_id, " ",  trajectories[:, :, start_index:end_index])




# multi-threading
# import threading
# threads = []
# thread_count = 16
# for i in range(thread_count):
#     start_index = int(i*meshshape/thread_count)
#     end_index = int((i+1)*meshshape/thread_count)
#     t = threading.Thread(target=simulate_trajectories, args=(start_index, end_index, str(i)))
#     threads.append(t)
#     t.start()
# for t in threads:
#     t.join()

# multi-processing
processes = []
process_count = multiprocessing.cpu_count()-2
progress_bars = [tqdm(total=int(meshshape/process_count), desc=f"Thread {i}") for i in range(process_count)]
for i in range(process_count):
    start_index = int(i*meshshape/process_count)
    end_index = int((i+1)*meshshape/process_count)
    p = multiprocessing.Process(target=simulate_trajectories, args=(start_index, end_index, str(i), progress_bars[i]))
    processes.append(p)
    p.start()
for p in processes:
    p.join()

# print(trajectories[:, :, 1])
trajectories = np.frombuffer(trajectories_shared.get_obj()).reshape((no_of_simulation_steps, 3, meshshape))
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
# 3d plot of the trajectories
for i in range(meshshape):
    ax.plot(trajectories[:,0,i], trajectories[:,1,i], trajectories[:,2,i], linewidth=1.7, alpha=0.3)  # Plot each trajectory
# plot starting points and ending points
ax.scatter(trajectories[0,0,:], trajectories[0,1,:], trajectories[0,2,:], c='y', s=10)
ax.scatter(trajectories[-1,0,:], trajectories[-1,1,:], trajectories[-1,2,:], c='g', s=10)
ax = drawGate(ax, points)
octahedron_points = defineOctahedron(cc, n_vect, gate_vectors, bwf_field_half_strength)
ax = drawOctahedron(ax,octahedron_points)

# Labels and title
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('3D Particle Trajectories')

# Show the plot
plt.show()
