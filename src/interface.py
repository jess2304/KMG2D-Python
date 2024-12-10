import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algos.KMG2D import kmg2d
from constantes import DOMAINS, SIZE_FUNCTIONS
from heights.hgeom import hgeom
from heights.huniforme import huniform
from informations.idcavity import idcavity
from informations.ihook import ihook
from informations.itrou import itrou
from informations.itwocircle import itwocircle


class KMG2D:
    def __init__(self, root):
        self.root = root
        self.root.title("KMG2D - Génération de Maillages 2D")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Variables pour les paramètres
        self.domain_var = tk.StringVar(value="1")
        self.sizefun_var = tk.StringVar(value="1")
        self.h0_var = tk.StringVar(value="0.03")
        self.dg_var = tk.StringVar(value="1")
        self.nr_var = tk.StringVar(value="0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Créer les widgets
        self.create_widgets()

    def create_widgets(self):
        # Frame principale
        frame_params = ttk.LabelFrame(self.root, text="Paramètres", padding=(10, 10))
        frame_params.pack(side="left", fill="y", padx=10, pady=10)

        # Widgets pour les paramètres
        ttk.Label(frame_params, text="Domaine").grid(row=0, column=0, sticky="w")
        ttk.OptionMenu(
            frame_params,
            self.domain_var,
            "Hook",
            "Trous dans un rectangle",
            "Cavité",
            "Hook",
            "Double cercles",
        ).grid(row=0, column=1, pady=5)

        ttk.Label(frame_params, text="Fonction de Taille").grid(
            row=1, column=0, sticky="w"
        )
        ttk.OptionMenu(
            frame_params, self.sizefun_var, "Uniforme", "Uniforme", "Géometrique"
        ).grid(row=1, column=1, pady=5)

        ttk.Label(frame_params, text="Taille des triangulations").grid(
            row=2, column=0, sticky="w"
        )
        ttk.Entry(frame_params, textvariable=self.h0_var, width=10).grid(
            row=2, column=1, pady=5
        )
        ttk.Label(frame_params, text="Nombre de rafinements").grid(
            row=3, column=0, sticky="w"
        )
        ttk.Entry(frame_params, textvariable=self.nr_var, width=10).grid(
            row=3, column=1, pady=5
        )

        # Frame pour les boutons
        frame_buttons = ttk.Frame(frame_params)
        frame_buttons.grid(row=5, column=0, columnspan=2, pady=10)

        # Bouton Exécuter
        ttk.Button(frame_buttons, text="Exécuter", command=self.run_algorithm).grid(
            row=0, column=0, padx=5, pady=5, sticky="ew"
        )

        # Bouton Forcer l'arrêt
        ttk.Button(frame_buttons, text="Forcer l'arrêt", command=self.force_stop).grid(
            row=0, column=1, padx=5, pady=5, sticky="ew"
        )

        # Bouton Quitter
        ttk.Button(frame_buttons, text="Quitter", command=self.on_closing).grid(
            row=0, column=2, padx=5, pady=5, sticky="ew"
        )

        # Ajuster l'espacement des colonnes pour uniformiser
        frame_buttons.columnconfigure(0, weight=1)
        frame_buttons.columnconfigure(1, weight=1)
        frame_buttons.columnconfigure(2, weight=1)

        self.root.stop_flag = False  # Variable pour contrôler l'arrêt forcé

        # Frame pour la barre de progression
        self.progress = ttk.Progressbar(
            frame_params, orient="horizontal", length=150, mode="determinate"
        )
        self.progress.grid(row=9, column=0, columnspan=2, pady=10)

        # Label pour le pourcentage
        self.progress_label = ttk.Label(frame_params, text="0%")
        self.progress_label.grid(row=10, column=0, columnspan=2, pady=(0, 10))

        # Initialisation de la figure et de l'axe
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

        # Frame pour l'affichage des résultats
        frame_plot = ttk.LabelFrame(self.root, text="Visualisation", padding=(10, 10))
        frame_plot.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Intégration Matplotlib dans Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_plot)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

    def run_algorithm(self):
        # Réinitialiser la progression
        self.progress["value"] = 0
        self.root.stop_flag = False
        # Récupérer les valeurs des paramètres
        try:
            domain = DOMAINS[self.domain_var.get()]
            sizefun = SIZE_FUNCTIONS[self.sizefun_var.get()]
            nr = int(self.nr_var.get())
            h0 = float(self.h0_var.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez vérifier les paramètres !")
            return

        # Choix de la fonction de taille
        if sizefun == 1:
            fh = huniform
        elif sizefun == 2:
            fh = hgeom
        else:
            messagebox.showerror("Erreur", "Fonction de taille invalide !")
            return

        # Choix du domaine
        if domain == 1:
            fd, bbox, pfix = itrou()
        elif domain == 2:
            fd, bbox, pfix = idcavity()
        elif domain == 3:
            fd, bbox, pfix = ihook()
        elif domain == 4:
            fd, bbox, pfix = itwocircle()
        else:
            messagebox.showerror("Erreur", "Domaine invalide !")
            return

        # Exécuter kmg2d
        try:
            # Réinitialiser les axes
            # Supprimer les anciens axes
            for ax in self.fig.axes:
                self.fig.delaxes(ax)
            # Créer un nouvel axe
            self.ax = self.fig.add_subplot(111)
            # S'assure que les axes sont vides
            self.ax.clear()
            # Met à jour le canvas
            self.canvas.draw()
            # Réinitialise la barre de progression
            self.progress["value"] = 0
            self.progress_label.config(text="0%")
            # Démarre l'algorithme
            if domain != 4:
                kmg2d(
                    fd,
                    fh,
                    h0,
                    bbox,
                    nr,
                    pfix,
                    self.canvas,
                    self.root,
                    self.ax,
                    self.update_progress,
                )
            else:
                kmg2d(
                    fd,
                    fh,
                    h0,
                    bbox,
                    nr,
                    pfix,
                    self.canvas,
                    self.root,
                    self.ax,
                    self.update_progress,
                    0,
                    0,
                    1,
                    -0.4,
                    0,
                    0.5,
                )
            if not self.root.stop_flag:
                messagebox.showinfo("Succès", "Maillage généré avec succès !")
        except Exception as e:
            if not self.root.stop_flag:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
                return

    def update_progress(self, value, iteration=None, iterMax=None):
        self.progress["value"] = value
        if iteration is not None and iterMax is not None:
            self.progress_label.config(
                text=f"{value:.1f}% (Itération {iteration}/{iterMax})"
            )
        else:
            self.progress_label.config(text=f"{value:.1f}%")
        self.root.update_idletasks()

    def on_closing(self):
        """
        Ferme proprement l'application lorsqu'on clique sur la croix.
        """
        if messagebox.askokcancel(
            "Quitter", "Voulez-vous vraiment quitter l'application ?"
        ):
            self.root.destroy()
            plt.close("all")

    def force_stop(self):
        """Déclenche l'arrêt forcé de l'algorithme."""
        self.root.stop_flag = True
