
class Papa:
    def __init__(self, liste_de_taches=[]):
        self.liste_de_taches = liste_de_taches

    def __str__(self):
        return "-".join(self.liste_de_taches)


def genere_un_papa_avec_ses_taches():

    un_papa = Papa()

    for i in range(0, 10):
        un_papa.liste_de_taches.append(f'tache {i}')

    return un_papa

le_meilleur_papa = genere_un_papa_avec_ses_taches()
print(le_meilleur_papa)
print(id(le_meilleur_papa))
print(id(le_meilleur_papa.liste_de_taches))

un_autre = genere_un_papa_avec_ses_taches()
print(un_autre)
print(id(un_autre))
print(id(un_autre.liste_de_taches))

encore_un_autre = genere_un_papa_avec_ses_taches()
print(encore_un_autre)
print(id(encore_un_autre))
print(id(encore_un_autre.liste_de_taches))
