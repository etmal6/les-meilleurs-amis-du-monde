# bourse.py
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

# exceptions.py
class SoldeInsuffisant(Exception):
    pass

# portefeuille.py
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

    def lister(self, date, titres=None):
        if not titres:
            titres = self.actions.keys()

        for titre in titres:
            if titre in self.actions:
                quantite = self.actions[titre]
                prix_unitaire = 10  # Remplacez par le vrai mécanisme pour obtenir le prix du titre
                montant = quantite * prix_unitaire
                print(f"{titre} = {quantite} x {prix_unitaire} = {montant:.2f}")

    def projeter(self, date, rendement, volatilite, titres=None):
        if not titres:
            titres = self.actions.keys()

        for titre in titres:
            if titre in self.actions:
                quantite = self.actions[titre]
                prix_unitaire = 10  # Remplacez par le vrai mécanisme pour obtenir le prix du titre
                valeur_actuelle = quantite * prix_unitaire
                q1, q2, q3 = Bourse.calculer_projections(rendement, volatilite)
                valeur_projete = valeur_actuelle * q2  # Utilisation de la médiane pour la projection
                print(f"valeur projetée = {valeur_projete:.2f}")

    def sauvegarder(self):
        data = {
            "nom_portefeuille": self.nom_portefeuille,
            "solde": self.solde,
            "actions": self.actions
        }
        with open(f"{self.nom_portefeuille}.json", "w") as f:
            json.dump(data, f)

    def charger(self):
        try:
            with open(f"{self.nom_portefeuille}.json", "r") as f:
                data = json.load(f)
                self.nom_portefeuille = data["nom_portefeuille"]
                self.solde = data["solde"]
                self.actions = data["actions"]
        except FileNotFoundError:
            pass  # Fichier non trouvé, le portefeuille est initialement vide

# portefeuille_graphique.py
from portefeuille import Portefeuille
import matplotlib.pyplot as plt

class PortefeuilleGraphique(Portefeuille):
    def lister_graphique(self, date, titres=None):
        # Implémentation de l'affichage graphique de l'historique des valeurs
        pass

    def projeter_graphique(self, date, rendement, volatilite, titres=None):
        # Implémentation de l'affichage graphique de la projection
        pass

# gesport.py
import argparse
from portefeuille import Portefeuille
from portefeuille_graphique import PortefeuilleGraphique

def analyser_commande():
    parser = argparse.ArgumentParser(description="Gestionnaire de portefeuille d'actions")
    subparsers = parser.add_subparsers(dest="action", help="Actions disponibles")

    # Parser pour la commande "déposer"
    parser_deposer = subparsers.add_parser("deposer", help="Déposer la quantité de dollars spécifiée")
    parser_deposer.add_argument("--date", "-d", help="Date spécifiée", required=True)
    parser_deposer.add_argument("--quantite", "-q", type=float, help="Quantité spécifiée", default=1)

    # Parser pour la commande "acheter"
    parser_acheter = subparsers.add_parser("acheter", help="Acheter la quantité spécifiée des titres spécifiés")
    parser_acheter.add_argument("--date", "-d", help="Date spécifiée", required=True)
    parser_acheter.add_argument("--titres", "-t", nargs="+", help="Titres spécifiés", required=True)
    parser_acheter.add_argument("--quantite", "-q", type=float, help="Quantité spécifiée", default=1)

    # Parser pour la commande "vendre"
    parser_vendre = subparsers.add_parser("vendre", help="Vendre la quantité spécifiée des titres spécifiés")
    parser_vendre.add_argument("--date", "-d", help="Date spécifiée", required=True)
    parser_vendre.add_argument("--titres", "-t", nargs="+", help="Titres spécifiés", required



# portefeuille_graphique.py
from portefeuille import Portefeuille
import matplotlib.pyplot as plt
import numpy as np

class PortefeuilleGraphique(Portefeuille):
    def lister_graphique(self, date, titres=None):
        if not titres:
            titres = self.actions.keys()

        for titre in titres:
            if titre in self.actions:
                historique = self._generer_historique(titre, date)
                self._afficher_graphique(historique, f'Historique de {titre}')

    def projeter_graphique(self, date, rendement, volatilite, titres=None):
        if not titres:
            titres = self.actions.keys()

        projections = {}
        for titre in titres:
            if titre in self.actions:
                historique = self._generer_historique(titre, date)
                projections[titre] = self._generer_projection(historique, rendement, volatilite)

        self._afficher_projection_graphique(projections)

    def _generer_historique(self, titre, date):
        # Implémentation de la génération de l'historique
        # Note : ceci est une simplification, remplacez-le par une logique basée sur les transactions réelles
        prix_unitaire = 10  # Remplacez par le vrai mécanisme pour obtenir le prix du titre
        historique = [(date, self.actions[titre] * prix_unitaire)]
        return historique

    def _afficher_graphique(self, historique, titre):
        dates, valeurs = zip(*historique)
        plt.plot(dates, valeurs, label=titre)

    def _generer_projection(self, historique, rendement, volatilite):
        dernier_moment = historique[-1][0]
        proj_dates = np.arange(dernier_moment, dernier_moment + 365, 3)
        proj_rendements = np.random.normal(rendement, volatilite, len(proj_dates))
        proj_valeurs = historique[-1][1] * np.cumprod(1 + proj_rendements)
        return list(zip(proj_dates, proj_valeurs))

    def _afficher_projection_graphique(self, projections):
        for titre, projection in projections.items():
            self._afficher_graphique(projection, f'Projection de {titre}')

        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Valeur')
        plt.title('Projections des titres')
        plt.show()
