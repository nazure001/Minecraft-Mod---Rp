import json
import uuid
import os

OUTPUT_DIR = r"D:\repo\Minecraft Mod & Rp\art-source\animation_studies\staff_thrust"
BBMODEL_PATH = os.path.join(OUTPUT_DIR, "player_staff_thrust_neutral.bbmodel")

def new_uuid():
    return str(uuid.uuid4())

def make_faces(dx, dy, dz):
    # Generates all 6 faces for a box of dimensions dx, dy, dz
    # texture: False ensures Blockbench marks the face as rendered (not culled/null)
    return {
        "north": {"uv": [0, 0, dx, dy], "texture": False},
        "east":  {"uv": [0, 0, dz, dy], "texture": False},
        "south": {"uv": [0, 0, dx, dy], "texture": False},
        "west":  {"uv": [0, 0, dz, dy], "texture": False},
        "up":    {"uv": [0, 0, dx, dz], "texture": False},
        "down":  {"uv": [0, 0, dx, dz], "texture": False}
    }

# Cube UUIDs
cube_torso_id = new_uuid()
cube_head_id = new_uuid()
cube_ru_id = new_uuid()
cube_rf_id = new_uuid()
cube_lu_id = new_uuid()
cube_lf_id = new_uuid()
cube_rleg_id = new_uuid()
cube_lleg_id = new_uuid()

cube_staff_c1 = new_uuid()
cube_staff_c2 = new_uuid()
cube_staff_c3 = new_uuid()
cube_staff_c4 = new_uuid()
cube_staff_c5 = new_uuid()

# Bone group UUIDs
grp_torso_id = new_uuid()
grp_head_id = new_uuid()
grp_ru_id = new_uuid()
grp_rf_id = new_uuid()
grp_lu_id = new_uuid()
grp_lf_id = new_uuid()
grp_rleg_id = new_uuid()
grp_lleg_id = new_uuid()
grp_staff_id = new_uuid()

elements = [
    # 0. Torso: 8x12x4, from [-4, 12, -2] to [4, 24, 2]
    {
        "name": "torso",
        "box_uv": False,
        "uuid": cube_torso_id,
        "from": [-4, 12, -2],
        "to": [4, 24, 2],
        "origin": [0, 12, 0],
        "color": 2,
        "faces": make_faces(8, 12, 4)
    },
    # 1. Head: 8x8x8, from [-4, 24, -4] to [4, 32, 4]
    {
        "name": "head",
        "box_uv": False,
        "uuid": cube_head_id,
        "from": [-4, 24, -4],
        "to": [4, 32, 4],
        "origin": [0, 24, 0],
        "color": 1,
        "faces": make_faces(8, 8, 8)
    },
    # 2. Right Upper Arm: 4x6x4, from [4, 16, -2] to [8, 22, 2]
    {
        "name": "right_upper_arm",
        "box_uv": False,
        "uuid": cube_ru_id,
        "from": [4, 16, -2],
        "to": [8, 22, 2],
        "origin": [5, 22, 0],
        "color": 3,
        "faces": make_faces(4, 6, 4)
    },
    # 3. Right Forearm: 4x6x4, from [4, 10, -2] to [8, 16, 2]
    {
        "name": "right_forearm",
        "box_uv": False,
        "uuid": cube_rf_id,
        "from": [4, 10, -2],
        "to": [8, 16, 2],
        "origin": [5, 16, 0],
        "color": 4,
        "faces": make_faces(4, 6, 4)
    },
    # 4. Left Upper Arm: 4x6x4, from [-8, 16, -2] to [-4, 22, 2]
    {
        "name": "left_upper_arm",
        "box_uv": False,
        "uuid": cube_lu_id,
        "from": [-8, 16, -2],
        "to": [-4, 22, 2],
        "origin": [-5, 22, 0],
        "color": 3,
        "faces": make_faces(4, 6, 4)
    },
    # 5. Left Forearm: 4x6x4, from [-8, 10, -2] to [-4, 16, 2]
    {
        "name": "left_forearm",
        "box_uv": False,
        "uuid": cube_lf_id,
        "from": [-8, 10, -2],
        "to": [-4, 16, 2],
        "origin": [-5, 16, 0],
        "color": 4,
        "faces": make_faces(4, 6, 4)
    },
    # 6. Right Leg: 4x12x4, from [0, 0, -2] to [4, 12, 2]
    {
        "name": "right_leg",
        "box_uv": False,
        "uuid": cube_rleg_id,
        "from": [0, 0, -2],
        "to": [4, 12, 2],
        "origin": [2, 12, 0],
        "color": 7,
        "faces": make_faces(4, 12, 4)
    },
    # 7. Left Leg: 4x12x4, from [-4, 0, -2] to [0, 12, 2]
    {
        "name": "left_leg",
        "box_uv": False,
        "uuid": cube_lleg_id,
        "from": [-4, 0, -2],
        "to": [0, 12, 2],
        "origin": [-2, 12, 0],
        "color": 7,
        "faces": make_faces(4, 12, 4)
    },
    # 8. Staff Lower Cap: 2x1x2, from [5.5, 0, -1] to [7.5, 1, 1]
    {
        "name": "staff_lower_cap",
        "box_uv": False,
        "uuid": cube_staff_c1,
        "from": [5.5, 0, -1],
        "to": [7.5, 1, 1],
        "origin": [6.5, 0, 0],
        "color": 0,
        "faces": make_faces(2, 1, 2)
    },
    # 9. Staff Lower Shaft: 1.5x11x1.5, from [5.75, 1, -0.75] to [7.25, 12, 0.75]
    {
        "name": "staff_lower_shaft",
        "box_uv": False,
        "uuid": cube_staff_c2,
        "from": [5.75, 1, -0.75],
        "to": [7.25, 12, 0.75],
        "origin": [6.5, 0, 0],
        "color": 8,
        "faces": make_faces(1.5, 11, 1.5)
    },
    # 10. Staff Grip Wrap: 2x6x2, from [5.5, 12, -1] to [7.5, 18, 1]
    {
        "name": "staff_grip_wrap",
        "box_uv": False,
        "uuid": cube_staff_c3,
        "from": [5.5, 12, -1],
        "to": [7.5, 18, 1],
        "origin": [6.5, 0, 0],
        "color": 5,
        "faces": make_faces(2, 6, 2)
    },
    # 11. Staff Upper Shaft: 1.5x11x1.5, from [5.75, 18, -0.75] to [7.25, 29, 0.75]
    {
        "name": "staff_upper_shaft",
        "box_uv": False,
        "uuid": cube_staff_c4,
        "from": [5.75, 18, -0.75],
        "to": [7.25, 29, 0.75],
        "origin": [6.5, 0, 0],
        "color": 8,
        "faces": make_faces(1.5, 11, 1.5)
    },
    # 12. Staff Upper Cap: 2x1x2, from [5.5, 29, -1] to [7.5, 30, 1]
    {
        "name": "staff_upper_cap",
        "box_uv": False,
        "uuid": cube_staff_c5,
        "from": [5.5, 29, -1],
        "to": [7.5, 30, 1],
        "origin": [6.5, 0, 0],
        "color": 0,
        "faces": make_faces(2, 1, 2)
    }
]

# Proper Blockbench Outliner Tree with strictly nested Bone Groups and Cube references:
outliner = [
    {
        "name": "torso",
        "uuid": grp_torso_id,
        "origin": [0, 12, 0],
        "rotation": [0, 0, 0],
        "children": [
            cube_torso_id,
            {
                "name": "head",
                "uuid": grp_head_id,
                "origin": [0, 24, 0],
                "rotation": [0, 0, 0],
                "children": [cube_head_id]
            },
            {
                "name": "right_upper_arm",
                "uuid": grp_ru_id,
                "origin": [5, 22, 0],
                "rotation": [0, 0, 0],
                "children": [
                    cube_ru_id,
                    {
                        "name": "right_forearm",
                        "uuid": grp_rf_id,
                        "origin": [5, 16, 0],
                        "rotation": [0, 0, 0],
                        "children": [cube_rf_id]
                    }
                ]
            },
            {
                "name": "left_upper_arm",
                "uuid": grp_lu_id,
                "origin": [-5, 22, 0],
                "rotation": [0, 0, 0],
                "children": [
                    cube_lu_id,
                    {
                        "name": "left_forearm",
                        "uuid": grp_lf_id,
                        "origin": [-5, 16, 0],
                        "rotation": [0, 0, 0],
                        "children": [cube_lf_id]
                    }
                ]
            }
        ]
    },
    {
        "name": "right_leg",
        "uuid": grp_rleg_id,
        "origin": [2, 12, 0],
        "rotation": [0, 0, 0],
        "children": [cube_rleg_id]
    },
    {
        "name": "left_leg",
        "uuid": grp_lleg_id,
        "origin": [-2, 12, 0],
        "rotation": [0, 0, 0],
        "children": [cube_lleg_id]
    },
    {
        "name": "staff_assembly",
        "uuid": grp_staff_id,
        "origin": [6.5, 0, 0],
        "rotation": [0, 0, 0],
        "children": [
            cube_staff_c1,
            cube_staff_c2,
            cube_staff_c3,
            cube_staff_c4,
            cube_staff_c5
        ]
    }
]

bb_model = {
    "meta": {
        "format_version": "4.10",
        "creation_time": 1730978000,
        "model_format": "modded_entity",
        "box_uv": False
    },
    "name": "player_staff_thrust_neutral",
    "geometry_name": "player_staff_thrust",
    "visible_box": [2, 3, 2],
    "resolution": {"width": 64, "height": 64},
    "elements": elements,
    "outliner": outliner,
    "animations": []
}

with open(BBMODEL_PATH, "w", encoding="utf-8") as f:
    json.dump(bb_model, f, indent=2)

print(f"Generated clean neutral model: {BBMODEL_PATH}")
