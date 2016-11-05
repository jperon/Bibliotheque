from datetime import date

from m import db


def ouvrir_db():
    db.base.connect()


def fermer_db():
    db.base.close()


def creer_auteur(particule, nom, prenom, titre):
    auteur = db.Auteur.get_or_create(
        particule=particule, nom=nom, prenom=prenom, titre=titre
    )
    return auteur


def creer_editeur(nom):
    return db.Editeur.get_or_create(nom=nom)


def creer_ouvrage(titre, auteur, editeur, auteurs=None):
    ouvrage = db.Ouvrage.get_or_create(
        titre=titre, auteur=auteur, editeur=editeur
    )
    if auteurs:
        ouvrage[0].auteurs = auteurs
    return ouvrage


def creer_exemplaire(ouvrage, numero):
    return db.Exemplaire.get_or_create(
        ouvrage=ouvrage, numero=numero
    )


def creer_volume(
        exemplaire,
        titre,
        date_acquisition=date.today(),
        date_suppression=None
        ):
    return db.Volume.create_or_get(
        exemplaire=exemplaire,
        titre=titre,
        date_acquisition=date_acquisition,
        date_suppression=date_suppression
    )


def liste_auteurs(tri='nom', criteres=None):
    if not criteres:
        criteres = {'particule': '', 'nom': '', 'prenom': '', 'titre': ''}
    return(
        db.Auteur.select()
        .where(
            (db.Auteur.particule ** '%{}%'.format(criteres['particule'])) &
            (db.Auteur.nom ** '%{}%'.format(criteres['nom'])) &
            (db.Auteur.prenom ** '%{}%'.format(criteres['prenom'])) &
            (db.Auteur.titre ** '%{}%'.format(criteres['titre']))
        )
        .order_by({
            'nom': db.Auteur.nom,
            'prenom': db.Auteur.prenom,
            'titre': db.Auteur.titre,
        }[tri])
    )


def liste_editeurs(tri='nom', criteres=None):
    if not criteres:
        criteres = {'nom': ''}
    return(
        db.Editeur.select()
        .where((db.Editeur.nom ** '%{}%'.format(criteres['nom'])))
        .order_by({
            'nom': db.Editeur.nom,
        }[tri])
    )


def liste_ouvrages(tri='titre', criteres=None):
    if not criteres:
        criteres = {'titre': '', 'auteur': '', 'editeur': ''}
    return (
        db.Ouvrage.select().join(db.Auteur)
        .switch(db.Ouvrage).join(db.Editeur)
        .switch(db.Exemplaire).join(db.Volume)
        .where(
            (db.Ouvrage.titre ** '%{}%'.format(criteres['titre'])) &
            (
                (db.Auteur.nom ** '%{}%'.format(criteres['auteur'])) |
                (db.Auteur.prenom ** '%{}%'.format(criteres['auteur']))
            ) &
            (db.Editeur.nom ** '%{}%'.format(criteres['editeur']))
        )
        .order_by({
            'titre': db.Ouvrage.titre,
            'auteur': db.Auteur.nom,
            'editeur': db.Editeur.nom,
            'auteurs': None,
            'exemplaires': None,
        }[tri])
    )


def auteur(id):
    return(db.Auteur.get(db.Auteur.id == id))


def editeur(id):
    return(db.Editeur.get(db.Editeur.id == id))


def ouvrage(id):
    return(
        db.Ouvrage.select().join(db.Auteur)
        .switch(db.Ouvrage).join(db.Editeur)
        .switch(db.Exemplaire).join(db.Volume)
        .where(db.Ouvrage.id == id)
        .get()
    )
