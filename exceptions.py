""" Prise en charge des exeptions """
class ErreurDate(RuntimeError):
    """ Classe erreur date """

class ErreurQuantité(RuntimeError):
    """ Classe erreur quantité """

class LiquiditéInsuffisante(RuntimeError):
    """ Classe manque de liquidité """
    