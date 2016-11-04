#!/usr/bin/env python3

from etc import cfg
from .peewee import peewee as pw
from .peewee.playhouse.fields import ManyToManyField

pw.ManyToManyField = ManyToManyField
base = pw.SqliteDatabase(cfg['db']['Chemin'].format(cfg['db']['Nom']))


class Table(pw.Model):
    class Meta:
        database = base


class Auteur(Table):
    particule = pw.CharField(null=True)
    nom = pw.CharField()
    prenom = pw.CharField(null=True)
    titre = pw.CharField(null=True)

    class Meta:
        indexes = (
            (('particule', 'nom', 'prenom', 'titre'), True),
        )


class Editeur(Table):
    nom = pw.CharField()

    class Meta:
        indexes = (
            (('nom',), True),
        )


class Ouvrage(Table):
    titre = pw.CharField()
    auteur = pw.ForeignKeyField(Auteur, related_name='ouvrages', null=True)
    editeur = pw.ForeignKeyField(Editeur, related_name='ouvrages')
    auteurs = pw.ManyToManyField(Auteur, related_name='ouvrages')

    class Meta:
        indexes = (
            (('titre', 'auteur', 'editeur'), True),
        )


class Exemplaire(Table):
    ouvrage = pw.ForeignKeyField(Ouvrage, related_name='exemplaires')
    numero = pw.IntegerField()

    class Meta:
        indexes = (
            (('ouvrage', 'numero'), True),
        )


class Volume(Table):
    exemplaire = pw.ForeignKeyField(Exemplaire, related_name='volumes')
    titre = pw.CharField()
    date_acquisition = pw.DateField()
    date_suppression = pw.DateField(null=True)

    class Meta:
        indexes = (
            (('exemplaire', 'titre'), True),
        )


base.connect()
try:
    base.create_tables([
        Auteur, Editeur,
        Ouvrage, Exemplaire, Volume,
        Ouvrage.auteurs.get_through_model(),
    ])
except pw.OperationalError:
    pass
finally:
    base.close()
