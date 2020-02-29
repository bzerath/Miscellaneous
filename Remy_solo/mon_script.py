import abc


class Signal(object):
    def __init__(self, signal):
        self.signal = signal

    @property
    def header(self):
        return self.signal[:9]

    @property
    def footer(self):
        return self.signal[-5:]

    @property
    def body(self):
        return self.signal[9:-5]

    @property
    def size(self):
        return int("".join(self.header[1:5]), 16)


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
        for ligne_raw in raw:
            if len(ligne_raw) > 5:
                ligne_raw = ligne_raw[5:52]
                ligne_raw = ligne_raw.strip()
                ligne_raw = ligne_raw.split(" ")
                signal.extend(ligne_raw)
            else:
                if signal:
                    self.supprimer_10(signal)
                    self.signaux.append(Signal(signal))
                    signal = []

    def supprimer_10(self, signal):
        pass


if __name__ == "__main__":
    """
    input.txt doit ressembler à ça :

0000 02 00 00 00 2C 53 53 54 10 03 00 00 00 01 01 56 ....xsqsdfsqdqds.....
0010 00 00 00 00 00 00 00 00 10 02 56 00 00 00 00 00 sdf.dsfs..f*dsfsdfsdf
0020 00 00 00 10 03 44 00 00 00 00 00 00 10 02 20 03 ... .. . .fd.dffbd. .
0030 

0000 02 00 00 00 2C 53 53 54 10 03 00 00 00 01 01 56 ....xsqsdfsqdqds.....
0010 00 00 00 00 00 00 00 00 10 02 56 00 00 00 00 00 sdf.dsfs..f*dsfsdfsdf
0020 00 00 00 10 03 44 00 00 00 00 00 00 10 02 20 03 ... .. . .fd.dffbd. .
0030

0000 02 00 00 00 2C 53 53 54 10 03 00 00 00 01 01 56 ....xsqsdfsqdqds.....
0010 00 00 00 00 00 00 00 00 10 02 56 00 00 00 00 00 sdf.dsfs..f*dsfsdfsdf
0020 00 00 00 10 03 44 00 00 00 00 00 00 10 02 20 03 ... .. . .fd.dffbd. .
0030
    """
    mon_fichier = RemyParser("input.txt")

    mon_fichier.parse_file()

    for s in mon_fichier.signaux:
        print(s.size, s.header, s.body, s.footer)
