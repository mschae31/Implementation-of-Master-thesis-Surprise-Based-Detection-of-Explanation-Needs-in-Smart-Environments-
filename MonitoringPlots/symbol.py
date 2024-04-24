import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Path

#Create a symbol for architeture Figure in thesis

fig, ax = plt.subplots(figsize=(3, 1.5)) 


ax.plot([0, 1.2], [0.5, 0.5], color="black", linewidth=4)

for i in range(0, 3):
    x = i / 2
    ax.plot([x, x], [0.4875, 0.5125], color="black", linewidth=4)
    ax.text(x, 0.4, rf"$t_{i}$", ha="center", va="center", color="black", fontsize=20, fontweight='bold')
    
ax.text(0/2, 0.6, "...", ha="center", va="center", color="black", fontsize=30)
ax.text(1/2, 0.6, "...", ha="center", va="center", color="black", fontsize=30)
ax.text(2/2, 0.6, "...", ha="center", va="center", color="black", fontsize=30)




ax.set_xlim(-0.05, 1.15)
ax.set_ylim(0.4, 0.55)
ax.set_aspect('equal')
ax.axis("off")  

plt.tight_layout()

plt.savefig('figure_architecture_symbol.png', dpi=600, bbox_inches='tight', transparent=True)

plt.show()