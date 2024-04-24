import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Path

#Create a data stream plot for user input data

fig, ax = plt.subplots(figsize=(12, 6)) 


ax.plot([0, 1.5], [0.5, 0.5], color="black", linewidth=2)

for i in range(0, 8):
    x = i / 7
    ax.plot([x, x], [0.4875, 0.5125], color="black")
    ax.text(x, 0.46, rf"$t_{i}$", ha="center", va="center", color="black", fontsize=13)
    
ax.text(1/7, 0.53, "(Switching power on)", ha="center", va="center", color="black", fontsize=12)
ax.text(3/7, 0.53, "(Pressing button to start)", ha="center", va="center", color="black", fontsize=12)
ax.text(4/7, 0.53, "(Waiting)", ha="center", va="center", color="black", fontsize=12)
ax.text(5/7, 0.53, "(Waiting)", ha="center", va="center", color="black", fontsize=12)
ax.text(6/7, 0.53, "(Waiting)", ha="center", va="center", color="black", fontsize=12)




ax.set_xlim(-0.05, 1.15)
ax.set_ylim(0.3, 0.55)
ax.set_aspect('equal')
ax.axis("off")  

plt.tight_layout()

plt.savefig('figure_RawDataUser.png', dpi=600, bbox_inches='tight')

plt.show()