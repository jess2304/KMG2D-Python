#		Projet : Génération de maillages 2D en Python.
#			    Jessem Ettaghouti

Le projet a été réalisé en MATLAB par le Professeur KOKO Jonas, et il a été refait en Python.
Auparavant, il représentait des anomalies dans l'algorithme et des problèmes majeurs.

Ces problèmes n'existent plus. Le programme fonctionne avec une bonne performance et une bonne représentation des maillages.

Une interface graphique est mise en place. L'outil exécutable est créé après le build de Github Actions dans le dossier src/dist/
Il suffit d'en faire un raccourcis au bureau et travailler avec.


L'outil présente 4 domaines qu'on peut représenter, avec deux fontions de taille différentes (géometrique et uniforme) : Elle donne la caractéristique de la taille de chaque triangulation. On peut préciser aussi la taille même de la triangulation : Plus on met une valeur petite, plus la taille sera petite, et plus le nombre de triangulations sera grand, et donc plus de temps à représenter.

On peut forcer l'arrêt si on veut démarrer une autre construction. Et quitter de façon safe que ce soit avec le bouton Quitter ou avec la croix de la fenêtre.


Pour démarrer le programme, il suffit de cloner le répertoire, et accéder à output/app/KMG2D.exe
