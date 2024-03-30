# Importation des librairies
import tkinter as tk
from tkinter import messagebox

# Importation des fonctions
from csp_pattern_optimaux import main
from csp_random import func_csp_random


class ImageCheckbutton(tk.Checkbutton):
    def __init__(self, master=None, checked_image=None, unchecked_image=None, **kwargs):
        self.checked_image = tk.PhotoImage(file='checked.png')
        self.unchecked_image = tk.PhotoImage(file='unchecked.jpg')
        super().__init__(master, image=self.unchecked_image,
                         selectimage=self.checked_image, **kwargs)


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

        # Checkbox pour la résolution optimale
        self.optimal_resolution = tk.IntVar()
        self.checkbox = ImageCheckbutton(
            self.racine,
            text="Résolution optimale",
            variable=self.optimal_resolution,
            # Remplacez par le chemin vers votre image pour l'état coché
            checked_image='checked.png',
            # Remplacez par le chemin vers votre image pour l'état non coché
            unchecked_image='unchecked.png',
            bg="#010D19",
            fg="#A5A5B5",
            font=("Helvetica", 24, "bold"),
            activebackground="white",
            activeforeground="black",
            bd=2,
            relief="sunken",
            padx=5,
            pady=5,
            cursor="hand2",
        )
        self.checkbox.pack(ipady=6, expand=True)

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
            command=self.user_mode,
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
            main([180, 100], [[800, 500, 100], [30, 45, 50]])
        else:
            func_csp_random([180, 100], [[800, 500, 100], [30, 45, 50]],
                            0, 5000, True)

    def multi_mode(self):
        """
        def:
        """
        if self.optimal_resolution.get():
            main([150, 100], [[600, 700, 500], [30, 45, 50]])
        else:
            func_csp_random([150, 100], [[600, 700, 500], [30, 45, 50]],
                            0, 5000, True)

    def user_mode(self):
        """
        def:
        """
        if self.optimal_resolution.get():
            main([100, 150], [[102, 103, 104, 101, 33, 100, 100],
                              [9.3, 11.2, 6.1, 10.4, 5.5, 7.3, 8.9]])
        else:
            func_csp_random([100, 150], [[102, 103, 104, 101, 33, 100, 100],
                                         [9.3, 11.2, 6.1, 10.4, 5.5, 7.3, 8.9]],
                            0, 5000, True)


if __name__ == "__main__":
    # Lancement de la fenêtre principale
    menu_principal = MenuPrincipal()
    menu_principal.racine.mainloop()
