# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8


def tranche_0(r, n):
    """
    :param r: revenu net imposable
    :param n: nombre de parts
    :return:
    """
    return 0


def tranche_14(r, n):
    """
    :param r: revenu net imposable
    :param n: nombre de parts
    :return:
    """
    return r*0.14 - 1359.4*n


def tranche_30(r, n):
    """
    :param r: revenu net imposable
    :param n: nombre de parts
    :return:
    """
    return r*0.3 - 5650.28*n


def tranche_41(r, n):
    """
    :param r: revenu net imposable
    :param n: nombre de parts
    :return:
    """
    return r*0.41 - 13559.06*n


def tranche_45(r, n):
    """
    :param r: revenu net imposable
    :param n: nombre de parts
    :return:
    """
    return r*0.45 - 19649.46*n


TRANCHES = {9710: tranche_0,
            26818: tranche_14,
            71898: tranche_30,
            152260: tranche_41,
            float("inf"): tranche_45}


def calcul_impot(revenu, nb_parts):
    """
    :param revenu: revenu net imposable
    :param nb_parts: nombre de parts
    :return:
    """
    revenu_par_personne = float(revenu)/nb_parts
    for tranche in sorted(TRANCHES.keys()):
        if revenu_par_personne < tranche:
            return TRANCHES[tranche](revenu, nb_parts)


if __name__ == "__main__":
    print calcul_impot(5, 1)
    print calcul_impot(22632, 1)
    print calcul_impot(25000, 1)
    print calcul_impot(100000, 1)
    print calcul_impot(100000, 2)
    print calcul_impot(5, 1)
    print calcul_impot(revenu=85000,
                       nb_parts=2)

    # with open("impots.csv", 'w') as fichier:
    #     fichier.write("revenu fiscal;impot seul;impot a 2;impot a 3;impot a 7\n")
    #     for revenu_fiscal_de_reference in xrange(200000):
    #         fichier.write("{revenu};{impot_seul};{impot_a_2};{impot_a_3};{impot_a_7}\n"
    #                       .format(revenu=revenu_fiscal_de_reference,
    #                               impot_seul=calcul_impot(revenu_fiscal_de_reference, 1),
    #                               impot_a_2=calcul_impot(revenu_fiscal_de_reference, 2),
    #                               impot_a_3=calcul_impot(revenu_fiscal_de_reference, 3),
    #                               impot_a_7=calcul_impot(revenu_fiscal_de_reference, 7)))
