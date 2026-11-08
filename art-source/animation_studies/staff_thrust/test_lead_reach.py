import numpy as np
import math

s_left = np.array([-4.8296, 22.0, 1.2941])

for z_grip in [-3.0, -3.5, -4.0]:
    for x_grip in [1.5, 2.0, 2.5]:
        P_lead = np.array([x_grip, 14.5, z_grip])
        # W_lead is roughly P_lead + [-0.8, -0.6, -0.2] normalized * 1.5
        v_offset = np.array([-0.8, -0.6, -0.2])
        v_offset = v_offset / np.linalg.norm(v_offset) * 1.5
        W_lead = P_lead + v_offset
        d = np.linalg.norm(W_lead - s_left)
        print(f"x={x_grip}, z={z_grip} -> Wrist: {W_lead.tolist()} -> Reach: {d:.3f} u")
