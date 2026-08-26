import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
import pandas as pd

rules = {
    'a': 'a', 'b': 'bé', 'c': 'cé', 'd': 'dé', 'e': 'eu',
    'f': 'effe', 'g': 'gé', 'h': 'ache', 'i': 'i', 'j': 'ji',
    'k': 'ka', 'l': 'elle', 'm': 'emme', 'n': 'enne', 'o': 'o',
    'p': 'pé', 'q': 'cu', 'r': 'erre', 's': 'esse', 't': 'té',
    'u': 'u', 'v': 'vé', 'w': 'doublevé', 'x': 'ixe', 'y': 'igrec',
    'z': 'zède', 'é': 'é', 'è': 'è'
}

# The phonetic spellings only use a subset of letters + accents. 
# We should probably map 'é' and 'è' back to 'e' to keep a 26x26 matrix, 
# or just include them in the alphabet for a 28x28 matrix.
# The original code uses 'é' and 'è' as their own symbols. Let's keep them as their own symbols, 
# or actually, maybe the user wants 26x26. The prompt says "matrice d'adjacence 26x26 de l'alphabet".
# Let's map 'é' and 'è' to 'e' for the matrix to have 26 letters, OR maybe the alphabet is 26 letters 
# but the rules introduce 'é' and 'è'. Wait, rules map 'é' to 'é'. 
# If I map 'é'->'e', then rules['e'] -> 'eu' -> 'euu' etc.
# Let's just create the exact 26x26 if we ignore accents (treat them as 'e'), 
# but wait, the prompt says "matrice d'adjacence 26x26 de l'alphabet". Let's stick to the 26 base letters.
# To do that, I'll strip accents when computing the matrix.
def strip_accents(s):
    return s.replace('é', 'e').replace('è', 'e')

alphabet = "abcdefghijklmnopqrstuvwxyz"

# 1. Plot growth curves
plt.figure(figsize=(10, 6))
iterations = 15
for letter in alphabet:
    current = letter
    lengths = [len(current)]
    for _ in range(iterations):
        current = "".join(rules.get(char, char) for char in current)
        lengths.append(len(current))
    
    # Optional: Highlight a few specific curves
    if lengths[-1] == 1:
        plt.plot(range(iterations + 1), lengths, color='grey', alpha=0.3)
    elif lengths[-1] < 100:
        plt.plot(range(iterations + 1), lengths, color='blue', alpha=0.5)
    else:
        plt.plot(range(iterations + 1), lengths, color='red', alpha=0.7)

plt.yscale('log')
plt.title('Croissance de la longueur des chaînes (Échelle logarithmique)')
plt.xlabel('Itérations')
plt.ylabel('Longueur de la chaîne')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.savefig('growth_curves.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Heatmap of the transition matrix (26x26)
# Build matrix
matrix = np.zeros((26, 26), dtype=int)
for i, source in enumerate(alphabet):
    # Rule for the letter, but we strip accents to keep it in the 26x26 space
    target_str = strip_accents(rules[source])
    for char in target_str:
        if char in alphabet:
            j = alphabet.index(char)
            matrix[i, j] += 1

plt.figure(figsize=(12, 10))
sns.heatmap(matrix, xticklabels=list(alphabet), yticklabels=list(alphabet), 
            cmap="YlOrRd", annot=True, fmt="d", linewidths=.5)
plt.title("Matrice d'adjacence des transitions (26x26)")
plt.xlabel("Lettre de destination")
plt.ylabel("Lettre source")
plt.savefig('transition_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. NetworkX directed graph
# For the graph, let's keep the full nodes including accents for accuracy, or map to 26?
# The prompt says "Tu pourrais utiliser la bibliothèque NetworkX... Chaque lettre est un nœud... c a une flèche vers c et é".
# So the graph SHOULD include 'é' and 'è' since the prompt mentions "c a une flèche vers é".
G = nx.DiGraph()

# Nodes are all keys in the rules
all_chars = list(rules.keys())
for char in all_chars:
    G.add_node(char)

# Edges
for char, target_str in rules.items():
    for target_char in target_str:
        if G.has_edge(char, target_char):
            G[char][target_char]['weight'] += 1
        else:
            G.add_edge(char, target_char, weight=1)

plt.figure(figsize=(14, 14))
# Layout that might show structure well (spring or kamada_kawai)
pos = nx.kamada_kawai_layout(G)

# Find self-loops, sinks, etc for coloring
sinks = [n for n in G.nodes() if G.out_degree(n) == 1 and list(G.successors(n))[0] == n]

node_colors = []
for node in G.nodes():
    if node in sinks:
        node_colors.append('lightgreen') # Sinks
    else:
        node_colors.append('lightblue')

nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, edgecolors='black')
nx.draw_networkx_labels(G, pos, font_size=14, font_weight="bold")

# Draw edges with arrows
edges = G.edges()
weights = [G[u][v]['weight'] * 1.5 for u,v in edges]
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, 
                       connectionstyle="arc3,rad=0.1", width=weights)

plt.title("Graphe orienté des transitions phonétiques", size=16)
plt.axis('off')
plt.savefig('transition_graph.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualisations générées avec succès : growth_curves.png, transition_heatmap.png, transition_graph.png")
