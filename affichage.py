import matplotlib.pyplot as plt
import matplotlib.patches as patches

# forme [decoupe 1, ..., decoupe n, [longueur bobine pere, perte, repetitions]], exemple :
# PATTERNS = [[35, 60, [150, 55, 4]], [35, 35, [100, 30, 3]], [35, 35, [100, 30, 3]], [30, 30, [100, 40, 2]],
#            [30, 30, [100, 40, 2]], [30, 30, [100, 40, 2]], [30, 30, 20, 20, 10, [150, 40, 2]], [30, 30, [140, 80, 2]]]


def affichage(PATTERNS, pertes):

    plt.close('all')
    fig, ax = plt.subplots()
    colors = ['red', 'blue', 'green', 'yellow',
              'purple', 'orange', 'pink', 'brown']
    PATTERNS.sort(key=lambda x: x[-1][0], reverse=True)
    nombre_patterns = len(PATTERNS)
    longueur_bobine_max = max([pattern[-1][0] for pattern in PATTERNS])

    for i in range(nombre_patterns):
        longueur = 0
        for j, bobine in enumerate(PATTERNS[i]):
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
        plt.text(-(longueur_bobine_max*0.05), i*15 + 5,
                 f'{PATTERNS[i][-1][0]}', ha='center', va='center', color='black')
        plt.text(longueur + (longueur_bobine_max*0.05), i*15 + 5,
                 f'x{PATTERNS[i][-1][2]}', ha='center', va='center', color='black')

    plt.gca().axes.get_yaxis().set_visible(False)
    plt.xticks(range(0, longueur_bobine_max + 1, longueur_bobine_max))
    plt.ylim(0, nombre_patterns*15 - 5)
    plt.xlim(0, longueur_bobine_max)
    plt.title(f'Pertes : {pertes:.2f}%')
    plt.show()
