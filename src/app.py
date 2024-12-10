"""
********************************************************************************************
*********************** Application pour la génération de maillages en 2D ******************
***********************               Jessem ETTAGHOUTI                    *****************
********************************************************************************************
"""
import tkinter as tk

from interface import KMG2D

if __name__ == "__main__":
    root = tk.Tk()
    app = KMG2D(root)
    root.mainloop()
