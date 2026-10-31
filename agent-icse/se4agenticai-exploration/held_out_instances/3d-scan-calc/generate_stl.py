#!/usr/bin/env python3
"""Generate a held-out binary STL for mesh-analysis: a 10x10x5 cm steel box
(main part, material ID 10 = Standard Steel, density 7.85 g/cm^3) plus a tiny
debris tetrahedron (material ID 1 = Generic Debris) far away, so the
largest-connected-component filter has something real to filter out.
Coordinates are written directly in the pinned convention: centimeters.
"""
import os
import struct

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_data.stl")

# Box corners (cm): 10 x 10 x 5
c = [
    (0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0),
    (0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5),
]
box_faces = [
    (0, 2, 1), (0, 3, 2),  # bottom
    (4, 5, 6), (4, 6, 7),  # top
    (0, 1, 5), (0, 5, 4),  # front
    (3, 6, 2), (3, 7, 6),  # back
    (0, 4, 7), (0, 7, 3),  # left
    (1, 2, 6), (1, 6, 5),  # right
]
box_material_id = 10  # Standard Steel, density 7.85 g/cm^3

# Tiny debris tetrahedron far from the box, material 1 = Generic Debris
d = [
    (100.0, 100.0, 100.0),
    (100.1, 100.0, 100.0),
    (100.0, 100.1, 100.0),
    (100.0, 100.0, 100.1),
]
debris_faces = [
    (0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3),
]
debris_material_id = 1  # Generic Debris, density 0.10 g/cm^3


def signed_volume(vertices, faces):
    total = 0.0
    for f in faces:
        v1, v2, v3 = [vertices[i] for i in f]
        cp = (
            v2[1] * v3[2] - v2[2] * v3[1],
            v2[2] * v3[0] - v2[0] * v3[2],
            v2[0] * v3[1] - v2[1] * v3[0],
        )
        total += v1[0] * cp[0] + v1[1] * cp[1] + v1[2] * cp[2]
    return abs(total) / 6.0


box_vol = signed_volume(c, box_faces)
debris_vol = signed_volume(d, debris_faces)
print(f"Box volume: {box_vol} cm^3 (expected 500.0)")
print(f"Debris volume: {debris_vol} cm^3")
print(f"Expected main-part mass (cm convention): {box_vol * 7.85:.4f} g, material_id={box_material_id}")

triangles = []
for f in box_faces:
    v1, v2, v3 = [c[i] for i in f]
    triangles.append((v1, v2, v3, box_material_id))
for f in debris_faces:
    v1, v2, v3 = [d[i] for i in f]
    triangles.append((v1, v2, v3, debris_material_id))

with open(OUT, "wb") as f:
    f.write(b"\x00" * 80)  # header
    f.write(struct.pack("<I", len(triangles)))
    for v1, v2, v3, mat_id in triangles:
        normal = (0.0, 0.0, 0.0)  # unused by the oracle/verifier
        f.write(struct.pack("<3f", *normal))
        f.write(struct.pack("<3f", *v1))
        f.write(struct.pack("<3f", *v2))
        f.write(struct.pack("<3f", *v3))
        f.write(struct.pack("<H", mat_id))

print(f"Wrote {len(triangles)} triangles to {OUT}")
