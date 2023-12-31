import numpy as np

class Bourse:
    @staticmethod
    def calculer_projections(rendement, volatilite):
        # Implémentation de la projection avec volatilité
        np.random.seed(42)  # Pour la reproductibilité des résultats
        rendements = np.random.normal(rendement, volatilite, 1000)
        projections = np.cumprod(1 + rendements)
        quartiles = np.percentile(projections, [25, 50, 75])
        return tuple(quartiles)

class SoldeInsuffisant(Exception):
    pass

import json
from exceptions import SoldeInsuffisant

class Portefeuille:
    def __init__(self, nom_portefeuille="folio"):
        self.nom_portefeuille = nom_portefeuille
        self.solde = 0
        self.actions = {}

    def deposer(self, date, montant):
        self.solde += montant
        print(f"solde = {self.solde:.2f}")

    def acheter(self, date, titres, quantite):
        # Simplification : on suppose que les titres ont un prix unitaire fixe
        prix_unitaire = 10  # Remplacez par le vrai mécanisme pour obtenir le prix du titre
        cout_total = quantite * prix_unitaire

        if self.solde < cout_total:
            raise SoldeInsuffisant("Solde insuffisant pour effectuer l'achat.")

        if titres not in self.actions:
            self.actions[titres] = 0

        self.actions[titres] += quantite
        self.solde -= cout_total
        print(f"solde = {self.solde:.2f}")

    def vendre(self, date, titres, quantite):
        # Simplification : on suppose que les titres ont un prix unitaire fixe
        prix_unitaire = 10  # Remplacez par le vrai mécanisme pour obtenir le prix du titre

        if titres not in self.actions or self.actions[titres] < quantite:
            raise ValueError("Vous ne possédez pas suffisamment d'actions pour effectuer la vente.")

        montant_total = quantite * prix_unitaire
        self.actions[titres] -= quantite
        self.solde += montant_total
        print(f"solde = {self.solde:.2f}")
