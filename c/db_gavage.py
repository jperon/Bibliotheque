from .db_interaction import *

stThomas, cree = creer_auteur("d'", "Aquin", "Thomas", "Saint")
stAugustin, cree = creer_auteur("", "Augustin", "", "Saint")
abBoubee, cree = creer_auteur("", "Boubée", "Jean-Pierre", "M. l'abbé")
marietti, cree = creer_editeur("Marietti")
dpf, cree = creer_editeur("DPF")
clovis, cree = creer_editeur("Clovis")

creer_ouvrage("Contra Gentes", stThomas, clovis)
creer_ouvrage("De Veritate", stThomas, marietti)
creer_ouvrage("Compendium", stThomas, marietti)
creer_ouvrage("Confessions", stAugustin, dpf)
creer_ouvrage("Idéal et l'art du chef (l')", abBoubee, clovis)

summa, cree = creer_ouvrage("Summa theologiæ", stThomas, marietti)
summa_exA, cree = creer_exemplaire(summa, 1)
summa_exA_volA, cree = creer_volume(summa_exA, "Ia Pars")

fermer_db()
