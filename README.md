# ocrp7
OpenClassRooms Projet 7  
Résolvez des problèmes en utilisant des algorithmes en Python  

![Logo AlgoInvestAndTrade](https://raw.githubusercontent.com/FLinguenheld/ocrp7/main/AlgoInvestAndTrade.png "Logo")
![Logo FLinguenheld](https://raw.githubusercontent.com/FLinguenheld/ocrp7/main/forelif.png "Pouet")


****
### Description
L'objectif de ce projet est d'aborder l'algorithmie en développant des solutions permettant à une société 
de maximiser ses investissements.  
Une première liste de 20 actions est traitée avec un algorithme *bruteforce* puis deux autres plus importantes avec 
un algorithme *glutton*.


****
### Installation

Rendez-vous dans le dossier de votre choix puis lancez un terminal.  
Clônez le dossier depuis GitHub avec la commande :

    git clone https://github.com/FLinguenheld/ocrp7

Les fichiers d'actions à analyser doivent être des .csv et rangés dans le dossier 'fichiers'.  
Ils doivent contenir trois colonnes : name, price, profit.  
Les nombres sont convertis en float, les valeurs nulles ou négatives sont ignorées.


****
### Déroulement
##### 1.Forcebrute

Entrez la commande :

    python forcebrute.py

Sélectionnez le fichier à analyser et validez.  
Le programme affichera le nombre de combinaisons à réaliser ainsi qu'une barre de progression.  
Attention: au delà de 30 actions le temps d'exécution devient très important.

Cet algorithme teste toutes les combinaisons possibles et trouve la meilleure solution.

##### 2.Optimized

Entrez la commande :

    python optimized.py

- Sélectionnez le fichier à analyser
- Entrez le temps d'analyse
- Entrez le nombre de threads

Basée sur un algorithme *glutton*, cette commande génère aléatoirement un maximum de combinaisons pendant le
temps renseigné afin de conserver la plus rentable.  

Un algorithme est lancé par thread pour multiplier le nombre d'essais.  
Il trouve donc une solution optimisée permettant de traiter une liste avec un nombre important d'actions.
