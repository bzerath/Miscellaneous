# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8
import psycopg2
import datetime
import ConfigParser
from time import strftime, localtime, strptime, time
from subprocess import CalledProcessError, check_output
import sys
import Tkinter as tk

def requete_complete(path_fichier_de_conf, requete_a_lancer):
    """
    Lance une requête, incluant l'ouverture de connexion
    Renvoie "" si la requête ne renvoie rien.

    :param path_fichier_de_conf: chemin vers le fichier de configuration
    :param requete_a_lancer: Requête à exécuter

    """

    # Lit le fichier de config
    cfg = ConfigParser.RawConfigParser()
    cfg.read(path_fichier_de_conf)

    # Cherche dans le fichier de config les identifiants dans la section "bdd"
    host = cfg.get("bdd", "host")
    dbname = cfg.get("bdd", "dbname")
    user = cfg.get("bdd", "user")
    password = cfg.get("bdd", "password")

    # Ouvre la connexion
    conn = psycopg2.connect(
        "host={host} dbname={db_name} user={user} password={password}"
        .format(host=host, db_name=dbname, user=user, password=password))

    # Crée un objet "cursor", qui permet l'héberger une requête
    cur = conn.cursor()

    # Exécute la requête
    cur.execute(requete_a_lancer)

    # Réceptionne le résultat.
    # Soit la requête renvoie quelque chose, auquel cas on fait un fetchall()
    #  --> renvoie un tableau, même si on n'a qu'un seul résultat
    # Soit ça renvoie rien (c'est normal si on fait genre un insert par exemple)
    #  --> on capture une erreur et on renvoie du vide
    try:
        all = cur.fetchall()
    except psycopg2.ProgrammingError as e:
        all = ""

    # On ferme le curseur
    cur.close()

    # On commit les résultats sur la connexion (sinon ça a servi à rien)
    conn.commit()

    # On déconnecte
    conn.close()

    # Et on renvoie le résultat
    return all


def fancy_time():
    """
    :return: Renvoie la date sous la forme "AAAA-MM-JJ_HH-MM-SS"
    """
    return strftime("date '%Y-%m-%d' + time '%H:%M'",localtime())


def run_cmd(args):
    """
    Runs the command.
    >>> run_cmd(["python", "script.py", "--help"])
    :param args: list of arguments.
    :return:
    """
    result = None
    try:
        result = check_output(args)
    except CalledProcessError:
        sys.stderr.write("The command {arg} returned a non-zero exit status !")
    return result


def date_du_jour():
    mois_lettres_chiffres = {1: "janvier",
                         2: "février",
                         3: "mars",
                         4: "avril",
                         5: "mai",
                         6: "juin",
                         7: "juillet",
                         8: "aout",
                         9: "septembre",
                         10: "octobre",
                         11: "novembre",
                         12: "décembre"}
    maintenant = datetime.now()
    jour = maintenant.day
    mois = maintenant.month

    return "{jour} {mois}".format(jour=jour, mois=mois_lettres_chiffres[mois]).encode("utf-8")


class ServerMenu(tk.Toplevel):
    def __init__(self, master, xoffset, height, type_server):
        """
        General class overridding Tkinter.Toplevel, in order to have a vertical scrollbar.
        Contains an instance of ServerFrame, that actually contains the buttons and entries.

            \\\\--> Does not do anything else than getting a scrollbar. <--////

        If you want to add some widgets after the __default__ menu, you shall do something like this:
        >>> class My_Menu:
        >>>    def __init__(self, master, offset):
        >>>        self.menu = ServerMenu(master, offset, "My_Type")    # creates the frame and the default HILC menu
        >>>        self.label = tk.Label(self.menu.frame, text="Note the self.menu.frame as master.")
        >>>        self.label.grid(your_grid_args)
        >>>        self.menu.mainloop()

        :param master: shall be Main.Main()
        :param xoffset:
        :param type_server: "WSIC" or "WSTC"
        :return:
        """
        tk.Toplevel.__init__(self, master)
        self.Type_server = type_server
        width = 400
        # height = ctypes.windll.user32.GetSystemMetrics(1)-50
        yoffset = 0
        self.geometry("%dx%d%+d%+d" % (width, height, xoffset, yoffset))

        self.title('TS-{} Controls'.format(self.Type_server))
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.resizable(False, True)

        self.canvas = tk.Canvas(self)

        # ----  Here is the real frame.  ----
        self.frame = tk.Frame(self.Type_server, self.canvas)
        # ----  -----------------------  ----

        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

    def onFrameConfigure(self, event):
        """
        Reset the scroll region to encompass the inner frame
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onClose(self):
        self.destroy()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta/120), "units")


if __name__ == "__main__":
    pass

