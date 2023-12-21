"""Bourse.py"""
import datetime
import json
import requests
from exceptions import ErreurDate

class Bourse:
    """Classe bourse"""
    def __init__(self):
        """Fonction init"""

    def prix(self, symbole, date):
        """Fonction prix"""
        url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
        params = {'début': date, 'fin': date}

        try:
            réponse = requests.get(url=url, params=params, timeout=10)
            réponse = json.loads(réponse.text)

            if date > datetime.date.today():
                raise ErreurDate("La date spécifiée est postérieure à la date du jour.")

            élément_plus_récent = max(
                (el for el in réponse["historique"].items() if el[0] <= str(date)),
                default=None
            )

            if élément_plus_récent:
                return élément_plus_récent[1]["fermeture"]

            raise ErreurDate(
                f"Aucune donnée disponible pour le symbole {symbole} à la date spécifiée {date}."
            )

        except requests.RequestException as e:
            print(f"Erreur de requête : {e}")
            return None
        