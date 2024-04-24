import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Path

fig, ax = plt.subplots(figsize=(12, 6)) 



for i in range(0, 3):
    x = i / 2
    #ax.plot([x, x], [0.4875, 0.5125], color="black")
    circle = Circle((x, 0.5), 0.018, edgecolor="black", facecolor="none")
    ax.add_patch(circle)
    #ax.text(x, 0.54, rf"${i}$", ha="center", va="center", color="black", fontsize=10)


ax.text(0/2, 0.46, "No explanation", ha="center", va="center", color="black", fontsize=12)
ax.text(1/2, 0.46, "Short explanation", ha="center", va="center", color="black", fontsize=12)
ax.text(2/2, 0.46, "Detailed explanation", ha="center", va="center", color="black", fontsize=12)





ax.set_xlim(-0.25, 1.25)
ax.set_ylim(0.3, 0.55)
ax.set_aspect('equal')
ax.axis("off")  

plt.tight_layout()

plt.savefig('figure_ExplanationScale.png', dpi=600, bbox_inches='tight')

plt.show()