from collections import Counter
from copy import deepcopy
from itertools import combinations_with_replacement, permutations
import random
from tqdm import tqdm
import csp_random
import affichage


####################################################################################################
#                                                                                                  #
#   Auteurs : MEYNARD Lucien, REYNIER Damien                                                       #
#   Date : 20/03/2024                                                                              #
#                                                                                                  #
####################################################################################################

#   DESCRIPTION
#   -----------
#   Ce programme permet de trouver les combinaisons de bobines qui permettent de minimiser la perte de matière première
#   lors de la découpe de bobines pères en bobines fils.
#   Il prend en entrée les longueurs des bobines pères et des bobines fils, et retourne les combinaisons possibles
#   pour chaque bobine père, ainsi que les combinaisons qui minimisent la perte de matière première.

# TODO: Faire la resolutions des bobines restantes apres avoir trouvé les combinaisons optimales avec de la resolution linéaire au lieu de la resolution aléatoire

#   VARIABLES
#   ---------
#   LONGUEUR_BOBINE_PERE : liste des longueurs des bobines pères
#   LISTE_BOBINE_VOULUE : liste des longueurs des bobines fils

# single mode
# LONGUEUR_BOBINE_PERE = [180, 100]
# LISTE_BOBINE_VOULUE = [[800, 500, 100], [30, 45, 50]]

# multi mode
# LONGUEUR_BOBINE_PERE = [150, 100]
# LISTE_BOBINE_VOULUE = [[600, 700, 500], [30, 45, 50]]

# user mode
LONGUEUR_BOBINE_PERE = [100, 150, 160, 170, 180]
LISTE_BOBINE_VOULUE = [[100, 100, 100, 100, 100, 100, 100],
                       [2, 4, 6, 3, 5, 7, 8]]

TAILLE_LISTE_DECOUPEE = 0
ITERATION_MINIMISATION_PERTES = 10000
# si combinaisons > FACTORIELLE_MAX : échantillon aléatoire de NOMBRE_COMBINAISONS combinaisons
NOMBRE_COMBINAISONS = 1000
# 6! = 720      7! = 5.040      8! = 40.320      9! = 362.880      10! = 3.628.800
FACTORIELLE_MAX = 7


#   FONCTIONS
#   ---------
#   combinaisons(liste_pere, liste_fils) : retourne toutes les combinaisons possibles pour chaque père
#   perte_nulle() : retourne les patterns qui ne font pas perdre de matière première
#   perte_minimale(pattern, liste) : retourne le pattern qui fait perdre le moins de matière première avec les bobines restantes


def random_permutation(iterable):
    "Renvoie une permutation aléatoire de l'itérable"
    pool = tuple(iterable)
    r = list(range(len(pool)))
    random.shuffle(r)
    return [pool[i] for i in r]


def combinaisons(liste_pere, liste_fils):
    """
    Fonction qui retourne toutes les combinaisons possibles pour chaque père
    entree : 
        liste_pere : liste des longueurs des bobines pères
        liste_fils : liste des longueurs des bobines fils
    sortie : 
        tous_patterns : liste des combinaisons possibles pour chaque bobine père de la forme [[combinaison1, combinaison2, ...], [combinaison1, combinaison2, ...], ...]
    """
    tous_patterns = []
    patterns_pere = []

    for pere in liste_pere:
        if pere // min(liste_fils) + 1 > 15:
            for r in tqdm(range(1, 15), desc="Calcul des combinaisons", leave=False):
                for comb in combinations_with_replacement(liste_fils, r):
                    if sum(comb) == pere:
                        patterns_pere.append([comb, pere])
        else:
            for r in tqdm(range(1, pere // min(liste_fils) + 1), desc="Calcul des combinaisons", leave=False):
                for comb in combinations_with_replacement(liste_fils, r):
                    if sum(comb) == pere:
                        patterns_pere.append([comb, pere])
        tous_patterns.append(patterns_pere)

    tous_patterns = tous_patterns[0]
    if len(tous_patterns) > FACTORIELLE_MAX:
        liste_test = []

        for i in range(NOMBRE_COMBINAISONS):
            liste_test.append(random_permutation(tous_patterns))
        tous_patterns = liste_test
    else:
        tous_patterns = [list(permutation)
                         for permutation in permutations(tous_patterns)]
    return tous_patterns


def perte_nulle():
    """
    Fonction qui retourne les patterns qui ne font pas perdre de matière première
    entree : 
        None
    sortie : 
        pattern_perte_nulle : liste des patterns qui ne font pas perdre de matière première de la forme [[pattern, nombre de répétitions, longueur de la bobine père], ...]
        liste : liste des bobines restantes après utilisation des patterns
    """

    tous_patterns = combinaisons(
        LONGUEUR_BOBINE_PERE, LISTE_BOBINE_VOULUE[1])
    pattern_perte_nulle = []
    liste_finale = [LISTE_BOBINE_VOULUE[0], LISTE_BOBINE_VOULUE[1]]

    for comb in tqdm(tous_patterns, desc="Calcul des combinaisons", leave=False):

        liste = deepcopy(LISTE_BOBINE_VOULUE)

        pattern_perte_nulle_temp = []

        for patterns in comb:
            for pattern in patterns[:-1]:
                compteur = dict(Counter(pattern))
                iterateur = 0
                while all(liste[0][liste[1].index(element)] >= nombre for element, nombre in zip(compteur.keys(), compteur.values())):
                    iterateur += 1
                    for element, nombre in zip(compteur.keys(), compteur.values()):
                        liste[0][liste[1].index(element)] -= nombre

                if iterateur != 0:
                    pattern_perte_nulle_temp.append(
                        [pattern, iterateur, patterns[-1]])

        for i, restant in reversed(list(enumerate(liste[0]))):
            if restant == 0:
                liste[0].pop(i)
                liste[1].pop(i)
        if len(liste[0]) == 0:
            liste = None
            pattern_perte_nulle = pattern_perte_nulle_temp

            return pattern_perte_nulle, liste
        elif sum(liste[0]) <= sum(liste_finale[0]):
            liste_finale = liste
            pattern_perte_nulle = pattern_perte_nulle_temp
    return pattern_perte_nulle, liste_finale


def perte_minimale(pattern, liste):
    """
    Fonction qui retourne le pattern qui fait perdre le moins de matière première avec les bobines restantes
    entree : 
        pattern : liste des patterns qui ne font pas perdre de matière première
        liste : liste des bobines restantes après utilisation des patterns
    sortie :
        pattern : pattern final de la forme [[pattern, nombre de répétitions, longueur de la bobine père], ...]
    """

    pattern_random, pertes = csp_random.func_csp_random(LONGUEUR_BOBINE_PERE, liste,
                                                        TAILLE_LISTE_DECOUPEE, ITERATION_MINIMISATION_PERTES, False)
    pattern.extend(pattern_random)

    pertes = 0
    total = 0
    for i in pattern:
        pertes += i[-1][1]*i[-1][2]
        total += i[-1][0]*i[-1][2]
    coeff_pertes = 100 - abs(pertes - total) / total * 100
    affichage.affichage(pattern, coeff_pertes)


# PROGRAMME PRINCIPAL
# -------------------

LONGUEUR_BOBINE_PERE.sort()

# on verifie que toutes les tailles sont inférieures à la plus grande bobine pere
for i in LISTE_BOBINE_VOULUE[1]:
    if i > max(LONGUEUR_BOBINE_PERE):
        print(
            "Erreur, une des tailles demandées est supérieure à la plus grande bobine père")
        exit()

pattern, liste = perte_nulle()

pattern_affichage = []
mise_en_forme = []
for listes in pattern:
    mise_en_forme.extend(bobine for bobine in listes[0])
    mise_en_forme.append([listes[-1], 0, listes[-2]])
    pattern_affichage.append(mise_en_forme)
    mise_en_forme = []

if liste:
    perte_minimale(pattern_affichage, liste)
else:
    affichage.affichage(pattern_affichage, 0)
