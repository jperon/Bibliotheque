#!/usr/bin/env python3

from functools import wraps
import json

from etc import cfg
from c import controleur as ctl
from c import db_gavage
from v import bottle as b

b.TEMPLATE_PATH = [cfg['html']['Modeles']]
rq = b.request
APP = b.Bottle()


@APP.hook('before_request')
def strip_path():
    """Effacement du / final s'il y en a un dans l'url
    """
    rq.environ['PATH_INFO'] = rq.environ['PATH_INFO'].rstrip('/')


def page(fonction):
    """Pages simples

    Cette fonction est un décorateur à appliquer aux fonctions retournant
    simplement du contenu, sans paramètre ésotérique
    """
    @wraps(fonction)
    def afficher(*arguments, **parametres):
        """Décorateur
        """
        corps = fonction(*arguments, **parametres)
        return b.template('page', {'corps': corps})
    return afficher


@APP.get('/')
@page
def index():
    with open(cfg['html']['Pages'] + '/index.html', 'r') as f:
        contenu = f.read()
    return contenu


@APP.get('/db/liste/<objet>')
@APP.get('/db/liste/<objet>/<tri>')
def liste_ouvrages(**params):
    return json.dumps(ctl.liste(**params))


@APP.get('/db/ouvrage/<id>')
def ouvrage(id):
    return json.dumps(ctl.ouvrage(id))


@APP.get('/db/auteur/<id>')
def auteur(id):
    return json.dumps(ctl.auteur(id))


@APP.get('/db/editeur/<id>')
def editeur(id):
    return json.dumps(ctl.editeur(id))


@APP.post('/db/enregistrer/<obj>')
def enregistrer(obj):
    ctl.enregistrer(obj, rq.forms.decode())
    return('OK')


@APP.get('/static/<chemin:path>')
def static(chemin):
    return b.static_file(chemin, root='./v/static')


if __name__ == '__main__':
    if bool(cfg['general']['Debug']):
        b.debug(True)
        b.run(app=APP, host=cfg['server']['Hote'], port=cfg['server']['Port'])
    else:
        from deps.wsgiserver import WSGIServer
        SERVER = WSGIServer(
            APP,
            host=cfg['server']['Hote'],
            port=cfg['server']['Port'],
            server_name='Bibliotheque',
            numthreads=30
        )
        SERVER.start()
