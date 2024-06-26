import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import groupby


def affichage(PATTERNS, pertes):

    plt.close('all')

    fig, ax = plt.subplots(figsize=(15, 8))

    colors = ['#C62727', '#27ABC6', '#9B27C6', '#3AC627',
              '#072748', '#48073B', '#B24826', '#0C5021']
    PATTERNS.sort(key=lambda x: x[-1][0], reverse=True)
    nombre_patterns = len(PATTERNS)
    longueur_bobine_max = max([pattern[-1][0] for pattern in PATTERNS])

    for i in range(nombre_patterns):
        longueur = 0
        iterateur = 0

        # affichage des bobines
        for bobine, repetition in groupby(PATTERNS[i][:-1]):
            repetition = len(list(repetition))
            color_index = iterateur % len(colors)
            rectangle = patches.Rectangle(
                (longueur, i*15), bobine*repetition, 10, edgecolor='white', facecolor=colors[color_index], linewidth=1.5)
            ax.add_patch(rectangle)
            format_bobine = round(bobine, 2) if bobine % 1 != 0 else int(bobine)
            if repetition > 1:
                plt.text(longueur + (bobine * repetition) / 2, i*15 + 5,
                         f"{repetition}x{format_bobine}m", ha='center', va='center', color='white', bbox=dict(facecolor='black', boxstyle='round', linewidth=0, alpha=0.7), fontsize='small', fontweight='bold')
            else:
                plt.text(longueur + (bobine * repetition) / 2, i*15 + 5,
                         f'{format_bobine}m', ha='center', va='center', color='white', bbox=dict(facecolor='black', boxstyle='round', linewidth=0, alpha=0.7), fontsize='small', fontweight='bold')
            longueur += bobine*repetition
            iterateur += 1

        # affichage de la perte restante
        if PATTERNS[i][-1][1] != 0:
            rectangle = patches.Rectangle(
                (longueur, i*15), PATTERNS[i][-1][1], 10, edgecolor='white', facecolor='black', linewidth=1.5, alpha=0.8, hatch='/')
            ax.add_patch(rectangle)
            format_pertes = round(PATTERNS[i][-1][1], 2) if PATTERNS[i][-1][1] % 1 != 0 else int(PATTERNS[i][-1][1])
            plt.text(longueur + PATTERNS[i][-1][1] / 2, i*15 + 5,
                     f'{format_pertes}m', ha='center', va='center', color='white', bbox=dict(facecolor='black', boxstyle='round', linewidth=0, alpha=0.7), fontsize='small', fontweight='bold')
            longueur += PATTERNS[i][-1][1]

        # affichage des longueurs de bobines et des répétitions du pattern
        plt.text(-(longueur_bobine_max*0.03), i*15 + 5,
                 f'{PATTERNS[i][-1][0]}m', ha='center', va='center', color='#050118', fontsize='medium', fontweight='bold')
        plt.text(longueur + (longueur_bobine_max*0.03), i*15 + 5,
                 f'{PATTERNS[i][-1][2]}x', ha='center', va='center', color='#050118', fontsize='medium', fontweight='bold')

    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().set_frame_on(False)
    plt.ylim(0, nombre_patterns*15 - 5)
    plt.xlim(0, longueur_bobine_max)
    longueur_totale_pere = sum([pattern[-1][0] * pattern[-1][2]
                                for pattern in PATTERNS])

    longueur_totale_decoupee = sum(
        [sum(pattern[:-1])*pattern[-1][2] for pattern in PATTERNS])
    longueur_pertes = longueur_totale_pere - longueur_totale_decoupee

    format_longueur_totale_pere = round(longueur_totale_pere, 2) if longueur_totale_pere % 1 != 0 else int(
        longueur_totale_pere)
    format_longueur_totale_decoupee = round(longueur_totale_decoupee, 2) if longueur_totale_decoupee % 1 != 0 else int(
        longueur_totale_decoupee)
    format_longueur_pertes = round(longueur_pertes, 2) if longueur_pertes % 1 != 0 else int(
        longueur_pertes)
    format_pertes = round(pertes, 2) if pertes % 1 != 0 else int(pertes)
    
    plt.title(f'Longueur utilisée : {format_longueur_totale_pere}m     Longueur découpée : {format_longueur_totale_decoupee}m \nLongueur perdue : {format_longueur_pertes}m     Pertes : {format_pertes}%',
              fontsize='large', pad=25, fontweight='bold', c='#03053D', )
    plt.show()


if __name__ == '__main__':
    # forme [decoupe 1, ..., decoupe n, [longueur bobine pere, perte, repetitions]], exemple :
    PATTERNS = [[10.3, 10.25, 20.569, 20, 20, 30, 10, [150, 30.0, 4]], [10, [100, 90.45, 3]], [
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, [100, 0.0, 3]], [30, 30, 30, 20, 20, 10, [150, 10.659, 2]]]
    pertes = 0
    affichage(PATTERNS, pertes)
