from browser import document, alert, ajax
from browser.html import DIV, TABLE, THEAD, TBODY, TR, TH, TD, A
from markdown import mark as md
from json import loads


def echo(ev):
    # alert(document['zone'].value)
    contenu, scripts = md(document['zone'].value)
    document['contenu'].clear()
    document['contenu'] <= DIV(contenu)


def demander_liste_livres(ev):
    rq = ajax.ajax()
    rq.bind('complete', afficher_tableau)
    rq.open('GET', '/db/liste_ouvrages')
    rq.set_header('content-type', 'application/x-www-form-urlencoded')
    rq.send()


def afficher(contenu):
    document['contenu'].clear()
    document['contenu'] <= DIV(contenu)


def afficher_tableau(rq):
    tbl = loads(rq.text)
    afficher(
        TABLE(
            THEAD(TR(TH(colonne) for colonne in tbl[0])) +
            TBODY(
                TR(
                    TD(A(cellule[0], href=cellule[1]))
                    if isinstance(cellule, list) else
                    TD(cellule)
                    for cellule in ligne
                ) for ligne in tbl[1]
            )
        )
    )


demander_liste_livres(None)
# document['echo'].bind('click', demander_liste_livres)
