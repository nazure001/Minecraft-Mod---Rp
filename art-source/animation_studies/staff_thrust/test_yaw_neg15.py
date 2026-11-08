import numpy as np
import math

from solve_ready_pose_ik import rotation_matrix_zyx

R_torso = rotation_matrix_zyx(0, -15, 0)
torso_pivot = np.array([0.0, 12.0, 0.0])

s_ru_local = np.array([5.0, 10.0, 0.0])
s_lu_local = np.array([-5.0, 10.0, 0.0])

s_right = torso_pivot + R_torso @ s_ru_local
s_left  = torso_pivot + R_torso @ s_lu_local

print(f"Right Shoulder World: {s_right.tolist()}")
print(f"Left Shoulder World : {s_left.tolist()}")

# Lead hand at [1.5, 14.5, -4.5], offset [-0.8, -0.6, -0.2] * 1.5:
W_lead = np.array([1.5, 14.5, -4.5]) + np.array([-0.8, -0.6, -0.2]) / math.sqrt(1.04) * 1.5
d_lead = np.linalg.norm(W_lead - s_left)
print(f"Lead Wrist: {W_lead.tolist()} -> Reach: {d_lead:.3f} u (Max: 12.0u)")

# Rear hand at [4.8, 12.5, 0.5], offset [0.9, -0.1, 0.4] * 1.5:
W_rear = np.array([4.8, 12.5, 0.5]) + np.array([0.9, -0.1, 0.4]) / math.sqrt(0.98) * 1.5
d_rear = np.linalg.norm(W_rear - s_right)
print(f"Rear Wrist: {W_rear.tolist()} -> Reach: {d_rear:.3f} u (Max: 12.0u)")
