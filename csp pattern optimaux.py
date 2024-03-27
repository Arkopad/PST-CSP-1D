from collections import Counter
from copy import deepcopy
from itertools import combinations_with_replacement, permutations

####################################################################################################
#                                                                                                  #
#   Auteurs : MEYNARD Lucien, REYNIER Damien                                                        #
#   Date : 20/03/2024                                                                               #
#                                                                                                  #
####################################################################################################

#   DESCRIPTION
#   -----------
#   Ce programme permet de trouver les combinaisons de bobines qui permettent de minimiser la perte de matière première
#   lors de la découpe de bobines pères en bobines fils.
#   Il prend en entrée les longueurs des bobines pères et des bobines fils, et retourne les combinaisons possibles
#   pour chaque bobine père, ainsi que les combinaisons qui minimisent la perte de matière première.


#   VARIABLES
#   ---------
#   LONGUEUR_BOBINE_PERE : liste des longueurs des bobines pères
#   LISTE_BOBINE_VOULUE : liste des longueurs des bobines fils

LONGUEUR_BOBINE_PERE = [180, 100]
LISTE_BOBINE_VOULUE = [[800, 500, 100], [30, 45, 50]]


#   FONCTIONS
#   ---------
#   combinaisons(liste_pere, liste_fils) : retourne toutes les combinaisons possibles pour chaque père
#   perte_nulle() : retourne les patterns qui ne font pas perdre de matière première
#   perte_minimale(pattern, liste) : retourne le pattern qui fait perdre le moins de matière première avec les bobines restantes

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
    for pere in liste_pere:
        patterns_pere = []
        for r in range(1, pere // min(liste_fils) + 1):
            for comb in combinations_with_replacement(liste_fils, r):
                if sum(comb) == pere:
                    patterns_pere.append(comb)
        tous_patterns.append(patterns_pere)

    combinaisons_tous_patterns = []
    for patterns in tous_patterns:
        combinaisons_tous_patterns.append(list(permutations(patterns)))
    print(tous_patterns, '\n', combinaisons_tous_patterns, '\n')

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
    liste = deepcopy(LISTE_BOBINE_VOULUE)
    pattern_perte_nulle = []
    tous_patterns = combinaisons(
        LONGUEUR_BOBINE_PERE, LISTE_BOBINE_VOULUE[1])

    for pere, patterns in zip(LONGUEUR_BOBINE_PERE, tous_patterns):
        for pattern in patterns:
            compteur = dict(Counter(pattern))
            iterateur = 0
            while all(liste[0][liste[1].index(element)] >= nombre for element, nombre in zip(compteur.keys(), compteur.values())):
                iterateur += 1
                for element, nombre in zip(compteur.keys(), compteur.values()):
                    liste[0][liste[1].index(element)] -= nombre

            if iterateur != 0:
                pattern_perte_nulle.append([pattern, iterateur, pere])

    for i, restant in reversed(list(enumerate(liste[0]))):
        if restant == 0:
            liste[0].pop(i)
            liste[1].pop(i)
    if len(liste[0]) == 0:
        liste = None

    print('Patterns qui ne font pas perdre de matière première :')
    for i in pattern_perte_nulle:
        print('Pattern:', i[0], '| Nombre de répétitions:',
              i[1], '| Longueur de la bobine père:', i[2])
    print('\nListe des bobines restantes à calculer:')
    print(liste)

    return pattern_perte_nulle, liste


def perte_minimale(pattern, liste):
    """
    Fonction qui retourne le pattern qui fait perdre le moins de matière première avec les bobines restantes
    entree : 
        pattern : liste des patterns qui ne font pas perdre de matière première
        liste : liste des bobines restantes après utilisation des patterns
    sortie :
        pattern : pattern final de la forme [[pattern, nombre de répétitions, longueur de la bobine père], ...]
    """
    return pattern


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
if liste:

    perte_minimale(pattern, liste)


# TODO : faire les combinaisons possibles de pertes nulles pour avoir celle qui minimise le nombre de bobines restantes
# TODO : faire les combinaisons possibles de pertes minimales pour avoir celle qui minimise la perte de matière première
