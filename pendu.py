from random import*

def dessinPendu(nb):
    tab=[
    """
       +-------+
       |       |
       |
       |
       |
       |
    ==============
    """
        ,
    """
       +-------+
       |       |
       |       O
       |
       |
       |
    ==============
    """
        ,
    """
       +-------+
       |       |
       |       O
       |       |
       |
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |      -|
       |
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |      -|-
       |
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |      -|-
       |      |
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |      -|-
       |      | |
       |
    ==============
    """
    ]
    return tab[nb]

def restart():
    continuer=input("Voulez-vous faire encore une partie ('y' ou 'n') : ")
    if continuer=='y':
        pendu()
    else:
        exit()

def pendu():
    lettres_utilisees=[]
    mots=[]
    nb_erreurs=0
    with open("dico.txt", "r", encoding="utf-8") as filin:
        for ligne in filin:
            mots.append(ligne)
    for mot in range(len(mots)):
        mots[mot] = mots[mot].rstrip('\n')

    nb=randint(0,len(mots))
    mot_choisi=mots[nb]
    #print(mot_choisi)

    print("JEU DU PENDU")
    #mot_cache ="_ "*len(mot_choisi)
    mot_cache = ["_" for c in range(len(mot_choisi))]
    for i in range(len(mot_cache)-1):
        print(mot_cache[i], end="")
        print(" ", end="")
    print(mot_cache[-1])

    while nb_erreurs<=7:
        lettre=input("Saississez une lettre :")
        if lettre in lettres_utilisees:
            print("Tu as déjà utilisé cette lettre !")
        elif lettre in mot_choisi:
            for i in range(len(mot_choisi)):
                if mot_choisi[i]==lettre:
                    mot_cache[i]=lettre
                    #print(mot_cache)
                    if "_" not in mot_cache:
                        print("Félicitations, vous avez gagné ! Le mot à deviner était " + mot_choisi + ".")
                        restart()
                        #exit()
            #print("ok")
        else:
            print(dessinPendu(nb_erreurs))
            nb_erreurs=nb_erreurs+1
            if nb_erreurs==7:
                print("Vous avez perdu ! Le mot à trouver était : " + mot_choisi + ". Réessayez et peut-être que vous réussirez !")
                restart()
                #exit()
        for i in range(len(mot_cache)-1):
            print(mot_cache[i], end="")
            print(" ", end="")
        print(mot_cache[-1])
        if lettre not in lettres_utilisees:
            lettres_utilisees.append(lettre)

pendu()
