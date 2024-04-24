import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle, Path

fig, ax = plt.subplots(figsize=(12, 6)) 



for i in range(0,7):
    ax.plot([0.018+(1/7)*i,(1/7)-0.019+(1/7)*i], [0.5, 0.5], color="black", linewidth=2)


#circle = Circle((-1/8, 0.5), 0.018, edgecolor="black", facecolor="none")
#ax.add_patch(circle)


for i in range(0, 8):
    x = i / 7
    #ax.plot([x, x], [0.4875, 0.5125], color="black")
    circle = Circle((x, 0.5), 0.018, edgecolor="black", facecolor="none")
    ax.add_patch(circle)
    ax.text(x, 0.54, rf"${i}$", ha="center", va="center", color="black", fontsize=10)


    
#ax.text(1/6, 0.46, "Slightly surprising", ha="center", va="center", color="black", fontsize=12)
#ax.text(4/6, 0.46, "Surprising", ha="center", va="center", color="black", fontsize=12)
ax.text(6/6, 0.46, "Very surprising", ha="center", va="center", color="black", fontsize=12)
ax.text(0/8, 0.46, "Not surprising", ha="center", va="center", color="black", fontsize=12)



ax.set_xlim(-0.018, 1.018)
ax.set_ylim(0.3, 0.55)
ax.set_aspect('equal')
ax.axis("off")  

plt.tight_layout()

#plt.savefig('figure_SurpriseScale.png', dpi=600, bbox_inches='tight')

plt.show()