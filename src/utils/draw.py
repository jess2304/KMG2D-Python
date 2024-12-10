def draw(p, t, ax, canvas, root):
    """
    Réalise une nouvelle visualisation (dessin de maillages) dans la figure.
    """
    ax.clear()
    ax.triplot(p[:, 0], p[:, 1], t, color="blue")
    canvas.draw()
    root.update_idletasks()
    root.update()
