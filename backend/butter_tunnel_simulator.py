import numpy as np
import itertools
import math
from bwf_utilities import checkPlaneSide, defineGate, drawGate, defineOctahedron, drawOctahedron, samplePointsInASphere, samplePointsInABox

rng = np.random.default_rng(12345)

class BtSimulator:
    
    def __init__(self, count):
        self.particle_count = count
        self.dt = 0.1
        self.positions = list(rng.random((self.particle_count, 3)) * (25 + 15) - 15)

        self.dist_type = "3d_euclidean"
        # self.dist_type = "2d_euclidean"
        # self.dist_type = "2d_manhattan"
        # self.dist_type = "2d_manhattan_mixed"
        self.butter_w_coeff_override = None
        self.slack_cost = 2000.0
        self.gate_outerside = 2.0 # width
        self.gate_innerside = 1.0 # width

        self.cc = np.array([0.0, 10.0, 0.0])
        self.n_vect = np.array([1.0, 0.0, 0.0]) # take from here

        _ , self.bounding_planes, _, _ = defineGate(self.cc, self.n_vect, self.gate_innerside, self.gate_outerside)

    def get_positions(self):
        return [{'x': float(p[0]), 'y': float(p[1]), 'z': float(p[2])} for p in self.positions]

    def step(self):
        new_positions = []
        for p in self.positions:
            new_positions.append(self.move(p))
        
        self.positions = new_positions
    
    def reset(self):
        self.positions = list(rng.random((self.particle_count, 3)) * (5 + 5) - 5)
    
    def move(self, cur_position: np.array) -> None:
        possible_directions = np.array(list(itertools.product((0, 1 * self.dt, -1 * self.dt), repeat=3)))
        direction_costs = np.zeros(possible_directions.shape[0])
        for index in range(0, possible_directions.shape[0]):
            new_position = cur_position + possible_directions[index]
            center_distance = 0.0
            post_center_distance = 0.0
            
            if(self.dist_type == "3d_euclidean"):
                center_distance = np.linalg.norm(new_position - self.cc)
            elif(self.dist_type == "2d_euclidean"):
                center_distance = np.sqrt((new_position[0] - self.cc[0])**2 + (new_position[2] - self.cc[2])**2)
            # elif(center_distance_type == "2d_manhattan"):
            #     center_distance = np.abs(p[0]-cc[0]) + np.abs(p[2]-cc[2])
            # elif(center_distance_type == "2d_manhattan_mixed"):
            #     center_distance = 1.5*np.abs(np.dot(n_vect.T, p-cc)) + np.abs(np.dot(gate_x_diag_vect.T, p-cc)) + np.abs(np.dot(gate_y_diag_vect.T, p-cc))

            post_center_distance = np.linalg.norm(new_position - self.cc)

            # if position_cost_enabled:
            direction_costs[index] += post_center_distance * post_center_distance * 0.5
            # butter_w_coeff = self.butter_w_coeff_override if self.butter_w_coeff_override is not None else 1.0/(1.0 + (center_distance/3.0)**12.0)
            butter_w_coeff = 1.0/(1.0 + (center_distance/3.0)**12.0)
            # butter_w_coeff = 1.0

            for plane in self.bounding_planes:
                plane_val = checkPlaneSide(plane, new_position) * checkPlaneSide(plane, self.cc) * butter_w_coeff
                if plane_val < 0:
                    direction_costs[index] += plane_val * plane_val * self.slack_cost
        
        return cur_position + possible_directions[np.argmin(direction_costs)] + (0.05 + 0.05) * rng.random((3,)) - 0.05
        # return cur_position + self.dt * possible_directions[np.argmin(direction_costs)]