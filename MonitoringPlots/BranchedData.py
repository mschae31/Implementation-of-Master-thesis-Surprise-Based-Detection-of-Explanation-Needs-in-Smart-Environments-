import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Path

#Create a data stream plot with branched data

fig, ax = plt.subplots(figsize=(12, 6))  


ax.plot([0, 1], [0.5, 0.5], color="black", linewidth=2)

for i in range(0, 7):
    x = i / 6
    ax.plot([x, x], [0.4875, 0.5125], color="black")
    ax.text(x, 0.53, str(f"$t_{i}$"), ha="center", va="center", color="black", fontsize=13)

circle = Circle((1/6, 0.5), 0.018, edgecolor="black", facecolor="none")
ax.add_patch(circle)
circle2 = Circle((3/6, 0.5), 0.018, edgecolor="black", facecolor="none")
ax.add_patch(circle2)
circle3 = Circle((4/6, 0.5), 0.018, edgecolor="black", facecolor="none")
ax.add_patch(circle3)
circle4 = Circle((6/6, 0.5), 0.018, edgecolor="black", facecolor="none")
ax.add_patch(circle4)

ax.text(1/6, 0.45, "$Input_{1}$", ha="center", va="center", color="black", fontsize=20)
ax.text(3/6, 0.45, "$Input_{2}$", ha="center", va="center", color="black", fontsize=20)
ax.text(4/6, 0.45, "$Output_{2}$", ha="center", va="center", color="black", fontsize=20)
ax.text(6/6, 0.45, "$Output_{1}$", ha="center", va="center", color="black", fontsize=20)


ax.set_xlim(-0.01, 1.03)
ax.set_ylim(0.3, 0.55)
ax.set_aspect('equal')
ax.axis("off")  

plt.tight_layout()

plt.savefig('figure6.png', dpi=600, bbox_inches='tight')

plt.show()