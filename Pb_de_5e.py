def check_triangle(a, b, c):
    if a + b + c > 20:
        return False
    if a >= b+c or b >= a+c or c >= a+b:
        return False
    else:
        return True


if __name__ == "__main__":
    resultat = set([tuple(sorted((A, B, C)))
                    for A in range(1, 20)
                    for B in range(1, 20)
                    for C in range(1, 20)
                    if A+B+C <= 20 and not (A >= B+C or B >= A+C or C >= A+B)])
    print(sorted(resultat))
    print("Il y a {} résultats trouvés !".format(len(set(resultat))))
