from pulp import *
import itertools

LONGUEUR_BOBINE_PERE = [180, 100]
LISTE_BOBINE_VOULUE = [[30, 45, 50], [800, 500, 100]]

def best_first_decreasing(lengths, max_length):
    sorted_lengths = sorted(lengths, reverse=True)
    patterns = []
    while sorted_lengths:
        pattern = []
        remaining = max_length
        for length in sorted_lengths[:]:
            if length <= remaining:
                pattern.append(length)
                remaining -= length
                sorted_lengths.remove(length)
        patterns.append(pattern)
    return patterns

# Utiliser l'heuristique BFD pour générer les motifs
motifs = []
for i in range(len(LONGUEUR_BOBINE_PERE)):
    motifs.extend(best_first_decreasing(LISTE_BOBINE_VOULUE[0], LONGUEUR_BOBINE_PERE[i]))

# Définir le problème
prob = LpProblem("Cutting Stock Problem", LpMinimize)

# Définir les variables
x = LpVariable.dicts("x", range(len(motifs)), 0, None, LpInteger)

# Définir la fonction objectif
prob += lpSum(x[i] for i in range(len(motifs)))

# Ajouter les contraintes
for j in range(len(LISTE_BOBINE_VOULUE[0])):
    prob += lpSum(x[i] for i in range(len(motifs)) if LISTE_BOBINE_VOULUE[0][j] in motifs[i][1]) >= LISTE_BOBINE_VOULUE[1][j]

# Résoudre le problème
prob.solve()

# Afficher les résultats
for i in range(len(motifs)):
    if x[i].varValue > 0:
        print(f"Motif {motifs[i][1]} utilisé {x[i].varValue} fois sur bobine père de longueur {LONGUEUR_BOBINE_PERE[motifs[i][0]]}")