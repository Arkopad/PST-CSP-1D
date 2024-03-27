import random as rand
from tqdm import tqdm
import math as m
import copy
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as patches

### single mode ###

# VARIABLES DU PROBLEME
# decoupage de la liste de bobine en sous listes de longeueur TAILLE_LISTE_DECOUPEE  (0 pour aucun découpage)
TAILLE_LISTE_DECOUPEE = 0
# nombre d'itération pour minimiser les pertes c'est à dire le nombre de fois que la boucle va aleatoirement essayer de minimiser les pertes
ITERATION_MINIMISATION_PERTES = 30000

# longueur des bobines initiales en stock et qui vont être découpées
longueur_bobine_pere = [150, 100]
# [[nombre], [taille]] ; nombres de bobines que l'on veut obtenir et leur longueur
liste_bobine_voulu = [[600, 700, 500], [30, 45, 50]]
total_nombre_bobine_voulue = sum(liste_bobine_voulu[0])

# On verifie que la taille de la liste de découpe est bien inférieure à la somme des bobines voulues si ce n'est pas le cas on met la taille de la liste de découpe à la somme des bobines voulues
if TAILLE_LISTE_DECOUPEE > total_nombre_bobine_voulue or TAILLE_LISTE_DECOUPEE == 0:
    TAILLE_LISTE_DECOUPEE = total_nombre_bobine_voulue

# on verifie que toutes les tailles sont inférieures à la plus grande bobine pere
for i in liste_bobine_voulu[1]:
    if i > max(longueur_bobine_pere):
        print(
            "Erreur, une des tailles demandées est supérieure à la plus grande bobine père")
        exit()


# découpage du prolème
def decoupage_probleme(liste_bobine, total, taille):
    liste_bobine_coupee = []
    liste = copy.deepcopy(liste_bobine)
    # m.ceil retourne l'entier supérieur et permet de lancer la boucle le nombre de fois nécessaire
    for k in range(m.ceil(total / taille)):
        liste_bobine_coupee_temp = []

        # on découpe la liste de bobine en sous liste de longueur taille
        for decoupage in range(taille):
            # on vérifie que la liste de bobine n'est pas vide
            if any(nombre > 0 for i, nombre in enumerate(liste[0])):
                # on choisi aléatoirement une bobine dans la liste de bobine
                aleatoire = rand.randint(0, len(liste[0]) - 1)
                # on enlève la bobine choisie de la liste
                liste[0][aleatoire] -= 1
                # on ajoute la bobine choisie à la liste de bobine découpée
                liste_bobine_coupee_temp.append(liste[1][aleatoire])
                # si la bobine choisie est la derniere on supprime le nombre et la taille de la bobine de la liste
                if liste[0][aleatoire] == 0:
                    liste[0].pop(aleatoire)
                    liste[1].pop(aleatoire)
        liste_bobine_coupee.append(liste_bobine_coupee_temp)
    return liste_bobine_coupee


def calcul_pertes(liste):
    pertes = 0
    total = 0
    for i in liste:
        pertes += i[-1][1]
        total += i[-1][0]
    coeff_pertes = 100 - abs(pertes - total) / total * 100
    return coeff_pertes


# résolution aléatoire
def resolution_probleme(iterations):

    best_pattern_aleatoire = []

    # on lance la boucle iterations fois pour minimiser les pertes sur chaque sous liste
    coeff_pertes = 100

    for i in tqdm(range(iterations)):
        liste_complete = decoupage_probleme(
            liste_bobine_voulu, total_nombre_bobine_voulue, TAILLE_LISTE_DECOUPEE)
        pattern_aleatoire = []

        # j = 1 si la liste de bobine n'a pas été découpée, sinon j = le nombre de sous liste de bobine découpée
        for j in (range(m.ceil(total_nombre_bobine_voulue / TAILLE_LISTE_DECOUPEE))):

            liste = liste_complete[j]

            bobine_pere_aleatoire = rand.choice(longueur_bobine_pere)
            # liste qui aura la forme en soustrayant au 2e element les decoupes [longueur pere utilisé, pertes dans la découpe]
            taille_pere = [bobine_pere_aleatoire, bobine_pere_aleatoire]
            pattern_aleatoire_temp = []

            for k, taille in enumerate(liste):
                # on verifie qu'il reste de la place sur la bobine pere

                if taille < taille_pere[1]:
                    taille_pere[1] -= taille
                    pattern_aleatoire_temp.append(taille)
                    if k == len(liste) - 1:
                        pattern_aleatoire.append(pattern_aleatoire_temp)
                        pattern_aleatoire_temp = []
                        pattern_aleatoire[-1].append(taille_pere)
                elif taille == taille_pere[1]:
                    taille_pere[1] -= taille
                    pattern_aleatoire_temp.append(taille)
                    pattern_aleatoire.append(pattern_aleatoire_temp)
                    pattern_aleatoire_temp = []
                    pattern_aleatoire[-1].append(taille_pere)
                    bobine_pere_aleatoire = rand.choice(longueur_bobine_pere)
                    taille_pere = [bobine_pere_aleatoire,
                                   bobine_pere_aleatoire]
                else:
                    pattern_aleatoire.append(pattern_aleatoire_temp)
                    pattern_aleatoire[-1].append(taille_pere)
                    pattern_aleatoire_temp = []
                    while taille > taille_pere[1]:
                        bobine_pere_aleatoire = rand.choice(
                            longueur_bobine_pere)
                        taille_pere = [bobine_pere_aleatoire,
                                       bobine_pere_aleatoire]

                    taille_pere[1] -= taille
                    pattern_aleatoire_temp.append(taille)
                    if k == len(liste) - 1:
                        pattern_aleatoire.append(pattern_aleatoire_temp)
                        pattern_aleatoire_temp = []
                        pattern_aleatoire[-1].append(taille_pere)

            coeff_pertes_temp = calcul_pertes(pattern_aleatoire)
            if coeff_pertes_temp >= coeff_pertes:
                break

        coeff_pertes_temp = calcul_pertes(pattern_aleatoire)

        if coeff_pertes_temp < coeff_pertes:
            best_pattern_aleatoire = pattern_aleatoire
            coeff_pertes = coeff_pertes_temp

    return best_pattern_aleatoire, coeff_pertes


solution, pertes = resolution_probleme(ITERATION_MINIMISATION_PERTES)


solution_triee = [sorted(item[:-1], reverse=True) + item[-1:]
                  for item in solution]
solution_triee = [str(i) for i in solution_triee]
counts = Counter(solution_triee)

pattern_finaux = []
for item, count in counts.items():
    test = eval(item)
    test[-1].append(count)
    pattern_finaux.append(test)

print(pattern_finaux, '\npertes = ', round(pertes, 4), '%')


plt.close('all')
fig, ax = plt.subplots()
colors = ['red', 'blue', 'green', 'yellow',
          'purple', 'orange', 'pink', 'brown']
pattern_finaux.sort(key=lambda x: x[-1][0], reverse=True)
nombre_patterns = len(pattern_finaux)
longueur_bobine_max = max([pattern[-1][0] for pattern in pattern_finaux])


for i in range(nombre_patterns):
    longueur = 0
    for j, bobine in enumerate(pattern_finaux[i]):
        if type(bobine) == list and bobine[1] != 0:
            bobine = bobine[1]
            rectangle = patches.Rectangle(
                (longueur, i*15), bobine, 10, edgecolor='white', facecolor='black', linewidth=1.5)
            ax.add_patch(rectangle)
            plt.text(longueur + bobine / 2, i*15 + 5, bobine,
                     ha='center', va='center', color='white')
            longueur = bobine + longueur

        elif type(bobine) == int:
            color_index = j % len(colors)
            rectangle = patches.Rectangle(
                (longueur, i*15), bobine, 10, edgecolor='white', facecolor=colors[color_index], linewidth=1.5)
            ax.add_patch(rectangle)
            plt.text(longueur + bobine / 2, i*15 + 5,
                     bobine, ha='center', va='center')
            longueur = bobine + longueur
    plt.text(-5, i*15 + 5,
             f'{pattern_finaux[i][-1][0]}', ha='center', va='center', color='black')
    plt.text(longueur + 5, i*15 + 5,
             f'x{pattern_finaux[i][-1][2]}', ha='center', va='center', color='black')


plt.gca().axes.get_yaxis().set_visible(False)
plt.xticks(range(0, longueur_bobine_max + 1, longueur_bobine_max))
plt.ylim(0, nombre_patterns*15 - 5)
plt.xlim(0, longueur_bobine_max)
plt.title('Pertes = ' + str(round(pertes, 4)) + '%')

plt.show()
