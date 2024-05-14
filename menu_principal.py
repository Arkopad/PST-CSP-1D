# Importation des librairies
import tkinter as tk
from tkinter import messagebox

# Importation des fonctions
from csp_pattern_optimaux import main
from csp_random import func_csp_random
from prog_lineaire import prog_lineaire_pulp


class MenuPrincipal():
    def __init__(self):
        # Create the main window using tkinter
        self.racine = tk.Tk()
        self.racine.geometry('1280x720')
        self.racine.configure(bg='#141418')
        self.racine.resizable(False, False)

        # Set the title of the window
        self.racine.title('Cutting Stock Problem - 1D')

        # Affectation des touches
        self.racine.bind_all("<Key-Escape>", self.echap)

        # Création des widgets
        self.creer_widgets()

    def creer_widgets(self):
        """
        def: crée et affiche les widgets sur la fenêtre principale
        """

        # Frame du titre du jeu en haut de l'écran
        self.frame_top = tk.Frame(
            self.racine,
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=12)

        # Label du titre du jeu
        self.titre = tk.Label(
            self.frame_top,
            text="Cutting Stock Problem - 1D",
            bg="#010D19",
            fg="#A5A5B5",
            # Increase font size and make it bold
            font=("Helvetica", 30, "bold")
        )
        self.titre.pack(pady=4)

        # frame des checkboxes
        self.frame_checkboxes = tk.Frame(
            self.racine,
            bg="#141418",
        )
        self.frame_checkboxes.pack(ipady=6, expand=True)

        # Checkbox pour la résolution optimale
        self.optimal_resolution = tk.IntVar()
        self.optimal_resolution.set(1)
        self.checkbox = tk.Checkbutton(
            self.frame_checkboxes,
            text="Résolution optimale",
            variable=self.optimal_resolution,
            bg="#010D19",
            fg="#A5A5B5",
            font=("Helvetica", 24, "bold"),
            selectcolor="black",
            activebackground="white",
            activeforeground="black",
            bd=2,
            relief="sunken",
            padx=5,
            pady=5,
            cursor="hand2",
        )
        self.checkbox.pack(side=tk.LEFT, padx=50)

        # Checkbox pour la résolution linéaire
        self.linear_resolution = tk.IntVar()
        self.linear_resolution.set(1)
        self.checkbox = tk.Checkbutton(
            self.frame_checkboxes,
            text="Résolution linéaire",
            variable=self.linear_resolution,
            bg="#010D19",
            fg="#A5A5B5",
            font=("Helvetica", 24, "bold"),
            selectcolor="black",
            activebackground="white",
            activeforeground="black",
            bd=2,
            relief="sunken",
            padx=5,
            pady=5,
            cursor="hand2",
        )
        self.checkbox.pack(side=tk.RIGHT, padx=50)

        # Bouton single mode
        self.single = tk.Button(
            self.racine,
            cursor="hand2",
            text="Single mode",
            bg="#010D19",
            fg="#A5A5B5",
            command=self.single_mode,
            font=("Helvetica", 24, "bold"),
        )
        self.single.pack(ipady=6, expand=True)

        # Bouton multi mode
        self.multi = tk.Button(
            self.racine,
            cursor="hand2",
            text="Multi mode",
            bg="#010D19",
            fg="#A5A5B5",
            command=self.multi_mode,
            font=("Helvetica", 24, "bold"),
        )
        self.multi.pack(ipady=6, expand=True)

        # Bouton mode utilisateur
        self.user = tk.Button(
            self.racine,
            cursor="hand2",
            text="Mode utilisateur",
            bg="#010D19",
            fg="#A5A5B5",
            command=self.parametre_user_mode,
            font=("Helvetica", 24, "bold"),
        )
        self.user.pack(ipady=6, expand=True)

    def echap(self, event):
        """
        def: sur appui de la touche "échap", quitte la fenêtre et arrête le programme
        """
        if event.keysym == "Escape":
            self.racine.destroy()

    def single_mode(self):
        """
        def: 
        """
        if self.optimal_resolution.get():
            main([180, 100], [[800, 500, 100], [30, 45, 50]], 0, 5000)
        elif self.linear_resolution.get():
            prog_lineaire_pulp([180, 100], [[800, 500, 100], [30, 45, 50]])
        else:
            func_csp_random([180, 100], [[800, 500, 100], [30, 45, 50]],
                            0, 5000, True)

    def multi_mode(self):
        """
        def:
        """
        if self.optimal_resolution.get():
            main([150, 100], [[600, 700, 500], [30, 45, 50]], 0, 5000)
        elif self.linear_resolution.get():
            prog_lineaire_pulp([100, 150], [[600, 700, 500], [30, 45, 50]])
        else:
            func_csp_random([150, 100], [[600, 700, 500], [30, 45, 50]],
                            0, 5000, True)

    def parametre_user_mode(self):
        """
        def:
        """
        # Create a new temporary window
        self.temp_window = tk.Toplevel(self.racine)
        self.temp_window.title('Paramètres utilisateur')
        self.temp_window.geometry('900x600')
        self.temp_window.configure(bg='#141418')
        self.temp_window.resizable(False, False)
        # Frame du titre du jeu en haut de l'écran
        self.frame_top = tk.Frame(
            self.temp_window,
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=12)

        # Label du titre du jeu
        self.titre = tk.Label(
            self.frame_top,
            text="Choix des paramètres utilisateur",
            bg="#010D19",
            fg="#A5A5B5",
            # Increase font size and make it bold
            font=("Helvetica", 25, "bold")
        )
        self.titre.pack(pady=4)

        # Affectation des touches
        self.racine.bind_all("<Key-Escape>", self.echap)

        # texte pour les longueurs des bobines pères
        self.label_longueur_bobine_pere = tk.Label(
            self.temp_window,
            text="Longueurs des bobines pères :",
            bg="#141418",
            fg="#A5A5B5",
            font=("Helvetica", 13, "bold"),
        )
        self.label_longueur_bobine_pere.pack(pady=(30, 0))

        # zone de texte pour les longueurs des bobines pères
        self.longueur_bobine_pere = tk.Entry(
            self.temp_window,
            bg="#010D19",
            fg="#A5A5B5",
            font=("Helvetica", 15, "bold"),
            width=30,
            justify='center',
            insertbackground='white',
        )
        self.longueur_bobine_pere.insert(
            0, '150, 100, 70')
        self.longueur_bobine_pere.pack(ipady=6, pady=(0, 50))

        # texte pour les longueurs des bobines fils
        self.label_longueur_bobine_fils = tk.Label(
            self.temp_window,
            text="Longueurs des bobines à découper :",
            bg="#141418",
            fg="#A5A5B5",
            font=("Helvetica", 13, "bold"),
        )
        self.label_longueur_bobine_fils.pack()

        # zone de texte pour les longueurs des bobines fils
        self.longueur_bobine_fils = tk.Entry(
            self.temp_window,
            bg="#010D19",
            fg="#A5A5B5",
            font=("Helvetica", 15, "bold"),
            width=30,
            justify='center',
            insertbackground='white',
        )
        self.longueur_bobine_fils.insert(
            0, '40, 50, 60, 80')

        self.longueur_bobine_fils.pack(ipady=6, pady=(0, 50))

        # texte pour le nombre des bobines fils
        self.label_nombre_bobine_fils = tk.Label(
            self.temp_window,
            text="Quantité des bobines à découper :",
            bg="#141418",
            fg="#A5A5B5",
            font=("Helvetica", 13, "bold"),
        )
        self.label_nombre_bobine_fils.pack()

        # zone de texte pour le nombre de bobines fils
        self.nombre_bobine_fils = tk.Entry(
            self.temp_window,
            bg="#010D19",
            fg="#A5A5B5",
            font=("Helvetica", 15, "bold"),
            width=30,
            justify='center',
            insertbackground='white',
        )
        self.nombre_bobine_fils.insert(
            0, '100, 500, 500, 300')
        self.nombre_bobine_fils.pack(ipady=6)

        # Create a button in the temporary window
        self.validate_button = tk.Button(
            self.temp_window,
            cursor="hand2",
            text="Lancer la résolution",
            bg="#010D19",
            fg="#A5A5B5",
            font=("Helvetica", 24, "bold"),
            command=self.user_mode,
        )
        self.validate_button.pack(ipady=6, expand=True)

    def user_mode(self):
        """
            def: This function will execute the user_mode function and destroy the temp_window
            """

        # Get the values from the entries
        longueur_bobine_pere = self.longueur_bobine_pere.get().split(',')
        longueur_bobine_pere = [int(i) for i in longueur_bobine_pere]
        longueur_bobine_fils = self.longueur_bobine_fils.get().split(',')
        longueur_bobine_fils = [float(i) for i in longueur_bobine_fils]
        nombre_bobine_fils = self.nombre_bobine_fils.get().split(',')
        nombre_bobine_fils = [int(i) for i in nombre_bobine_fils]

        if self.optimal_resolution.get():
            main(longueur_bobine_pere, [
                 nombre_bobine_fils, longueur_bobine_fils], 0, 5000)

        elif self.linear_resolution.get():
            prog_lineaire_pulp(longueur_bobine_pere, [
                nombre_bobine_fils, longueur_bobine_fils])

        else:
            func_csp_random(longueur_bobine_pere, [
                            nombre_bobine_fils, longueur_bobine_fils], 0, 5000, True)


if __name__ == "__main__":

    # Lancement de la fenêtre principale
    menu_principal = MenuPrincipal()
    menu_principal.racine.mainloop()
