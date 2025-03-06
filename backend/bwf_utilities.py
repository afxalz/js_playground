import csv
import numpy as np

def getCsvData(filename):
    with open(filename, newline='\n') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        data = []
        for row in csvreader:
            for row in csvreader:
                data.append(row)
        return data

def makePlane(point, normal):
    d = -np.dot(point, normal)
    return np.array([normal[0], normal[1], normal[2], d])

def checkPlaneSide(plane, point):
    return np.dot(plane[:3], point) + plane[3]

def defineGate(center,normal_vector, gate_innerside, gate_outerside):
    cc = center
    n_vect = normal_vector
    n_vect = n_vect/np.linalg.norm(n_vect)
    z_vect = np.array([0,0,1])
    x_vect = np.cross(n_vect.T, z_vect.T).T
    points = np.empty(shape=(0,3),dtype=float)
    pointA = cc -gate_outerside/2*x_vect + gate_outerside/2*z_vect
    points = np.vstack([points, pointA])
    pointB = cc + gate_outerside/2*x_vect + gate_outerside/2*z_vect
    points = np.vstack([points, pointB])
    pointC = cc + gate_outerside/2*x_vect - gate_outerside/2*z_vect
    points = np.vstack([points, pointC])
    pointD = cc -gate_outerside/2*x_vect - gate_outerside/2*z_vect
    points = np.vstack([points, pointD])
    pointE = cc -gate_innerside/2*x_vect + gate_innerside/2*z_vect
    points = np.vstack([points, pointE])
    pointF = cc + gate_innerside/2*x_vect + gate_innerside/2*z_vect
    points = np.vstack([points, pointF])
    pointG = cc + gate_innerside/2*x_vect - gate_innerside/2*z_vect
    points = np.vstack([points, pointG])
    pointH = cc + -gate_innerside/2*x_vect - gate_innerside/2*z_vect
    points = np.vstack([points, pointH])
    gate_x_diag_vect = pointF - pointH
    gate_x_diag_vect = gate_x_diag_vect/np.linalg.norm(gate_x_diag_vect)
    gate_y_diag_vect = pointE - pointG
    gate_y_diag_vect = gate_y_diag_vect/np.linalg.norm(gate_y_diag_vect)
    gate_vectors = np.array([gate_x_diag_vect, gate_y_diag_vect, n_vect])

    bounding_planes = []
    plane1 = makePlane(pointE, z_vect)
    bounding_planes.append(plane1)
    plane2 = makePlane(pointE, x_vect)
    bounding_planes.append(plane2)
    plane3 = makePlane(pointG, z_vect)
    bounding_planes.append(plane3)
    plane4 = makePlane(pointG, x_vect)
    bounding_planes.append(plane4)
    mid_plane = makePlane(cc, n_vect)
    return points, bounding_planes, mid_plane, gate_vectors

def checkIfInsideTunnel(point, bounding_planes, center):
    for plane in bounding_planes:
        if checkPlaneSide(plane, point)*checkPlaneSide(plane, center) < 0:
            return False
    return True

def defineOctahedron(center, normal_vector, gate_vectors, bwf_field_half_strength):
    normal_vector = normal_vector/np.linalg.norm(normal_vector)
    gate_x_diag_vect = gate_vectors[0]
    gate_y_diag_vect = gate_vectors[1]
    octahedron_y_vect = np.cross(normal_vector.T, gate_x_diag_vect.T).T
    # octahedron_x_vect = np.cross(octahedron_y_vect.T, normal_vector.T).T
    octahedron_x_vect = np.cross(normal_vector.T, gate_y_diag_vect.T).T
    octahedron_points = np.empty(shape=(0,3),dtype=float)
    octahedron_points = np.vstack([octahedron_points, center + (bwf_field_half_strength/1.0)*octahedron_x_vect])
    octahedron_points = np.vstack([octahedron_points, center - (bwf_field_half_strength/1.0)*octahedron_x_vect])
    octahedron_points = np.vstack([octahedron_points, center + (bwf_field_half_strength/1.0)*octahedron_y_vect])
    octahedron_points = np.vstack([octahedron_points, center - (bwf_field_half_strength/1.0)*octahedron_y_vect])
    octahedron_points = np.vstack([octahedron_points, center + (bwf_field_half_strength/1.5)*normal_vector])
    octahedron_points = np.vstack([octahedron_points, center - (bwf_field_half_strength/1.5)*normal_vector])
    return octahedron_points

def drawOctahedron(ax,octahedron_points):
    ax.plot([octahedron_points[0,0],octahedron_points[2,0]], [octahedron_points[0,1],octahedron_points[2,1]], [octahedron_points[0,2],octahedron_points[2,2]], c='r', alpha=0.5)
    ax.plot([octahedron_points[2,0],octahedron_points[1,0]], [octahedron_points[2,1],octahedron_points[1,1]], [octahedron_points[2,2],octahedron_points[1,2]], c='r', alpha=0.5)
    ax.plot([octahedron_points[1,0],octahedron_points[3,0]], [octahedron_points[1,1],octahedron_points[3,1]], [octahedron_points[1,2],octahedron_points[3,2]], c='r', alpha=0.5)
    ax.plot([octahedron_points[3,0],octahedron_points[0,0]], [octahedron_points[3,1],octahedron_points[0,1]], [octahedron_points[3,2],octahedron_points[0,2]], c='r', alpha=0.5)
    ax.plot([octahedron_points[0,0],octahedron_points[4,0]], [octahedron_points[0,1],octahedron_points[4,1]], [octahedron_points[0,2],octahedron_points[4,2]], c='r', alpha=0.5)
    ax.plot([octahedron_points[1,0],octahedron_points[4,0]], [octahedron_points[1,1],octahedron_points[4,1]], [octahedron_points[1,2],octahedron_points[4,2]], c='r', alpha=0.5)
    ax.plot([octahedron_points[2,0],octahedron_points[4,0]], [octahedron_points[2,1],octahedron_points[4,1]], [octahedron_points[2,2],octahedron_points[4,2]], c='r', alpha=0.5)
    ax.plot([octahedron_points[3,0],octahedron_points[4,0]], [octahedron_points[3,1],octahedron_points[4,1]], [octahedron_points[3,2],octahedron_points[4,2]], c='r', alpha=0.5)

    return ax

def drawGate(ax, gate_points):
    ax.plot(gate_points[0:4, 0], gate_points[0:4, 1], gate_points[0:4, 2], c='g', linewidth=2)
    ax.plot([gate_points[3, 0], gate_points[0, 0]], [gate_points[3, 1], gate_points[0, 1]], [
            gate_points[3, 2], gate_points[0, 2]], c='g', linewidth=2)
    ax.plot(gate_points[4:8, 0], gate_points[4:8, 1],
            gate_points[4:8, 2], c='b', linewidth=2)
    ax.plot([gate_points[7, 0], gate_points[4, 0]], [gate_points[7, 1], gate_points[4, 1]], [
        gate_points[7, 2], gate_points[4, 2]], c='b', linewidth=2)
    return ax

def samplePointsInASphere(center, radius, no_of_samples):
    r = radius
    X = np.array([])
    Y = np.array([])
    Z = np.array([])
    xyz_samples = np.zeros((3,no_of_samples))
    while X.shape[0] < no_of_samples:
        x_sample_min = center[0] - r
        x_sample_max = center[0] + r
        y_sample_min = center[1] - r
        y_sample_max = center[1] + r
        z_sample_min = center[2] - r
        z_sample_max = center[2] + r
        x = np.random.uniform(x_sample_min, x_sample_max, no_of_samples)
        y = np.random.uniform(y_sample_min, y_sample_max, no_of_samples)
        z = np.random.uniform(z_sample_min, z_sample_max, no_of_samples)
        xyz_samples[0,:] = x
        xyz_samples[1,:] = y
        xyz_samples[2,:] = z
        dist = np.linalg.norm(np.subtract(xyz_samples,center.reshape(3,1)), axis=0)
        X = np.append(X, xyz_samples[0,dist<r])
        Y = np.append(Y, xyz_samples[1,dist<r])
        Z = np.append(Z, xyz_samples[2,dist<r])
    return X, Y, Z

def samplePointsInABox(center, dimensions, no_of_samples):
    sample = no_of_samples
    x_sample_min = center[0] - dimensions[0]
    x_sample_max = center[0] + dimensions[0]
    y_sample_min = center[1] - dimensions[1]
    y_sample_max = center[1] + dimensions[1]
    z_sample_min = center[2] - dimensions[2]
    z_sample_max = center[2] + dimensions[2]
    x = np.random.uniform(x_sample_min, x_sample_max, sample**3)
    y = np.random.uniform(y_sample_min, y_sample_max, sample**3)
    z = np.random.uniform(z_sample_min, z_sample_max, sample**3)
    X = x
    Y = y
    Z = z
    return X, Y, Z

def getBWF(bwf_a, bwf_b, x):
    return 1.0/(1.0 + (x/bwf_a)**bwf_b)

def getManhattanDistance(point, center, gate_vectors, a, b, c):
    center = center.reshape(3,1)
    dist = a*np.abs(np.dot(gate_vectors[2].T, point-center)) + b*np.abs(np.dot(gate_vectors[0].T, point-center)) + c*np.abs(np.dot(gate_vectors[1].T, point-center))
    return dist

