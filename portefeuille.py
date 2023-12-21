""" PorteFeuille.py """
import datetime
from exceptions import ErreurDate, ErreurQuantité, LiquiditéInsuffisante

class Portefeuille:
    """Classe portefeuille"""

    def __init__(self, bourse):
        """Fonction init"""
        self.bourse = bourse
        self.liquidités = 0
        self.titres = {}

    def déposer(self, montant, date=None):
        """Fonction déposer"""
        if date is None:
            date = datetime.date.today()

        self.liquidités += montant

    def solde(self, date=None):
        """Fonction solde"""
        if date is None:
            date = datetime.date.today()

        if date > datetime.date.today():
            raise ErreurDate("La date d'évaluation doit être aujourd'hui ou dans le passé.")

        return self.liquidités

    def acheter(self, symbole, quantité, date=None):
        """Fonction acheter"""
        if date is None:
            date = datetime.date.today()

        prix_unitaire = self.bourse.prix(symbole, date)
        coût_total = prix_unitaire * quantité

        if coût_total > self.liquidités:
            raise LiquiditéInsuffisante("Liquidités insuffisantes pour effectuer l'achat.")

        self.liquidités -= coût_total
        self.titres.setdefault(symbole, 0)
        self.titres[symbole] += quantité

    def vendre(self, symbole, quantité, date=None):
        """Fonction vendre"""
        if date is None:
            date = datetime.date.today()

        if symbole not in self.titres or self.titres[symbole] < quantité:
            raise ErreurQuantité(f"Quantité insuffisante de {symbole} pour effectuer la vente.")

        prix_unitaire = self.bourse.prix(symbole, date)
        recette_totale = prix_unitaire * quantité

        self.liquidités += recette_totale
        self.titres[symbole] -= quantité

    def valeur_totale(self, date=None):
        """Fonction valeur totale"""
        if date is None:
            date = datetime.date.today()

        total_titres = sum(self.bourse.prix(sym, date) * quant for sym, quant in self.titres.items())
        return self.liquidités + total_titres

    def valeur_des_titres(self, symboles, date=None):
        """Fonction valeur des titres"""
        if date is None:
            date = datetime.date.today()

        if date > datetime.date.today():
            raise ErreurDate("La date d'évaluation doit être aujourd'hui ou dans le passé.")

        valeur_totale_titres = sum(
            self.bourse.prix(sym, date) * quant for sym, quant in self.titres.items() if sym in symboles
        )
        return valeur_totale_titres

    def les_titres(self, date=None):
        """Fonction titres"""
        if date is None:
            date = datetime.date.today()

        if date > datetime.date.today():
            raise ErreurDate("La date d'évaluation doit être aujourd'hui ou dans le passé.")

        return self.titres

    def valeur_projetée(self, date_future, rendement):
        """Fonction valeur projetée"""
        if date_future <= datetime.date.today():
            raise ErreurDate("La date future doit être postérieure à la date actuelle.")

        nb_années = (date_future - datetime.date.today()).days / 365.25

        if isinstance(rendement, float):
            valeur_projetée = self.valeur_totale() * (1 + rendement / 100) ** nb_années
        elif isinstance(rendement, dict):
            valeur_projetée = self.liquidités
            for symbole, quant in self.titres.items():
                rendement_titre = rendement.get(symbole, 0)
                valeur_projetée += (
                    self.bourse.prix(symbole, date_future) * quant * (1 + rendement_titre / 100) ** nb_années
                )
        else:
            raise ValueError(
                "Le rendement doit être soit un nombre à virgule flottante, soit un dictionnaire."
            )

        return valeur_projetée
    