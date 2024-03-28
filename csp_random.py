import random as rand
from tqdm import tqdm
import math as m
import copy
from collections import Counter
import affichage

### single mode ###

# VARIABLES DU PROBLEME
# decoupage de la liste de bobine en sous listes de longeueur TAILLE_LISTE_DECOUPEE  (0 pour aucun découpage)
TAILLE_LISTE_DECOUPEE = 0
# nombre d'itération pour minimiser les pertes c'est à dire le nombre de fois que la boucle va aleatoirement essayer de minimiser les pertes
ITERATION_MINIMISATION_PERTES = 10000


# single mode
# LONGUEUR_BOBINE_PERE = [180, 100]
# LISTE_BOBINE_VOULUE = [[800, 500, 100], [30, 45, 50]]

# multi mode
# LONGUEUR_BOBINE_PERE = [150, 100]
# LISTE_BOBINE_VOULUE = [[600, 700, 500], [30, 45, 50]]

# user mode
LONGUEUR_BOBINE_PERE = [150, 100, 160, 140, 83]
LISTE_BOBINE_VOULUE = [[600, 700, 500, 400, 140, 56], [30, 45, 50, 43, 67, 83]]

affichage_graphique = True


def func_csp_random(LONGUEUR_BOBINE_PERE, LISTE_BOBINE_VOULUE, TAILLE_LISTE_DECOUPEE, ITERATION_MINIMISATION_PERTES, affichage_graphique):

    total_nombre_bobine_voulue = sum(LISTE_BOBINE_VOULUE[0])

    # On verifie que la taille de la liste de découpe est bien inférieure à la somme des bobines voulues si ce n'est pas le cas on met la taille de la liste de découpe à la somme des bobines voulues
    if TAILLE_LISTE_DECOUPEE > total_nombre_bobine_voulue or TAILLE_LISTE_DECOUPEE == 0:
        TAILLE_LISTE_DECOUPEE = total_nombre_bobine_voulue

    # on verifie que toutes les tailles sont inférieures à la plus grande bobine pere
    for i in LISTE_BOBINE_VOULUE[1]:
        if i > max(LONGUEUR_BOBINE_PERE):
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
                LISTE_BOBINE_VOULUE, total_nombre_bobine_voulue, TAILLE_LISTE_DECOUPEE)
            pattern_aleatoire = []

            # j = 1 si la liste de bobine n'a pas été découpée, sinon j = le nombre de sous liste de bobine découpée
            for j in (range(m.ceil(total_nombre_bobine_voulue / TAILLE_LISTE_DECOUPEE))):

                liste = liste_complete[j]

                bobine_pere_aleatoire = rand.choice(LONGUEUR_BOBINE_PERE)
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
                        bobine_pere_aleatoire = rand.choice(
                            LONGUEUR_BOBINE_PERE)
                        taille_pere = [bobine_pere_aleatoire,
                                       bobine_pere_aleatoire]
                    else:
                        pattern_aleatoire.append(pattern_aleatoire_temp)
                        pattern_aleatoire[-1].append(taille_pere)
                        pattern_aleatoire_temp = []
                        while taille > taille_pere[1]:
                            bobine_pere_aleatoire = rand.choice(
                                LONGUEUR_BOBINE_PERE)
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
    if affichage_graphique:
        affichage.affichage(pattern_finaux, pertes)

    return pattern_finaux, pertes


if __name__ == "__main__":
    func_csp_random(LONGUEUR_BOBINE_PERE, LISTE_BOBINE_VOULUE,
                    TAILLE_LISTE_DECOUPEE, ITERATION_MINIMISATION_PERTES, affichage)
