import abc

from Remy import Signal


class Parser(object):
    def __init__(self, path_to_input_file):
        self.filepath = path_to_input_file
        self.signaux = []

    def parse_file(self):
        fichier_brut = []
        with open(self.filepath, "r") as fichier:
            for ligne in fichier.readlines():
                fichier_brut.append(ligne.replace("\n", ""))

        self.analyse_fichier(fichier_brut)

    @abc.abstractmethod
    def analyse_fichier(self, raw):
        pass


class RemyParser(Parser):

    def analyse_fichier(self, raw):
        signal = []
        signaux = []
        for ligne_raw in raw:
            if ligne_raw.strip() and len(ligne_raw) > 5:
                ligne_raw = ligne_raw[5:52]
                ligne_raw = ligne_raw.strip()
                ligne_raw = ligne_raw.split(" ")
                signal.extend(ligne_raw)
            else:
                if signal:
                    self.supprimer_10(signal)
                    self.signaux.append(Signal.Signal(signal))
                    signal = []

    def supprimer_10(self, signal):
        pass



