from . import (
    properties,
    operations,
    panels,
)

__modules = [
    properties,
    operations,
    panels,
]


bl_info = {
    "name": "Bake Audio",
    "author": "Rohit Ramu <rohitramu@gmail.com>",
    "version": (1, 0, 2),
    "blender": (2, 80, 0),
    "category": "Tools",
    "location": "Scene properties -> Bake Audio",
    "description": "Bake audio into f-curves, split into frequency ranges.",
}


def register():
    for module in __modules:
        module.register()


def unregister():
    for module in reversed(__modules):
        module.unregister()


if __name__ == "__main__":
    register()
