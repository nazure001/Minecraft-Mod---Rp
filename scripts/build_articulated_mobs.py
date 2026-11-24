import os
import json
import math
from PIL import Image, ImageDraw

REPO_ROOT = r"d:\repo\Minecraft Mod & Rp"
MOD_ENTITY_MODELS = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "models", "entity")
MOD_ENTITY_ANIMS = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "animations", "entity")
MOD_MOBS_TEX = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "textures", "entity", "mobs")
MOD_BOSS_TEX = os.path.join(REPO_ROOT, "mod", "src", "main", "resources", "assets", "avatar_elements", "textures", "entity", "boss")

STAGING_MODELS = os.path.join(REPO_ROOT, "art-source", "Avatar_Elements_Missing_Assets_Staging", "models", "entity")

# -----------------------------------------------------------------------------
# 1. PLATYPUS BEAR: GEOMETRY & ANIMATIONS
# -----------------------------------------------------------------------------

def build_platypus_bear_geo():
    bones = [
        {"name": "root", "pivot": [0, 14, 0], "parent": None},
        {
            "name": "body", "pivot": [0, 14, 0], "parent": "root", "rotation": [-5, 0, 0],
            "cubes": [
                {"origin": [-7.5, 8, -9], "size": [15, 13, 18], "uv": [0, 0]}, # main chest
                {"origin": [-8.5, 14, -10], "size": [17, 8, 12], "inflate": 0.5, "uv": [0, 68]} # heavy shoulder fur mantle
            ]
        },
        {
            "name": "neck", "pivot": [0, 16, -9], "parent": "body", "rotation": [-8, 0, 0],
            "cubes": [{"origin": [-5, 13, -14], "size": [10, 8, 7], "uv": [66, 0]}]
        },
        {
            "name": "head", "pivot": [0, 17, -14], "parent": "neck", "rotation": [12, 0, 0],
            "cubes": [{"origin": [-4.5, 14, -20], "size": [9, 8, 7], "uv": [66, 20]}]
        },
        {
            "name": "platypus_bill", "pivot": [0, 15, -20], "parent": "head", "rotation": [-4, 0, 0],
            "cubes": [{"origin": [-5, 14, -28], "size": [10, 2.5, 9], "uv": [66, 40]}] # flat duck bill
        },
        {
            "name": "jaw", "pivot": [0, 14, -18], "parent": "head", "rotation": [8, 0, 0],
            "cubes": [{"origin": [-4, 12, -26], "size": [8, 2, 8], "uv": [66, 56]}] # openable lower jaw
        },
        {
            "name": "ear_left", "pivot": [4, 21, -16], "parent": "head", "rotation": [0, 0, -20],
            "cubes": [{"origin": [3, 21, -17], "size": [2.5, 2.5, 1.5], "uv": [100, 0]}]
        },
        {
            "name": "ear_right", "pivot": [-4, 21, -16], "parent": "head", "rotation": [0, 0, 20],
            "cubes": [{"origin": [-5.5, 21, -17], "size": [2.5, 2.5, 1.5], "uv": [100, 8]}]
        },
        {
            "name": "body_back", "pivot": [0, 14, 5], "parent": "body", "rotation": [5, 0, 0],
            "cubes": [{"origin": [-7, 8, 5], "size": [14, 12, 10], "uv": [0, 36]}] # hindquarters
        },
        {
            "name": "tail_base", "pivot": [0, 13, 14], "parent": "body_back", "rotation": [-18, 0, 0],
            "cubes": [{"origin": [-6, 12, 14], "size": [12, 2.5, 6], "uv": [0, 92]}] # flat beaver tail seg 1
        },
        {
            "name": "tail_mid", "pivot": [0, 12.5, 20], "parent": "tail_base", "rotation": [8, 0, 0],
            "cubes": [{"origin": [-5.5, 12, 20], "size": [11, 2.2, 6], "uv": [0, 104]}] # seg 2
        },
        {
            "name": "tail_tip", "pivot": [0, 12, 26], "parent": "tail_mid", "rotation": [6, 0, 0],
            "cubes": [{"origin": [-4.5, 11.5, 26], "size": [9, 2.0, 7], "uv": [0, 116]}] # seg 3 paddle
        },
        # 4 Articulated Clawed Limbs
        {
            "name": "leg_front_left", "pivot": [6.5, 12, -6], "parent": "body", "rotation": [8, 0, -5],
            "cubes": [{"origin": [4.5, 6, -8], "size": [4.5, 7, 5], "uv": [112, 0]}]
        },
        {
            "name": "foot_front_left", "pivot": [6.5, 6, -6], "parent": "leg_front_left", "rotation": [-8, 0, 5],
            "cubes": [
                {"origin": [4, 0, -9], "size": [5.5, 6, 6], "uv": [112, 16]},
                {"origin": [4.2, 0, -12], "size": [5.0, 2, 3], "uv": [112, 32]} # claws
            ]
        },
        {
            "name": "leg_front_right", "pivot": [-6.5, 12, -6], "parent": "body", "rotation": [8, 0, 5],
            "cubes": [{"origin": [-9, 6, -8], "size": [4.5, 7, 5], "uv": [112, 0]}]
        },
        {
            "name": "foot_front_right", "pivot": [-6.5, 6, -6], "parent": "leg_front_right", "rotation": [-8, 0, -5],
            "cubes": [
                {"origin": [-9.5, 0, -9], "size": [5.5, 6, 6], "uv": [112, 16]},
                {"origin": [-9.2, 0, -12], "size": [5.0, 2, 3], "uv": [112, 32]} # claws
            ]
        },
        {
            "name": "leg_back_left", "pivot": [6.5, 12, 9], "parent": "body_back", "rotation": [-10, 0, -5],
            "cubes": [{"origin": [4.5, 6, 7], "size": [4.5, 7, 5.5], "uv": [112, 42]}]
        },
        {
            "name": "foot_back_left", "pivot": [6.5, 6, 9], "parent": "leg_back_left", "rotation": [10, 0, 5],
            "cubes": [
                {"origin": [4, 0, 6.5], "size": [5.5, 6, 6.5], "uv": [112, 58]},
                {"origin": [4.2, 0, 4.5], "size": [5.0, 2, 2.5], "uv": [112, 74]}
            ]
        },
        {
            "name": "leg_back_right", "pivot": [-6.5, 12, 9], "parent": "body_back", "rotation": [-10, 0, 5],
            "cubes": [{"origin": [-9, 6, 7], "size": [4.5, 7, 5.5], "uv": [112, 42]}]
        },
        {
            "name": "foot_back_right", "pivot": [-6.5, 6, 9], "parent": "leg_back_right", "rotation": [10, 0, -5],
            "cubes": [
                {"origin": [-9.5, 0, 6.5], "size": [5.5, 6, 6.5], "uv": [112, 58]},
                {"origin": [-9.2, 0, 4.5], "size": [5.0, 2, 2.5], "uv": [112, 74]}
            ]
        }
    ]
    
    geo = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.platypus_bear",
                    "texture_width": 256,
                    "texture_height": 256,
                    "visible_bounds_width": 4,
                    "visible_bounds_height": 3,
                    "visible_bounds_offset": [0, 1.5, 0]
                },
                "bones": bones
            }
        ]
    }
    return geo


def build_platypus_bear_animations():
    anims = {
        "format_version": "1.8.0",
        "animations": {
            "animation.platypus_bear.idle": {
                "loop": True,
                "animation_length": 3.0,
                "bones": {
                    "body": {
                        "position": {"0.0": [0, 0, 0], "1.5": [0, 0.4, 0], "3.0": [0, 0, 0]},
                        "rotation": {"0.0": [-5, 0, 0], "1.5": [-3, 0, 0], "3.0": [-5, 0, 0]}
                    },
                    "neck": {
                        "rotation": {"0.0": [-8, 0, 0], "1.5": [-12, 0, 0], "3.0": [-8, 0, 0]}
                    },
                    "head": {
                        "rotation": {"0.0": [12, 0, 0], "1.5": [8, 0, 0], "3.0": [12, 0, 0]}
                    },
                    "tail_base": {
                        "rotation": {"0.0": [-18, 0, 0], "1.0": [-18, 5, 0], "2.0": [-18, -5, 0], "3.0": [-18, 0, 0]}
                    },
                    "tail_mid": {
                        "rotation": {"0.0": [8, 0, 0], "1.0": [8, 8, 0], "2.0": [8, -8, 0], "3.0": [8, 0, 0]}
                    },
                    "tail_tip": {
                        "rotation": {"0.0": [6, 0, 0], "1.0": [6, 12, 0], "2.0": [6, -12, 0], "3.0": [6, 0, 0]}
                    }
                }
            },
            "animation.platypus_bear.walk": {
                "loop": True,
                "animation_length": 1.2,
                "bones": {
                    "body": {
                        "position": {"0.0": [0, 0, 0], "0.3": [0, -0.6, 0], "0.6": [0, 0, 0], "0.9": [0, -0.6, 0], "1.2": [0, 0, 0]},
                        "rotation": {"0.0": [-5, 0, 0], "0.3": [-5, 2, -2], "0.6": [-5, 0, 0], "0.9": [-5, -2, 2], "1.2": [-5, 0, 0]}
                    },
                    "leg_front_left": {
                        "rotation": {"0.0": [8, 0, -5], "0.3": [28, 0, -5], "0.6": [8, 0, -5], "0.9": [-15, 0, -5], "1.2": [8, 0, -5]}
                    },
                    "leg_front_right": {
                        "rotation": {"0.0": [8, 0, 5], "0.3": [-15, 0, 5], "0.6": [8, 0, 5], "0.9": [28, 0, 5], "1.2": [8, 0, 5]}
                    },
                    "leg_back_left": {
                        "rotation": {"0.0": [-10, 0, -5], "0.3": [-25, 0, -5], "0.6": [-10, 0, -5], "0.9": [15, 0, -5], "1.2": [-10, 0, -5]}
                    },
                    "leg_back_right": {
                        "rotation": {"0.0": [-10, 0, 5], "0.3": [15, 0, 5], "0.6": [-10, 0, 5], "0.9": [-25, 0, 5], "1.2": [-10, 0, 5]}
                    }
                }
            },
            "animation.platypus_bear.slam_attack": {
                "loop": False,
                "animation_length": 1.5,
                "bones": {
                    "body": {
                        "position": {"0.0": [0, 0, 0], "0.6": [0, 8, -4], "0.9": [0, -2, 0], "1.5": [0, 0, 0]},
                        "rotation": {"0.0": [-5, 0, 0], "0.6": [-45, 0, 0], "0.9": [10, 0, 0], "1.5": [-5, 0, 0]}
                    },
                    "jaw": {
                        "rotation": {"0.0": [8, 0, 0], "0.5": [35, 0, 0], "0.9": [8, 0, 0]}
                    },
                    "leg_front_left": {
                        "rotation": {"0.0": [8, 0, -5], "0.6": [-40, 0, -15], "0.9": [30, 0, -5], "1.5": [8, 0, -5]}
                    },
                    "leg_front_right": {
                        "rotation": {"0.0": [8, 0, 5], "0.6": [-40, 0, 15], "0.9": [30, 0, 5], "1.5": [8, 0, 5]}
                    }
                }
            }
        }
    }
    return anims


# -----------------------------------------------------------------------------
# 2. PHOENIX KING OZAI: GEOMETRY & ANIMATIONS
# -----------------------------------------------------------------------------

def build_phoenix_king_ozai_geo():
    bones = [
        {"name": "root", "pivot": [0, 12, 0], "parent": None},
        {
            "name": "waist", "pivot": [0, 12, 0], "parent": "root", "rotation": [0, 0, 0],
            "cubes": [{"origin": [-4, 11, -2.5], "size": [8, 4, 5], "uv": [0, 32]}]
        },
        {
            "name": "chest", "pivot": [0, 15, 0], "parent": "waist", "rotation": [-3, 0, 0],
            "cubes": [
                {"origin": [-4.5, 15, -3], "size": [9, 9, 6], "uv": [0, 44]}, # imperial dragon robe torso
                {"origin": [-5, 14, -3.2], "size": [10, 10, 6.4], "inflate": 0.25, "uv": [40, 44]} # outer silk sash
            ]
        },
        {
            "name": "neck", "pivot": [0, 24, 0], "parent": "chest", "rotation": [2, 0, 0],
            "cubes": [{"origin": [-2, 23.5, -2], "size": [4, 2, 4], "uv": [0, 64]}]
        },
        {
            "name": "head", "pivot": [0, 25, 0], "parent": "neck", "rotation": [3, 0, 0],
            "cubes": [
                {"origin": [-3.5, 25, -3.5], "size": [7, 7, 7], "uv": [0, 0]}, # face & skull
                {"origin": [-2, 24.5, -3.8], "size": [4, 3, 2], "uv": [0, 72]} # goatee beard
            ]
        },
        {
            "name": "topknot", "pivot": [0, 32, -0.5], "parent": "head", "rotation": [5, 0, 0],
            "cubes": [{"origin": [-1.5, 32, -2], "size": [3, 3, 3], "uv": [32, 0]}]
        },
        {
            "name": "crown_flame_trident", "pivot": [0, 33, -1], "parent": "topknot", "rotation": [8, 0, 0],
            "cubes": [
                {"origin": [-2, 33, -2], "size": [4, 4, 1.5], "uv": [48, 0]},
                {"origin": [-0.5, 36, -2], "size": [1, 3, 1.5], "uv": [48, 10]}, # center trident spike
                {"origin": [-2.2, 35, -2], "size": [0.8, 2.5, 1.5], "uv": [54, 10]}, # left spike
                {"origin": [1.4, 35, -2], "size": [0.8, 2.5, 1.5], "uv": [54, 10]}  # right spike
            ]
        },
        # Pauldrons
        {
            "name": "pauldron_left", "pivot": [4.5, 23, 0], "parent": "chest", "rotation": [0, 0, -18],
            "cubes": [{"origin": [4.5, 21, -3.5], "size": [4.5, 4.5, 7], "uv": [80, 0]}]
        },
        {
            "name": "pauldron_right", "pivot": [-4.5, 23, 0], "parent": "chest", "rotation": [0, 0, 18],
            "cubes": [{"origin": [-9, 21, -3.5], "size": [4.5, 4.5, 7], "uv": [80, 0]}]
        },
        # Flowing Robe Skirt (Cloth Articulation)
        {
            "name": "robe_skirt_front", "pivot": [0, 12, -2.5], "parent": "waist", "rotation": [-10, 0, 0],
            "cubes": [{"origin": [-4.5, 1, -2.8], "size": [9, 11, 1], "uv": [0, 80]}]
        },
        {
            "name": "robe_skirt_back", "pivot": [0, 12, 2.5], "parent": "waist", "rotation": [10, 0, 0],
            "cubes": [{"origin": [-4.5, 1, 1.8], "size": [9, 11, 1], "uv": [24, 80]}]
        },
        {
            "name": "robe_skirt_left", "pivot": [4, 12, 0], "parent": "waist", "rotation": [0, 0, -10],
            "cubes": [{"origin": [3.5, 1, -2.5], "size": [1, 11, 5], "uv": [48, 80]}]
        },
        {
            "name": "robe_skirt_right", "pivot": [-4, 12, 0], "parent": "waist", "rotation": [0, 0, 10],
            "cubes": [{"origin": [-4.5, 1, -2.5], "size": [1, 11, 5], "uv": [48, 80]}]
        },
        # Limbs with Fire Gauntlets
        {
            "name": "arm_left", "pivot": [5.5, 22, 0], "parent": "chest", "rotation": [12, 0, -8],
            "cubes": [{"origin": [5, 16, -2], "size": [3, 7, 4], "uv": [80, 20]}]
        },
        {
            "name": "forearm_left", "pivot": [6.5, 16, 0], "parent": "arm_left", "rotation": [-28, 0, -5],
            "cubes": [
                {"origin": [5, 9, -2], "size": [3, 7, 4], "uv": [80, 36]}, # arm
                {"origin": [4.8, 8.5, -2.2], "size": [3.4, 4.5, 4.4], "inflate": 0.2, "uv": [80, 52]} # gold bracer
            ]
        },
        {
            "name": "arm_right", "pivot": [-5.5, 22, 0], "parent": "chest", "rotation": [12, 0, 8],
            "cubes": [{"origin": [-8, 16, -2], "size": [3, 7, 4], "uv": [80, 20]}]
        },
        {
            "name": "forearm_right", "pivot": [-6.5, 16, 0], "parent": "arm_right", "rotation": [-28, 0, 5],
            "cubes": [
                {"origin": [-8, 9, -2], "size": [3, 7, 4], "uv": [80, 36]},
                {"origin": [-8.2, 8.5, -2.2], "size": [3.4, 4.5, 4.4], "inflate": 0.2, "uv": [80, 52]}
            ]
        },
        {
            "name": "leg_left", "pivot": [2.2, 12, 0], "parent": "waist", "rotation": [5, 0, -2],
            "cubes": [{"origin": [0.7, 5, -2], "size": [3.2, 7, 4], "uv": [100, 20]}]
        },
        {
            "name": "shin_left", "pivot": [2.2, 5, 0], "parent": "leg_left", "rotation": [-6, 0, 0],
            "cubes": [{"origin": [0.7, 0, -2], "size": [3.2, 5, 4], "uv": [100, 36]}]
        },
        {
            "name": "leg_right", "pivot": [-2.2, 12, 0], "parent": "waist", "rotation": [-8, 0, 2],
            "cubes": [{"origin": [-3.9, 5, -2], "size": [3.2, 7, 4], "uv": [100, 20]}]
        },
        {
            "name": "shin_right", "pivot": [-2.2, 5, 0], "parent": "leg_right", "rotation": [10, 0, 0],
            "cubes": [{"origin": [-3.9, 0, -2], "size": [3.2, 5, 4], "uv": [100, 36]}]
        }
    ]

    geo = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.phoenix_king_ozai",
                    "texture_width": 256,
                    "texture_height": 256,
                    "visible_bounds_width": 3,
                    "visible_bounds_height": 3,
                    "visible_bounds_offset": [0, 1.5, 0]
                },
                "bones": bones
            }
        ]
    }
    return geo


def build_phoenix_king_ozai_animations():
    anims = {
        "format_version": "1.8.0",
        "animations": {
            "animation.phoenix_king_ozai.idle": {
                "loop": True,
                "animation_length": 2.5,
                "bones": {
                    "chest": {
                        "position": {"0.0": [0, 0, 0], "1.25": [0, 0.3, 0], "2.5": [0, 0, 0]},
                        "rotation": {"0.0": [-3, 0, 0], "1.25": [-1, 0, 0], "2.5": [-3, 0, 0]}
                    },
                    "neck": {
                        "rotation": {"0.0": [2, 0, 0], "1.25": [0, 0, 0], "2.5": [2, 0, 0]}
                    },
                    "robe_skirt_front": {
                        "rotation": {"0.0": [-10, 0, 0], "1.25": [-14, 0, 0], "2.5": [-10, 0, 0]}
                    },
                    "robe_skirt_back": {
                        "rotation": {"0.0": [10, 0, 0], "1.25": [14, 0, 0], "2.5": [10, 0, 0]}
                    },
                    "forearm_left": {
                        "rotation": {"0.0": [-28, 0, -5], "1.25": [-32, 0, -5], "2.5": [-28, 0, -5]}
                    },
                    "forearm_right": {
                        "rotation": {"0.0": [-28, 0, 5], "1.25": [-32, 0, 5], "2.5": [-28, 0, 5]}
                    }
                }
            },
            "animation.phoenix_king_ozai.walk": {
                "loop": True,
                "animation_length": 1.0,
                "bones": {
                    "waist": {
                        "position": {"0.0": [0, 0, 0], "0.25": [0, -0.4, 0], "0.5": [0, 0, 0], "0.75": [0, -0.4, 0], "1.0": [0, 0, 0]},
                        "rotation": {"0.0": [0, 0, 0], "0.25": [0, 4, 0], "0.5": [0, 0, 0], "0.75": [0, -4, 0], "1.0": [0, 0, 0]}
                    },
                    "leg_left": {
                        "rotation": {"0.0": [5, 0, -2], "0.25": [30, 0, -2], "0.5": [5, 0, -2], "0.75": [-25, 0, -2], "1.0": [5, 0, -2]}
                    },
                    "leg_right": {
                        "rotation": {"0.0": [-8, 0, 2], "0.25": [-25, 0, 2], "0.5": [-8, 0, 2], "0.75": [30, 0, 2], "1.0": [-8, 0, 2]}
                    },
                    "arm_left": {
                        "rotation": {"0.0": [12, 0, -8], "0.5": [-20, 0, -8], "1.0": [12, 0, -8]}
                    },
                    "arm_right": {
                        "rotation": {"0.0": [12, 0, 8], "0.5": [35, 0, 8], "1.0": [12, 0, 8]}
                    }
                }
            },
            "animation.phoenix_king_ozai.lightning_strike": {
                "loop": False,
                "animation_length": 2.0,
                "bones": {
                    "chest": {
                        "rotation": {"0.0": [-3, 0, 0], "0.8": [-15, 25, 0], "1.2": [10, -20, 0], "2.0": [-3, 0, 0]}
                    },
                    "arm_left": {
                        "rotation": {"0.0": [12, 0, -8], "0.8": [-80, 30, 0], "1.2": [-40, -10, 0], "2.0": [12, 0, -8]}
                    },
                    "arm_right": {
                        "rotation": {"0.0": [12, 0, 8], "0.8": [-90, -45, 0], "1.2": [-95, 10, 0], "2.0": [12, 0, 8]}
                    }
                }
            }
        }
    }
    return anims


def deploy_articulated_mobs():
    print("="*70)
    print("DEPLOYING MULTI-BONE KINEMATIC RIGS & ANIMATIONS")
    print("="*70)

    # 1. Platypus Bear
    p_geo = build_platypus_bear_geo()
    p_anim = build_platypus_bear_animations()
    
    geo_path_p = os.path.join(MOD_ENTITY_MODELS, "platypus_bear.geo.json")
    with open(geo_path_p, "w", encoding="utf-8") as f:
        json.dump(p_geo, f, indent=2)
    with open(os.path.join(STAGING_MODELS, "platypus_bear.geo.json"), "w", encoding="utf-8") as f:
        json.dump(p_geo, f, indent=2)
    print(f"  -> Generated 21-bone platypus_bear.geo.json")

    anim_path_p = os.path.join(MOD_ENTITY_ANIMS, "platypus_bear.animation.json")
    with open(anim_path_p, "w", encoding="utf-8") as f:
        json.dump(p_anim, f, indent=2)
    print(f"  -> Generated 3-set platypus_bear.animation.json")

    # 2. Phoenix King Ozai
    o_geo = build_phoenix_king_ozai_geo()
    o_anim = build_phoenix_king_ozai_animations()

    geo_path_o = os.path.join(MOD_ENTITY_MODELS, "phoenix_king_ozai.geo.json")
    with open(geo_path_o, "w", encoding="utf-8") as f:
        json.dump(o_geo, f, indent=2)
    with open(os.path.join(STAGING_MODELS, "phoenix_king_ozai.geo.json"), "w", encoding="utf-8") as f:
        json.dump(o_geo, f, indent=2)
    print(f"  -> Generated 22-bone phoenix_king_ozai.geo.json")

    anim_path_o = os.path.join(MOD_ENTITY_ANIMS, "phoenix_king_ozai.animation.json")
    with open(anim_path_o, "w", encoding="utf-8") as f:
        json.dump(o_anim, f, indent=2)
    print(f"  -> Generated 3-set phoenix_king_ozai.animation.json")

    print("\n" + "="*70)
    print("DEPLOYMENT OF ARTICULATED RIGS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    deploy_articulated_mobs()
