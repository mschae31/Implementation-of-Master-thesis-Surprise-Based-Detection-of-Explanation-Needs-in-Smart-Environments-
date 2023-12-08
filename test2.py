import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Erstellen des Zeitstrahls
fig, ax = plt.subplots(figsize=(8, 1))
ax.set_xlim(1, 7)
ax.set_ylim(0, 1)

# Hinzufügen von Input- und Output-Punkten
ax.plot(2, 0.5, 'o', color='black', markerfacecolor='white', markersize=8, label='Input')
ax.plot(5, 0.5, 'o', color='black', markerfacecolor='white', markersize=8, label='Output')

# Hinzufügen des Strichs zwischen Input und Output
ax.plot([1, 7], [0.5, 0.5], color='black', linestyle='-', linewidth=2)

# Beschriften der Punkte
ax.text(2, 0.6, 'Input', ha='center', va='center', color='black')
ax.text(5, 0.6, 'Output', ha='center', va='center', color='black')

# Beschriften der Zeitschritte und Hinzufügen senkrechter Schritte
for t in range(1, 8):
    ax.text(t, -0.1, str(t), ha='center', va='center', color='black')

# Ausblenden der Achsen
ax.axis('off')

# Anzeigen des Plots
plt.show()
