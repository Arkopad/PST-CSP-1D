from itertools import combinations_with_replacement
from tqdm import tqdm
from ortools.linear_solver import pywraplp
import affichage
import random
import statistics as statitics


def combinaisons(liste_pere, liste_fils):
    """
    Fonction qui retourne toutes les combinaisons possibles pour chaque père
    entree : 
        liste_pere : liste des longueurs des bobines pères
        liste_fils : liste des longueurs des bobines fils
        TODO: ENLEVER TOUT LES DOUBLONS DE PATTERNS
    """
    combinaison_possibles = []
    for i, taille in enumerate(liste_pere):
        for r in range(1, 40):
            combinations = combinations_with_replacement(liste_fils, r)
            for combination in combinations:
                combinaison_possibles_temp = []
                if sum(combination) <= liste_pere[i]:
                    combinaison_possibles_temp.append(combination)
                    combinaison_possibles_temp.append(taille)
                    combinaison_possibles.append(combinaison_possibles_temp)

    representation_vectorielle = []
    for combination in combinaison_possibles:
        taille_pere = combination[1]
        combination = combination[0]

        representation_vectorielle_temp = []
        vector = [combination.count(length) for length in liste_fils]
        representation_vectorielle_temp.append(vector)
        representation_vectorielle_temp.append(taille_pere)
        representation_vectorielle.append(representation_vectorielle_temp)

    # On enlève les doublons en gardant uniquement le pattern avec la taille de bobine père la plus petite, les doublons etant les meme listes du premier item de chaque element de la liste representation_vectorielle

    dict_temp = {}
    for item in representation_vectorielle:
        key = str(item[0])
        if key not in dict_temp or item[1] < dict_temp[key][1]:
            dict_temp[key] = item
    liste_sans_doublons = list(dict_temp.values())
    representation_vectorielle = liste_sans_doublons

    dict_temp = {}
    for item in combinaison_possibles:
        key = str(item[0])
        if key not in dict_temp or item[1] < dict_temp[key][1]:
            dict_temp[key] = item
    liste_sans_doublons = list(dict_temp.values())
    combinaison_possibles = liste_sans_doublons

    return representation_vectorielle, combinaison_possibles


def prog_lineaire_or_tools(longueur_bobine_pere, liste_bobine_voulue):
    nombres_pieces = liste_bobine_voulue[0]
    taille_pieces = liste_bobine_voulue[1]
    representation_vectorielle, combinaison_possibles = combinaisons(
        longueur_bobine_pere, taille_pieces)

    # Create the solver
    # GLOP, CBC, CLP, SCIP, CP-SAT, SAT
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Define the decision variables
    n = len(combinaison_possibles)
    variables = []
    for i in range(1, n+1):
        variables.append(solver.IntVar(0, solver.infinity(), f'x{i}'))

    # Define the objective function
    objective = solver.Objective()
    for i in range(n):
        objective.SetCoefficient(variables[i], 1)
    objective.SetMinimization()

    # Define the constraints
    for i, piece in enumerate(nombres_pieces):
        total = solver.Sum(
            variables[j] * representation_vectorielle[j][0][i] for j in range(n))

        solver.Add(total == piece)

    # Solve the problem
    solver.Solve()

    # Print the solution

    liste_affichage = []
    for i, var in enumerate(variables):
        liste_temp = []
        if var.solution_value() != 0:
            for j, nbr in enumerate(representation_vectorielle[i][0]):
                for k in range(nbr):
                    liste_temp.append(liste_bobine_voulue[1][j])

            perte = representation_vectorielle[i][1] - sum(liste_temp)
            liste_temp.append(
                [representation_vectorielle[i][1], perte, int(var.solution_value())])
            liste_affichage.append(liste_temp)

    pertes = 0
    total = 0
    for i in liste_affichage:
        pertes += i[-1][1]*i[-1][2]
        total += i[-1][0]*i[-1][2]
    pertes_pourcent = 100 - abs(pertes - total) / total * 100
    # affichage.affichage(liste_affichage, pertes_pourcent)

    return pertes_pourcent, solver.wall_time() / 1000


if __name__ == "__main__":
    REPETITIONS = 1000
    TAILLE_LISTE_PERE = 3
    TAILLE_LISTE_FILS = 5

    PERTES = []
    TEMPS = []
    for k in tqdm(range(REPETITIONS)):
        liste_pere = []
        nombre_bobine_fils = []
        taille_bobine_fils = []

        for i in range(random.randint(2, TAILLE_LISTE_FILS)):
            nombre_bobine_fils.append(
                10*random.randint(10, 50))  # ENTRE 100 ET 500
            taille_bobine_fils.append(
                10*random.randint(1, 9))  # ENTRE 10 ET 90

        for j in range(random.randint(1, TAILLE_LISTE_PERE)):
            liste_pere.append(round(random.randint(max(
                taille_bobine_fils)/10, 3*max(taille_bobine_fils)/10))*10)  # ENTRE (10-90) ET (50-450)
        liste_pere = list(set(liste_pere))
        if len(taille_bobine_fils) != len(set(taille_bobine_fils)):
            taille_bobine_fils = list(set(taille_bobine_fils))
            nombre_bobine_fils = [nombre_bobine_fils[taille_bobine_fils.index(
                taille)] for taille in taille_bobine_fils]

        perte, temps_calcul = prog_lineaire_or_tools(
            liste_pere, [nombre_bobine_fils, taille_bobine_fils])
        TEMPS.append(temps_calcul)
        if perte != None:
            PERTES.append(perte)

    if PERTES != []:
        print(f' Nombre de solutions : {len(PERTES)}')
        print(f' Perte moyenne : {sum(PERTES)/ len(PERTES):.2f} %')
        print(f' Perte médiane : {statitics.median(PERTES):.2f} %')
        print(f' Temps moyen : {sum(TEMPS)/ len(TEMPS):.6f} s')
    else:
        print('Pas de solution')
