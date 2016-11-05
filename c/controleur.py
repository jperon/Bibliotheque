from . import db_interaction as db


def enregistrer(objet, donnees):
    {
        'ouvrage': enregistrer_ouvrage,
        'auteur': enregistrer_auteur,
        'editeur': enregistrer_editeur,
    }[objet](donnees)


def enregistrer_ouvrage(donnees):
    ouvrage = db.ouvrage(donnees['id'])
    ouvrage.titre = donnees['titre']
    ouvrage.auteur = db.auteur(donnees['auteur'])
    ouvrage.editeur = db.editeur(donnees['editeur'])
    ouvrage.save()


def enregistrer_auteur(donnees):
    auteur = db.auteur(donnees['id'])
    auteur.particule = donnees['particule']
    auteur.nom = donnees['nom']
    auteur.prenom = donnees['prenom']
    auteur.titre = donnees['titre']
    auteur.save()


def enregistrer_editeur(donnees):
    editeur = db.editeur(donnees['id'])
    editeur.nom = donnees['nom']
    editeur.save()


def liste(**params):
    fnct = {
        'auteurs': liste_auteurs,
        'editeurs': liste_editeurs,
        'ouvrages': liste_ouvrages,
    }[params['objet']]
    del params['objet']
    return fnct(**params)


def liste_auteurs(tri='nom', criteres=None):
    return(tuple(
        dict(
            id=auteur.id,
            particule=auteur.particule,
            nom=auteur.nom,
            prenom=auteur.prenom,
            titre=auteur.titre
        ) for auteur in db.liste_auteurs(tri, criteres)
    ))


def liste_editeurs(tri='nom', criteres=None):
    return(tuple(
        dict(
            id=editeur.id,
            nom=editeur.nom,
        ) for editeur in db.liste_editeurs(tri, criteres)
    ))


def liste_ouvrages(tri='titre', criteres=None):
    return(tuple(
        dict(
            id=ouvrage.id,
            titre=ouvrage.titre,
            auteur=' '.join((
                ouvrage.auteur.titre,
                ouvrage.auteur.prenom,
                ' '.join((
                    ouvrage.auteur.particule, ouvrage.auteur.nom
                )).replace("' ", "'"),
            )),
            editeur=ouvrage.editeur.nom,
            auteurs=' ; '.join(
                ' '.join((
                    auteur.titre,
                    auteur.prenom,
                    auteur.particule,
                    auteur.nom,
                ))
                for auteur in ouvrage.auteurs
            ),
            exemplaires=ouvrage.exemplaires.count()
        ) for ouvrage in db.liste_ouvrages(tri, criteres)
    ))


def ouvrage(id):
    ouvrage = db.ouvrage(id)
    return dict(
        id=ouvrage.id,
        titre=ouvrage.titre,
        auteur=dict(
            id=ouvrage.auteur.id,
            particule=ouvrage.auteur.particule,
            nom=ouvrage.auteur.nom,
            prenom=ouvrage.auteur.prenom,
            titre=ouvrage.auteur.titre
        ),
        editeur=dict(
            id=ouvrage.editeur.id,
            nom=ouvrage.editeur.nom,
        ),
        exemplaires=[
            dict(
                id=exemplaire.id,
                numero=exemplaire.numero,
                volumes=[
                    dict(
                        id=volume.id,
                        titre=volume.titre,
                        date_acquisition=str(volume.date_acquisition)
                    )
                    for volume in exemplaire.volumes
                    if not(volume.date_suppression)
                ]
            )
            for exemplaire in ouvrage.exemplaires
        ],
    )


def auteur(id):
    auteur = db.auteur(id)
    return dict(
        id=auteur.id,
        particule=auteur.particule,
        nom=auteur.nom,
        prenom=auteur.prenom,
        titre=auteur.titre,
    )


def editeur(id):
    editeur = db.editeur(id)
    return dict(
        id=editeur.id,
        nom=editeur.nom,
    )
