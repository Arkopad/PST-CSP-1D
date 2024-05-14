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
    for i, taille in enumerate(liste_pere):
        for r in range(1, len(liste_fils) + 1):
            combinations = combinations_with_replacement(liste_fils, r)
            for combination in combinations:
                combinaison_possibles_temp = [] 
                if sum(combination) <= liste_pere[i]:
                    combinaison_possibles_temp.append(combination)
                    combinaison_possibles_temp.append(taille)
                    combinaison_possibles.append(combinaison_possibles_temp)    

    combinaison_possibles = list(set(tuple(i) for i in combinaison_possibles))


    representation_vectorielle = []
    for combination in combinaison_possibles:
        taille_pere = combination[1]	
        combination = combination[0]

        representation_vectorielle_temp = []
        vector = [combination.count(length) for length in liste_fils]
        representation_vectorielle_temp.append(vector)
        representation_vectorielle_temp.append(taille_pere)
        representation_vectorielle.append(representation_vectorielle_temp)

    
  
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

            coeff = representation_vectorielle[j][0]

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
        
        print('\n',representation_vectorielle)

        liste_affichage = []
        for i, var in enumerate(variables):
            liste_temp = []
            if pulp.value(var) != 0:
                print(f"{pulp.value(var)}x la representation : {representation_vectorielle[i]}")
                # creer la liste pour l'affichage de cette forme : [[10, 10, 20, 20, 20 [150, 30.0, 4]], [10, [100, 90, 3]]]
                
                

    else:
        print("The problem does not have an optimal solution.")

    # # affichage graphique (FAIRE LE TODO AVANT)
    # pattern_affichage = []
    # for i, var in enumerate(variables):
    #     if pulp.value(var) != 0:
    #         pattern_affichage.append()



if __name__ == "__main__":
    prog_lineaire_pulp([10, 14], [[16,18], [4,6]])
