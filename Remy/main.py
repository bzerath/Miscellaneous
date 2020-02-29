from Remy import Parser


if __name__ == "__main__":
    mon_fichier = Parser.RemyParser("input.txt")

    mon_fichier.parse_file()

    for signal in mon_fichier.signaux:
        print(signal.header, signal.body, signal.footer)
