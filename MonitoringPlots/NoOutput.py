import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Path

#Create a data stream plot with no outputs

fig, ax = plt.subplots(figsize=(12, 6))  


ax.plot([0, 1], [0.5, 0.5], color="black", linewidth=2)

for i in range(0, 7):
    x = i / 6
    ax.plot([x, x], [0.4875, 0.5125], color="black")
    ax.text(x, 0.53, str(f"$t_{i}$"), ha="center", va="center", color="black", fontsize=13)


circle = Circle((1/6, 0.5), 0.018, edgecolor="black", facecolor="none")
ax.add_patch(circle)

ax.text(1/6, 0.45, "Input", ha="center", va="center", color="black", fontsize=20)


#ax.text(0.5, 0.8, "No Output", ha="center", va="center", color="black", fontsize=18, style='italic')

arrow = plt.Arrow(1.05, 0.5, 0.1, 0, width=0.02, color="black")
ax.add_patch(arrow)

#ax.text(1.15, 0.5, "(Input,.)", ha="left", va="center", color="black", fontsize=12)

ax.set_xlim(-0.01, 1.01)
ax.set_ylim(0.4, 0.55)
ax.set_aspect('equal')
ax.axis("off")  

plt.tight_layout()

#plt.savefig('figure5.png', dpi=600, bbox_inches='tight')

plt.show()