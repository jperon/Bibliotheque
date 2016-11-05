from browser import document as doc, ajax, alert
from browser.html import (
    DIV, A, P,
    FORM, INPUT, BUTTON, SELECT, OPTION,
    TABLE, TBODY, TH, THEAD, TD, TR,
    UL, LI,
)
import json

TRI = ''
ASC = True
RQ = ajax.ajax()


def menu():
    menu = UL()
    lien_ouvrages = A('Ouvrages', href='#liste')
    lien_auteurs = A('Auteurs', href='#liste')
    lien_editeurs = A('Éditeurs', href='#liste')
    lien_ouvrages.bind(
        'click', lambda ev: charger_liste(ev, 'ouvrages', 'titre')
    )
    lien_auteurs.bind(
        'click', lambda ev: charger_liste(ev, 'auteurs', 'nom')
    )
    lien_editeurs.bind(
        'click', lambda ev: charger_liste(ev, 'editeurs', 'nom')
    )
    menu <= LI(lien_ouvrages)
    menu <= LI(lien_auteurs)
    menu <= LI(lien_editeurs)
    doc['menu'].clear()
    doc['menu'] <= menu


def menu_cacher(ev):
    doc['menu'].hidden = not(doc['menu'].hidden)
    doc['cacher'].text = {'«': '»', '»': '«'}[doc['cacher'].text]


def afficher(contenu):
    doc['contenu'].clear()
    doc['contenu'] <= DIV(contenu)


def requete(adresse, fonction=None, methode='GET', parametres=None):
    global RQ
    rq = ajax.ajax()
    if fonction:
        rq.bind('complete', fonction)
    rq.open(methode, adresse, False)
    rq.set_header('content-type', 'application/x-www-form-urlencoded')
    if parametres:
        rq.send(parametres)
    else:
        rq.send()
    RQ = rq
    return rq.text


def charger(ev, cible):
    fonction, arguments = cible.split(':')
    {
        'ouvrages':
            lambda num: requete(
                '/db/ouvrage/{}'.format(num),
                fonction=lambda rq: afficher(charger_ouvrage(rq))
            ),
        'auteurs':
            lambda num: requete(
                '/db/auteur/{}'.format(num),
                fonction=lambda rq: afficher(charger_auteur(rq))
            ),
        'editeurs':
            lambda num: requete(
                '/db/editeur/{}'.format(num),
                fonction=lambda rq: afficher(charger_editeur(rq))
            ),
    }[fonction](*arguments)


def charger_ouvrage(rq):
    prp = json.loads(rq.text)
    sel_auteur = SELECT(name='auteur', id='auteur')
    sel_auteur <= (OPTION(
            '{titre} {prenom} {particule} {nom}'
            .format(**auteur).replace("' ", "'"),
            value=auteur['id'],
            selected=(auteur['id'] == prp['auteur']['id'])
        ) for auteur in json.loads(requete('/db/liste/auteurs')))
    sel_editeur = SELECT(name='editeur', id='editeur')
    sel_editeur <= (OPTION(
            editeur['nom'],
            value=editeur['id'],
            selected=(editeur['id'] == prp['editeur']['id'])
        ) for editeur in json.loads(requete('/db/liste/editeurs')))
    bouton = BUTTON('Modifier')
    bouton.bind(
        'click',
        lambda ev: enregistrer(ev, 'ouvrage')
    )
    return (
        INPUT(type='hidden', value=str(prp['id']), id='id') +
        tableau(
            [
                ['Titre', INPUT(
                    type='text', name='titre', value=prp['titre'], id='titre'
                )],
                ['Auteur', sel_auteur],
                ['Éditeur', sel_editeur],
            ],
            entete=False, trier=False
        ) +
        bouton
    )


def charger_auteur(rq):
    prp = json.loads(rq.text)
    bouton = BUTTON('Modifier')
    bouton.bind(
        'click',
        lambda ev: enregistrer(ev, 'auteur')
    )
    return (
        INPUT(type='hidden', value=str(prp['id']), id='id') +
        tableau(
            [
                ['Titre', INPUT(
                    type='text', name='titre', id='titre',
                    value=prp['titre']
                )],
                ['Prénom', INPUT(
                    type='text', name='prenom', id='prenom',
                    value=prp['prenom']
                )],
                ['Particule', INPUT(
                    type='text', name='particule', id='particule',
                    value=prp['particule']
                )],
                ['Nom', INPUT(
                    type='text', name='nom', id='nom',
                    value=prp['nom']
                )],
            ],
            entete=False, trier=False
        ) +
        bouton
    )


def charger_editeur(rq):
    prp = json.loads(rq.text)
    bouton = BUTTON('Modifier')
    bouton.bind(
        'click',
        lambda ev: enregistrer(ev, 'editeur')
    )
    return (
        INPUT(type='hidden', value=str(prp['id']), id='id') +
        tableau(
            [
                ['Nom', INPUT(
                    type='text', name='nom', id='nom',
                    value=prp['nom']
                )],
            ],
            entete=False, trier=False
        ) +
        bouton
    )


def charger_liste(ev, obj, tri='', actualiser=True, criteres=None):
    global TRI, ASC
    adr, titres = {
        'ouvrages': (
            '/db/liste/ouvrages',
            [
                ('Titre', 'titre'),
                ('Auteur', 'auteur'),
                ('Éditeur', 'editeur'),
                ('Autres auteurs', 'auteurs'),
                ('Exemplaires', 'exemplaires')
            ]
        ),
        'auteurs': (
            '/db/liste/auteurs',
            [
                ('Particule', 'particule'),
                ('Nom', 'nom'),
                ('Prénom', 'prenom'),
                ('Titre', 'titre')
            ]
        ),
        'editeurs': (
            '/db/liste/editeurs',
            [
                ('Nom', 'nom'),
            ]
        ),
    }[obj]

    def fnct(rq):
        afficher(
            formulaire(obj, titres) +
            tableau_dict(titres, json.loads(rq.text), obj=obj)
        )

    if actualiser or tri != TRI:
        TRI = tri
        requete(
            '{}/{}?{}'.format(adr, tri, '&'.join(
                '{}={}'.format(cle, valeur)
                for cle, valeur in criteres.items()
            ) if criteres else ''),
            fonction=fnct
        )
    else:
        ASC = not(ASC)
        fnct(RQ)


def enregistrer(ev, obj):
    if obj == 'ouvrage':
        parametres = dict(
            id=doc['id'].value,
            titre=doc['titre'].value,
            auteur=doc['auteur'].value,
            editeur=doc['editeur'].value
        )
    elif obj == 'auteur':
        parametres = dict(
            id=doc['id'].value,
            particule=doc['particule'].value,
            nom=doc['nom'].value,
            prenom=doc['prenom'].value,
            titre=doc['titre'].value
        )
    elif obj == 'editeur':
        parametres = dict(
            id=doc['id'].value,
            nom=doc['nom'].value
        )
    if requete(
                '/db/enregistrer/{}'.format(obj),
                methode='PUT',
                parametres=parametres
            ) == 'OK':
        alert('Modifications enregistrées.')
    else:
        alert('Il y a eu une erreur.')


def formulaire(obj, donnees):
    bouton = BUTTON('Filtrer')
    bouton.bind(
        'click',
        lambda ev: charger_liste(
            ev, obj, actualiser=True,
            criteres={donnee[1]: doc[donnee[1]].value for donnee in donnees}
        )
    )
    return (
        tableau(
            [
                [donnee[0], INPUT(
                    type='text', name=donnee[1], id=donnee[1]
                )] for donnee in donnees
            ],
            entete=False, trier=False
        ) +
        bouton
    )


def tableau_dict(
    colonnes, donnees, entete=True, trier=True, obj='ouvrages'
):
    titres = TR()
    if entete:
        for colonne in colonnes:
            if colonne[1]:
                titre = A(colonne[0], href='#')
                titre.bind(
                    'click',
                    lambda ev, col=colonne[1]:
                        charger_liste(ev, obj, col, actualiser=False)
                )
            else:
                titre = P(colonne[0])
            titres <= TH(titre.clone())
    if trier:
        donnees = donnees if ASC else reversed(donnees)
    corps = TBODY()
    for element in donnees:
        lgn = TR()
        for colonne in colonnes:
            if 'id' in element:
                lien = '{}:{}'.format(obj, element['id'])
                cel = A(element[colonne[1]], href='#' + lien)
                cel.bind(
                    'click',
                    lambda ev, col=lien: charger(ev, col)
                )
            else:
                cel = element[colonne[1]]
            lgn <= TD(cel)
        corps <= lgn
    return TABLE((
        THEAD(titres),
        corps
    ))


def tableau(tbl, entete=True, trier=True):
    titres = TR()
    if entete:
        titres <= TH(P(colonne[0]) for colonne in tbl[0])
        tbl = tbl[1]
    if trier:
        tbl = tbl if ASC else reversed(tbl)
    corps = TBODY()
    for ligne in tbl:
        lgn = TR()
        for cellule in ligne:
            if isinstance(cellule, list):
                cel = A(cellule[0], href='#{}'.format(cellule[1]))
                cel.bind(
                    'click',
                    lambda ev, col=cellule[1]: charger(ev, col)
                )
            else:
                cel = cellule
            lgn <= TD(cel)
        corps <= lgn
    return TABLE((
        THEAD(titres),
        corps
    ))


menu()
doc['cacher'].bind('click', menu_cacher)
charger_liste(None, 'ouvrages', 'titre')
