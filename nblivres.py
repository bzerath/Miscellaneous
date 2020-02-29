NbLivres, NbJours = [int(a) for a in raw_input("<Nombre de livres> <Nombre de jours> ").split(" ")]
Empreintable = [0]*NbLivres

for jour in range(NbJours):
    for nblivre in range(NbLivres):
        if Empreintable[nblivre] > 0:
            Empreintable[nblivre] -= 1

    clients = int(input("Nombres de clients pour aujourd'hui : "))
    for client in range(clients):
        Num, Dur = [int(a) for a in raw_input("Demande du client #{} : ".format(client)).split(" ")]
        if Empreintable[Num] > 0:
            print 0
            continue
        else:
            Empreintable[Num] = Dur
            print 1
            continue
