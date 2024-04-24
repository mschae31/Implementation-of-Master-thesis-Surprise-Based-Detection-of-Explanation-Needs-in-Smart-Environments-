import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Path

#Create a data stream plot with one input and output

fig, ax = plt.subplots(figsize=(12, 6)) 


ax.plot([0, 1], [0.5, 0.5], color="black", linewidth=2)

for i in range(0, 7):
    x = i / 6
    ax.plot([x, x], [0.4875, 0.5125], color="black")
    ax.text(x, 0.53, str(f"$t_{i}$"), ha="center", va="center", color="black", fontsize=13)

circle = Circle((1/6, 0.5), 0.018, edgecolor="black", facecolor="none")
ax.add_patch(circle)
circle2 = Circle((5/6, 0.5), 0.018, edgecolor="black", facecolor="none")
ax.add_patch(circle2)

ax.text(1/6, 0.45, "Input", ha="center", va="center", color="black", fontsize=20)
ax.text(5/6, 0.45, "Output", ha="center", va="center", color="black", fontsize=20)

path_data = [
    (Path.MOVETO, [5/6 , 0.425]),
    (Path.CURVE3, [3/6 , 0.35]),
    (Path.CURVE3, [1/6, 0.425]),
]

codes, verts = zip(*path_data)
path = Path(verts, codes)

patch = PathPatch(path, facecolor="none", edgecolor="black", linewidth=2)
ax.add_patch(patch)


arrow = plt.Arrow(1.05, 0.5, 0.1, 0, width=0.02, color="black")
ax.add_patch(arrow)


ax.set_xlim(-0.01, 1.01)
ax.set_ylim(0.3, 0.55)
ax.set_aspect('equal')
ax.axis("off")  

plt.tight_layout()

plt.savefig('figure1.png', dpi=600, bbox_inches='tight', transparent=True)

plt.show()