import numpy as np
import math

def euler_from_matrix_zyx(R):
    # Extracts Euler angles (in degrees) for rotation order "ZYX"
    # R = Rz * Ry * Rx
    # R = [ [cy*cz, cz*sx*sy - cx*sz, cx*cz*sy + sx*sz],
    #       [cy*sz, cx*cz + sx*sy*sz, -cz*sx + cx*sy*sz],
    #       [-sy,   cy*sx,            cx*cy] ]
    sy = -R[2, 0]
    sy = max(-1.0, min(1.0, sy))
    ry = math.asin(sy)
    
    if abs(math.cos(ry)) > 1e-6:
        rx = math.atan2(R[2, 1], R[2, 2])
        rz = math.atan2(R[1, 0], R[0, 0])
    else:
        # Gimbal lock
        rx = math.atan2(-R[1, 2], R[1, 1])
        rz = 0.0
    return np.degrees([rx, ry, rz])

def rotation_matrix_zyx(rx_deg, ry_deg, rz_deg):
    rx = math.radians(rx_deg)
    ry = math.radians(ry_deg)
    rz = math.radians(rz_deg)
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(rx), -math.sin(rx)],
        [0, math.sin(rx), math.cos(rx)]
    ])
    Ry = np.array([
        [math.cos(ry), 0, math.sin(ry)],
        [0, 1, 0],
        [-math.sin(ry), 0, math.cos(ry)]
    ])
    Rz = np.array([
        [math.cos(rz), -math.sin(rz), 0],
        [math.sin(rz), math.cos(rz), 0],
        [0, 0, 1]
    ])
    return Rz @ Ry @ Rx

def solve_2bone_ik(shoulder, target_wrist, L1=6.0, L2=6.0, pole_hint=np.array([1, 0, 0])):
    # Shoulder to target vector
    D_vec = target_wrist - shoulder
    D = np.linalg.norm(D_vec)
    if D > (L1 + L2) * 0.999:
        D = (L1 + L2) * 0.999
        target_wrist = shoulder + (D_vec / np.linalg.norm(D_vec)) * D
        D_vec = target_wrist - shoulder
    
    # Cosine rule for elbow angle
    cos_alpha = (L1**2 + D**2 - L2**2) / (2 * L1 * D)
    cos_alpha = max(-1.0, min(1.0, cos_alpha))
    alpha = math.acos(cos_alpha)
    
    # Direction from shoulder to target
    d_dir = D_vec / D
    
    # Plane normal from pole hint
    pole_proj = pole_hint - np.dot(pole_hint, d_dir) * d_dir
    if np.linalg.norm(pole_proj) < 1e-4:
        pole_proj = np.array([0, 1, 0]) - np.dot(np.array([0, 1, 0]), d_dir) * d_dir
    pole_dir = pole_proj / np.linalg.norm(pole_proj)
    
    # Elbow position
    elbow = shoulder + d_dir * (L1 * math.cos(alpha)) + pole_dir * (L1 * math.sin(alpha))
    
    # Verify lengths
    assert abs(np.linalg.norm(elbow - shoulder) - L1) < 1e-4
    assert abs(np.linalg.norm(target_wrist - elbow) - L2) < 1e-4
    
    # Default unrotated bone vectors point along [0, -1, 0] (downward)
    v0 = np.array([0.0, -1.0, 0.0])
    
    # Upper arm orientation matrix R_upper
    v_upper = (elbow - shoulder) / L1
    # Rotation from v0 to v_upper:
    # Axis-angle
    axis_u = np.cross(v0, v_upper)
    if np.linalg.norm(axis_u) < 1e-6:
        R_upper = np.eye(3) if np.dot(v0, v_upper) > 0 else rotation_matrix_zyx(180, 0, 0)
    else:
        axis_u = axis_u / np.linalg.norm(axis_u)
        angle_u = math.acos(max(-1.0, min(1.0, np.dot(v0, v_upper))))
        # Rodrigues formula
        K = np.array([[0, -axis_u[2], axis_u[1]], [axis_u[2], 0, -axis_u[0]], [-axis_u[1], axis_u[0], 0]])
        R_upper = np.eye(3) + math.sin(angle_u) * K + (1 - math.cos(angle_u)) * (K @ K)
        
    # Forearm world orientation matrix R_forearm_world
    v_forearm = (target_wrist - elbow) / L2
    axis_f = np.cross(v0, v_forearm)
    if np.linalg.norm(axis_f) < 1e-6:
        R_forearm_world = np.eye(3) if np.dot(v0, v_forearm) > 0 else rotation_matrix_zyx(180, 0, 0)
    else:
        axis_f = axis_f / np.linalg.norm(axis_f)
        angle_f = math.acos(max(-1.0, min(1.0, np.dot(v0, v_forearm))))
        K_f = np.array([[0, -axis_f[2], axis_f[1]], [axis_f[2], 0, -axis_f[0]], [-axis_f[1], axis_f[0], 0]])
        R_forearm_world = np.eye(3) + math.sin(angle_f) * K_f + (1 - math.cos(angle_f)) * (K_f @ K_f)
        
    # Local forearm rotation: R_forearm_local = R_upper.T @ R_forearm_world
    R_forearm_local = R_upper.T @ R_forearm_world
    
    euler_upper = euler_from_matrix_zyx(R_upper)
    euler_forearm = euler_from_matrix_zyx(R_forearm_local)
    
    return {
        'elbow': elbow,
        'wrist': target_wrist,
        'euler_upper': euler_upper,
        'euler_forearm': euler_forearm,
        'R_upper': R_upper,
        'R_forearm_local': R_forearm_local
    }

print("IK Solver module ready.")
