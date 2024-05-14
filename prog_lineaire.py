from itertools import combinations_with_replacement
from tqdm import tqdm
import pulp
import affichage


def combinaisons(liste_pere, liste_fils):
    """
    Fonction qui retourne toutes les combinaisons possibles pour chaque père
    entree : 
        liste_pere : liste des longueurs des bobines pères
        liste_fils : liste des longueurs des bobines fils
    TODO : PENSER A FAIRE UN FOR POUR TOUTES LES BOBINES PERES    
    """
    combinaison_possibles = []
    for r in range(1, len(liste_fils) + 1):
        combinations = combinations_with_replacement(liste_fils, r)
        for combination in combinations:
            if sum(combination) <= liste_pere[0]:
                combinaison_possibles.append(combination)

    representation_vectorielle = []
    for combination in combinaison_possibles:
        vector = [combination.count(length) for length in liste_fils]
        representation_vectorielle.append(vector)
    return representation_vectorielle, combinaison_possibles


def prog_lineaire_pulp(longueur_bobine_pere, liste_bobine_voulue):
    nombres_pieces = liste_bobine_voulue[0]
    taille_pieces = liste_bobine_voulue[1]
    representation_vectorielle, combinaison_possibles = combinaisons(longueur_bobine_pere, taille_pieces)
    

    # Create the LP problem
    problem = pulp.LpProblem("Linear_Programming_Problem", pulp.LpMinimize)

    # Define the decision variables
    n = len(combinaison_possibles)
    variables = []
    for i in range(1, n+1):
        variables.append(pulp.LpVariable(f"x{i}", lowBound=0, cat='Integer'))

    # Define the objective function
    objective = pulp.LpAffineExpression([(variables[i], 1) for i in range(n)])
    problem += objective

    # Define the constraints
    for i, piece in enumerate(nombres_pieces):
        total = 0
        for j, var in enumerate(variables):

            coeff = representation_vectorielle[j]

            total += pulp.LpAffineExpression([(var, coeff[i])])

        problem += total == piece

    # Solve the problem
    problem.solve()

    # Print the solution
    if problem.status == pulp.LpStatusOptimal:
        print("Solution:")
        print("x0 =", pulp.value(problem.objective))
        for i, var in enumerate(variables):
            print(f"x{i+1} =", pulp.value(var))
        print(representation_vectorielle)

    else:
        print("The problem does not have an optimal solution.")

    # # affichage graphique (FAIRE LE TODO AVANT)
    # pattern_affichage = []
    # for i, var in enumerate(variables):
    #     if pulp.value(var) != 0:
    #         pattern_affichage.append()



if __name__ == "__main__":
    prog_lineaire_pulp([15, 12], [[20, 12, 6, 4], [4, 5, 10, 12]])
