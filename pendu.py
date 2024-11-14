# Importation des modules nécessaires au fonctionnement du programme
from random import randint
from time import sleep
import tkinter as tk
from tkinter import messagebox
from tkhtmlview import HTMLLabel
import webbrowser
import urllib.request
import os
import platform
import csv

# Importation du mixeur de "Pygame" et suppression de son message de bienvenue dans la console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

OS_PLATFORM = platform.system();
if OS_PLATFORM == 'Windows':
    DIRECTORY_SEP = "\\"
else:
    DIRECTORY_SEP = "/"

# Initialisation du mixeur de pygame
mixer.init()

# Création de la fenêtre
fenetre=tk.Tk()
fenetre.title("Le jeu du pendu")
if OS_PLATFORM == 'Windows':
    fenetre.iconbitmap("icone.ico")
else:
    fenetre.iconbitmap("@./icone.xbm")

fenetre.minsize(1000, 600)
fenetre.geometry("1000x600")
frame = tk.Frame(fenetre)

version = open("last_version.txt", "r", encoding="utf-8")
pendu_version = version.read()[:-1]
version.close()

if OS_PLATFORM == 'Windows':
    dir = os.getenv('APPDATA')+"\\Jeu du pendu\\"
    if os.path.exists(dir) == False:
        os.makedirs(dir)
    file_name = "score.csv"
else:
    dir = os.getenv('HOME') + "/"
    file_name = ".pendu_score.csv"
global best_scores
if os.path.exists(dir + file_name) == False:
    fichier = open(dir + file_name, "w", encoding="utf-8")
    fichier.write("normal,difficile,aveulge,grec\n0,0,0,0")
    fichier.close()
    best_scores = {'normal' : 0, 'difficile' : 0, 'aveugle' : 0, 'grec' : 0}
else:
    fichier = open(dir + file_name, "r", encoding="utf-8")
    best_scores = list(csv.DictReader(fichier))[0]
    fichier.close()

def ecrire_best_score(reset, mode):
    if platform == 'Windows':
        location = os.getenv('APPDATA')+"\\Jeu du pendu\\score.csv"
    else:
        location = "~/.pendu_score.csv"
    fichier = open(location, "w", encoding="utf-8")
    if reset:
        best_scores[mode] = 0;
        messagebox.showinfo(f'Meilleur score {mode}', f'Le meilleur score {mode} a été réinitialisé et est maintenant de : {best_scores[mode]}.')
    ecrire = csv.writer(fichier)
    ecrire.writerow(best_scores[0].keys)
    ecrire.writerow(best_scores[1].values)
    fichier.close()
                        
def afficher_best_score(mode):
    messagebox.showinfo(f'Meilleur score {mode}', f'Le meilleur score {mode} est de : {best_scores[mode]}.')

# Création des scores pour les différents modes
scores = {'normal' : 0, 'difficile' : 0, 'aveugle' : 0, 'grec' : 0}

class Window(tk.Toplevel):
    """Permet de créer une sous-fenêtre pour l'aide ou les notes de mises à jour par exemple"""
    def __init__(self, parent):
        super().__init__(parent)
    
    def titre_icone(self, titre):
        self.title(titre)
        if OS_PLATFORM == 'Windows':
            self.iconbitmap("icone.ico")
        else:
            self.iconbitmap("@./icone.xbm")
        self.minsize(600,500)
        self.geometry("600x500")
    
    def main_titre(self, texte):
        title = tk.Label(self, text=texte, font=("Calibri", 40, "bold", "underline"), fg="black")
        title.pack(side="top")
        close=tk.Button(self, text="Fermer", font=("Calibri", 13), bg="lightblue", cursor="hand2", bd=1, pady=0, command=lambda:self.destroy())
        close.pack(side="bottom")
        close.bind_all("<space>", lambda x: self.destroy())

    def contenu(self, texte):
        S = tk.Scrollbar(self)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        html = HTMLLabel(self, html=texte)
        html.pack(padx=20, pady=0)
        S.config(command=html.yview)
        html.config(yscrollcommand=S.set)

    def lancer(self):
        self.wm_resizable(0, 0)
        self.grab_set()

def update():
    """Crée une sous-fenêtre à l'aide de la classe Window pour afficher les notes de mises à jour"""
    fichier = open(f"text{DIRECTORY_SEP}update.html", "r", encoding="utf-8")
    texte_update = fichier.read()
    fichier.close()

    update = Window(fenetre)
    update.titre_icone("Notes de mises à jour")
    update.main_titre("Notes de mises à jour")
    update.contenu(texte_update)
    update.lancer()

def help():
    """Crée une sous-fenêtre à l'aide de la classe Window pour afficher l'aide du jeu du pendu"""
    fichier = open(f"text{DIRECTORY_SEP}help.html", "r", encoding="utf-8")
    texte_help = fichier.read()
    fichier.close()

    help = Window(fenetre)
    help.titre_icone("Aide du jeu du pendu")
    help.main_titre("Aide du jeu du pendu")
    help.contenu(texte_help)
    help.lancer()

def contributeurs():
    """Crée une sous-fenêtre à l'aide de la classe Window pour afficher les contributeurs du jeu du pendu"""
    fichier = open(f"text{DIRECTORY_SEP}contributors.html", "r", encoding="utf-8")
    texte_contributeurs = fichier.read()
    fichier.close()

    contributeurs = Window(fenetre)
    contributeurs.titre_icone("Contributeurs")
    contributeurs.main_titre("Contributeurs")
    contributeurs.contenu(texte_contributeurs)
    contributeurs.lancer()

# Configuration de la barre de menus, avec sous-menus et raccourcis claviers
menu_bar = tk.Menu(fenetre)
file_menu = tk.Menu(menu_bar, tearoff=0)

#file_menu.add_command(label="Nouvelle partie", command=lambda:preinitialisation())
menu_normal = tk.Menu(menu_bar, tearoff=0)
menu_normal.add_command(label="Voir le meilleur score", command=lambda:afficher_best_score('normal'))
menu_normal.add_command(label="Réinitialiser le meilleur score", command=lambda:ecrire_best_score(True, 'normal'))
file_menu.add_cascade(label="Mode normal", underline=0, menu=menu_normal)

menu_aveugle = tk.Menu(menu_bar, tearoff=0)
menu_aveugle.add_command(label="Voir le meilleur score aveugle", command=lambda:afficher_best_score('aveugle'))
menu_aveugle.add_command(label="Réinitialiser le meilleur score auveugle", command=lambda:ecrire_best_score(True, 'aveugle'))
file_menu.add_cascade(label="Mode aveugle", underline=0, menu=menu_aveugle)

menu_grec = tk.Menu(menu_bar, tearoff=0)
menu_grec.add_command(label="Voir le meilleur score grec", command=lambda:afficher_best_score('grec'))
menu_grec.add_command(label="Réinitialiser le meilleur score grec", command=lambda:ecrire_best_score(True, 'grec'))
file_menu.add_cascade(label="Mode grec", underline=0, menu=menu_grec)

menu_diff = tk.Menu(menu_bar, tearoff=0)
menu_diff.add_command(label="Voir le meilleur score difficile", command=lambda:afficher_best_score('difficile'))
menu_diff.add_command(label="Réinitialiser le meilleur score difficile", command=lambda:ecrire_best_score(True, 'difficile'))
file_menu.add_cascade(label="Mode difficile", underline=0, menu=menu_diff)

file_menu.add_separator()
file_menu.add_command(label="Quitter", accelerator="CTRL+Q", command=lambda:on_close())
menu_bar.add_cascade(label="Fichier", menu=file_menu)
menu_bar.bind_all("<Control-q>", lambda x: on_close())

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Aide du jeu", accelerator="F1", command=lambda:help())
help_menu.add_command(label="Notes de mises à jour", command=lambda:update())
help_menu.add_command(label="Contributeurs", command=lambda:contributeurs())
help_menu.add_separator()
help_menu.add_command(label="Dépôt GitHub", command=lambda:open_link('https://github.com/Androl404/pendu_tk'))
help_menu.add_command(label="Vérifier les mises à jour", command=lambda:verify_update())
help_menu.add_separator()
help_menu.add_command(label="À propos", command=lambda:about())
menu_bar.add_cascade(label="Aide", menu=help_menu)
menu_bar.bind_all("<F1>", lambda x: help())

def open_link(link):
    """Ouvre un lien dans le navigateur Web par défaut"""
    webbrowser.open(link)

def verify_update():
    """Vérifie les mises à jour du Jeu du pendu en récupérant un fichier texte sur GitHub"""
    file = []
    try:
        for line in urllib.request.urlopen('https://raw.githubusercontent.com/Androl404/pendu_tk/master/last_version.txt'):
            file.append(line.decode('utf-8'))
    except:
        messagebox.showwarning('Vérification des mises à jour', 'La vérification des mises à jour a échoué.\nVeuillez vérifier votre connexion Internet et réessayer !')
    if len(file) != 0:
        if file[0][:-1] == pendu_version:
            messagebox.showinfo('Vérification des mises à jour', f'Vous êtes bien sur la dernière version du jeu du pendu : {file[0][:-1]}.')
        else:
            messagebox.showinfo('Vérification des mises à jour', f'Une mise à jour vers la version {file[0][:-1]} est disponible.\nVous pouvez la télécharger depuis le dépôt GitHub.\nVous êtes actuellement sur la version {pendu_version}.')

def play_music(music, loops):
    """Joue la musique donné en paramètre. Possibilité de jouer une musique en boucle."""
    mixer.music.load(music)
    if loops == True:
        mixer.music.play(loops=-1)
    else:
        mixer.music.play()

def stop_music():
    """Arrête n'importe quel musique en train de jouer sur Pygame"""
    mixer.music.stop()

def about():
    """Définit le message à propos des auteurs."""
    lines = ['Jeu du pendu', 'Développé par Andrei Zeucianu','Merci aux contributeurs ❤' , 'Copyright 2024, Tous droits réservés', f'Version {pendu_version} (Stable)']
    messagebox.showinfo('À propos de ce jeu', "\n".join(lines))

def on_close():
    """Demande une confirmation à la fermeture de la fenêtre."""
    response=messagebox.askyesno("Fermeture de l'application",'Voulez-vous vraiment quitter le jeu du pendu ?')
    if response:
        fenetre.quit()

def create_mots_utilisees():
    """Crée la liste de mots utilisées pour éviter d'avoir plusieurs fois le mêmes mot en une seule partie. Se réinitialise à cause lancement du jeu du pendu."""
    global mots_utilisees 
    mots_utilisees = []

def texte_principal(color, first):
    """Création du texte principal selon la couleur et l'avancée de l'utilisateur dans le jeu"""
    global label
    if first == False:
        label.destroy()
    if color == 'grec':
        label=tk.Label(frame, text="Le jeu du pendu", font=("Castellar", 48), pady=30)
    elif color != 'black' :
        label=tk.Label(frame, text="Le jeu du pendu", font=("Calibri", 48, "bold"), pady=30, fg=color)
    else:
        label=tk.Label(frame, text="Le jeu du pendu", font=("Calibri", 48), pady=30, fg=color)
    label.pack(side="top")
texte_principal('black', True)

def autres_modes():
    global button_play, espace_bouton, button_mode, button_play_diff, button_play_aveugle, button_play_grec, button_main_menu, canvas_bouton
    canvas_bouton.destroy()
    canvas_bouton = tk.Canvas(frame)
    canvas_bouton.pack(side="top")
    button_play_aveugle=tk.Button(canvas_bouton, text="Mode Aveugle", font=("Consolas", 24),bg="white", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(False, "aveugle")])
    button_play_aveugle.pack(side="top")
    button_play_grec=tk.Button(canvas_bouton, text="Mode Grec", font=("Castellar", 24),bg="#e5e5e5", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(False, 'grec')])
    button_play_grec.pack(side="top")
    button_play_diff=tk.Button(canvas_bouton, text="Mode Difficile", font=("Algerian", 24),bg="red", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(False, "diff")])
    button_play_diff.pack(side="top")
    espace_bouton=tk.Canvas(canvas_bouton, height="30")
    espace_bouton.pack(side="top")
    button_main_menu=tk.Button(canvas_bouton, text="Retour au menu principal", font=("Arial", 15), cursor="hand2", bg="#fff", padx="20", command=lambda:return_main_menu(False))
    button_main_menu.pack(side="top")

def return_main_menu(first):
    global button_play_aveugle, button_play_grec, button_play_diff, espace_bouton, button_main_menu, button_mode, button_play, canvas_bouton
    if not first :
        canvas_bouton.destroy()
    canvas_bouton = tk.Canvas(frame)
    canvas_bouton.pack(side="top")
    button_play=tk.Button(canvas_bouton, text="Jouer", font=("Calibri", 36), bg="lightgreen", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(False, "normal")])
    button_play.pack(side="top")
    espace_bouton=tk.Canvas(canvas_bouton, height="30")
    espace_bouton.pack(side="top")
    button_mode=tk.Button(canvas_bouton, text="Autres modes...", font=("Arial", 15), cursor="hand2", bg="#fff", padx="20", command=lambda:autres_modes())
    button_mode.pack(side="top")

def button(pre):
    """Création du bouton principal pour lancer le jeu, fonction de retour au menu principal et lancement de la musique du menu principal"""
    global button_play, espace_bouton, button_mode, canvas_bouton
    fenetre.configure(bg='#f0f0f0')
    frame.configure(bg='#f0f0f0')
    if pre==True:
        label_score.destroy()
        canvas_rejouer.destroy()
        label_rejouer.destroy()
        mot_cache_label.destroy()
        canvas_dessin.destroy()
    return_main_menu(True)
    play_music(f"music{DIRECTORY_SEP}Menu.mp3", True)
button(False)
create_mots_utilisees()

def fond_color(color):
    """Applique la couleur de fond donné en paramètre à tous les éléments de la partie pour permettre un changement d'ambiance."""
    fenetre.configure(bg=color)
    frame.configure(bg=color)
    label.configure(bg=color)
    canvas_dessin.configure(bg=color)
    mot_cache_label.configure(bg=color)

def choix_mot(file):
    """Fonction qui permet de choisir le mot qui va être caché."""
    global mot_choisi, mots_utilisees    
    mots=[]
    with open(file, "r", encoding="utf-8") as filin:
        for ligne in filin:
            mots.append(ligne)
    for mot in range(len(mots)):
        mots[mot] = mots[mot].rstrip('\n')
    #print(mots)
    nb=randint(0,len(mots)-1)
    mot_choisi=mots[nb]
    if mot_choisi not in mots_utilisees:
        mots_utilisees.append(mot_choisi)
    else:
        choix_mot(file)
    if len(mots_utilisees)>=190:
        create_mots_utilisees()

def pendu0():
    """Détruit le bouton de départ, initialise le canvas pour les images du pendu et affiche la première image du pendu."""
    global canvas_dessin, img, button_play, button_play_diff, button_play_aveugle, button_play_grec
    img = tk.PhotoImage(file=f"pendu_img{DIRECTORY_SEP}pendu0.png")
    (l,h)=(img.width(),img.height())
    canvas_dessin = tk.Canvas(frame, width=l, height=h)
    canvas_dessin.create_image(l/2, h/2, image=img)
    canvas_dessin.pack(side="top")

def creation_bouton():
    """Crée un canvas avec tous les boutons avec les lettres de l'alphabet latin ou grec selon le mode pour pouvoir jouer au pendu."""
    global bouton, alphabet_frame, canvas_alphabet, nombre_lettre_trouvees, mode
    canvas_alphabet = tk.Canvas(frame, width=720, height=40)
    start, end = 65, 91
    if mode == 'grec':
        start, end = 945, 970
    lettres = [chr(i) for i in range(start, end)]
    for i in range(len(lettres)):
        bouton = tk.Button(canvas_alphabet, text=lettres[i], width=5)
        if mode=='aveugle':
            bouton.bind("<Button-1>", if_in_mot_aveugle)
            nombre_lettre_trouvees = 0
        else:
            bouton.bind("<Button-1>", if_in_mot)
        bouton.grid(row=i // 13, column=i % 13, padx=1, pady=1)
    canvas_alphabet.pack(side="bottom")

def cacher_mot():
    """Permet de cacher et d'afficher le mot caché qu'on souhaite faire deviner."""
    global mot_cache, mot_cache_label, mode
    mot_cache = ["_" for c in range(len(mot_choisi))]
    if mode=="aveugle":
        mot_cache_label=tk.Label(frame, text="Il y a "+str(len(mot_choisi))+" lettres dans le mot.", font=("Calibri", 20), pady=5)
    else:
        mot_cache_label=tk.Label(frame, text=len(mot_choisi)*"_ ", font=("Calibri", 36))
    mot_cache_label.pack(side="top")
    # print(mot_choisi)

def rejouer(victoire):
    """Propose de refaire une partie de pendu.
    Fonction bricolé à revoir rapidement !"""
    global canvas_rejouer, label_rejouer, label_score, mode
    canvas_rejouer = tk.Canvas(frame, width=200, height=70)
    canvas_rejouer.pack(side="bottom")
    if mode == "normal":
        if victoire==True:
            scores['normal'] += 1
            if int(scores['normal']) > int(best_scores['normal']):
                best_scores['normal'] = scores['normal']
                ecrire_best_score(False)
            label_score = tk.Label(frame, text=f"Votre score est de : {scores['normal']}. Le meilleur score est de : {best_scores['normal']}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Continuer la série ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
        else:
            label_score = tk.Label(frame, text=f"Votre score était de : {scores['normal']}. Le meilleur score est de : {best_scores['normal']}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Voulez vous rejouer ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
            scores['normal'] = 0
        button_rejouer_oui=tk.Button(canvas_rejouer, text="Oui", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(True, 'normal')])
        button_rejouer_oui.grid(row=0, column=1)
        button_rejouer_non=tk.Button(canvas_rejouer, text="Revenir au menu principal", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), texte_principal('black', False), button(True)])
        button_rejouer_non.grid(row=0, column=3)
    if mode == "diff":
        if victoire==True:
            gscores['difficile'] += 1
            if int(scores['difficile']) > int(best_scores['difficile']):
                best_scores['difficile'] = scores['difficile']
                ecrire_best_score(False)
            label_score = tk.Label(frame, text=f"Votre score est de : {scores['difficile']}. Le meilleur score est de : {best_scores['difficile']}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Continuer la série ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
        else:
            label_score = tk.Label(frame, text=f"Votre score était de : {scores['difficile']}. Le meilleur score est de : {best_scores['difficile']}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Voulez vous rejouer ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
            scores['difficile'] = 0
        button_rejouer_oui=tk.Button(canvas_rejouer, text="Oui", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(True, 'diff')])
        button_rejouer_oui.grid(row=0, column=1)
        button_rejouer_non=tk.Button(canvas_rejouer, text="Revenir au menu principal", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), texte_principal('black', False), button(True)])
        button_rejouer_non.grid(row=0, column=2)
    if mode == "aveugle":
        if victoire==True:
            scores['aveugle'] += 1
            if int(scores['aveugle']) > int(best_scores['aveugle']):
                best_scores['aveugle'] = scores['aveugle']
                ecrire_best_score(False)
            label_score = tk.Label(frame, text=f"Votre score est de : {scores['aveugle']}. Le meilleur score est de : {best_scores['aveugle']}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Continuer la série ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
        else:
            label_score = tk.Label(frame, text=f"Votre score était de : {scores['aveugle']}. Le meilleur score est de : {best_scores['aveugle']}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Voulez vous rejouer ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
            scores['aveugle'] = 0
        label_score.configure(bg='#ffffff')
        label_rejouer.configure(bg='#ffffff')
        button_rejouer_oui=tk.Button(canvas_rejouer, text="Oui", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(True, 'aveugle')])
        button_rejouer_oui.grid(row=0, column=1)
        button_rejouer_non=tk.Button(canvas_rejouer, text="Revenir au menu principal", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), texte_principal('black', False), button(True)])
        button_rejouer_non.grid(row=0, column=2)
    if mode == "grec":
        if victoire==True:
            scores['grec'] += 1
            if int(scores['grec']) > int(best_scores['grec']):
                best_scores['grec'] = scores['grec']
                ecrire_best_score(False)
            label_score = tk.Label(frame, text=f"Votre score est de : {scores['grec']}. Le meilleur score est de : {best_scores['grec']}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Continuer la série ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
        else:
            label_score = tk.Label(frame, text=f"Votre score était de : {scores['grec']}. Le meilleur score est de : {best_scores['grec']}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Voulez vous rejouer ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
            scores['grec'] = 0
        button_rejouer_oui=tk.Button(canvas_rejouer, text="Oui", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(True, 'grec')])
        button_rejouer_oui.grid(row=0, column=1)
        button_rejouer_non=tk.Button(canvas_rejouer, text="Revenir au menu principal", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), texte_principal('black', False), button(True)])
        button_rejouer_non.grid(row=0, column=2)

def fin_perdu():
    """Propose une fin où le joueur n'a pas réussit à trouver le mot caché."""
    global mot_cache_label
    canvas_alphabet.destroy()
    canvas_dessin.delete("all")
    nb_image = randint(1,9)
    img=tk.PhotoImage(file=f"pleur{DIRECTORY_SEP}pleur"+str(nb_image)+".png")
    (l,h)=(img.width(),img.height())
    canvas_dessin.config(width=l, height=h)
    canvas_dessin.create_image(l/2, h/2, image=img)
    canvas_dessin.pack(side="top")
    canvas_dessin.image=img
    mot_cache_label.config(text="Perdu, le mot à trouver était " + mot_choisi + " !", font=('Calibri',30))
    stop_music()
    if randint(1,2) == 1:
        play_music(f"music{DIRECTORY_SEP}defaite.mp3", False)
    else:
        play_music(f"music{DIRECTORY_SEP}nope_court.mp3", False)
    rejouer(False)

def fin_victoire():
    """Propose une fin où le joueur a réussit à trouver le mot caché."""
    global mot_cache_label
    canvas_alphabet.destroy()
    mot_cache_label.config(text="Bravo, le mot à trouver était bien " + mot_choisi + " !", font=('Calibri',28))
    nb_image=randint(1,7)
    canvas_dessin.delete("all")
    img=tk.PhotoImage(file=f"vic{DIRECTORY_SEP}vic"+str(nb_image)+".png")
    (l,h)=(img.width(),img.height())
    canvas_dessin.config(width=l, height=h)
    canvas_dessin.create_image(l/2, h/2, image=img)
    canvas_dessin.pack(side="top")
    canvas_dessin.image=img
    stop_music()
    if randint(1,2)==1:
        play_music(f"music{DIRECTORY_SEP}victoire.mp3", False)
    else:
        play_music(f"music{DIRECTORY_SEP}ole.mp3", False)
    rejouer(True)

def initialisation(replay, mode_jeu):
    """Initialise la partie avec différentes variables, supprime certains éléments si on rejoue et organise toute la partie selon le mode de jeu fournie en paramètre."""
    global mode, nb_erreurs, lettres_utilisees, button_main_menu
    mode = mode_jeu
    if replay==True:
        label_score.destroy()
        canvas_rejouer.destroy()
        label_rejouer.destroy()
        mot_cache_label.destroy()
        canvas_dessin.destroy()
    else:
        canvas_bouton.destroy()
    nb_erreurs = 1
    lettres_utilisees=[]
    if mode=='diff':
        texte_principal('red', False)
        pendu0()
        choix_mot(f"dico{DIRECTORY_SEP}dico_diff.txt")
        cacher_mot()
        play_music(f"music{DIRECTORY_SEP}jeu_diff.mp3", True)
    if mode=='grec':
        texte_principal('grec', False) 
        pendu0() 
        choix_mot(f"dico{DIRECTORY_SEP}dico_grec.txt")
        cacher_mot()
        play_music(f"music{DIRECTORY_SEP}jeu_grec.mp3", True)
    if mode=='aveugle':
        texte_principal('black', False)
        pendu0()
        choix_mot(f"dico{DIRECTORY_SEP}dico.txt")
        cacher_mot()
        fond_color("#ffffff")
    if mode=='normal':
        texte_principal('black', False)
        pendu0()
        choix_mot(f"dico{DIRECTORY_SEP}dico.txt")
        cacher_mot()
        play_music(f"music{DIRECTORY_SEP}jeu.mp3", True)
    creation_bouton()
    
def if_in_mot(event):
    """Fonction permettant de trouver la lettre proposer par l'utilisateur, et de l'afficher dans le mot caché tout en changeant le pendu si la lettre n'apparaît pas dans le mot caché.
    Cette fonction bloque les lettrees déjà utilisées et lance les fonctions de victoire et de défaite."""
    global nb_erreurs, lettres_utilisees
    bouton_lettre=event.widget
    lettre=bouton_lettre["text"]
    if lettre in lettres_utilisees:
        messagebox.showwarning("Lettre utilisée", "Cette lettre a déjà été utilisée !")
    else:
        lettres_utilisees.append(lettre)
        if lettre in mot_choisi:
            for i in range(len(mot_choisi)):
                if lettre==mot_choisi[i]:
                    mot_cache[i]=lettre
                    mot_cache_label.config(text=mot_cache)
                    bouton_lettre.config(bg='darkgreen')
            if "_" not in mot_cache:
                fin_victoire()
        else:
            bouton_lettre.config(state='disabled', bg='darkred')
            canvas_dessin.delete("all")
            img=tk.PhotoImage(file=f"pendu_img{DIRECTORY_SEP}pendu"+str(nb_erreurs)+".png")
            (l,h)=(img.width(),img.height())
            canvas_dessin.create_image(l/2, h/2, image=img)
            canvas_dessin.pack(side="top")
            canvas_dessin.image=img
            nb_erreurs = nb_erreurs + 1
            if nb_erreurs>=8:
                fin_perdu()

def if_in_mot_aveugle(event):
    """Fonction permettant de trouver la lettre proposer par l'utilisateur, en changeant le pendu si la lettre n'apparaît pas dans le mot caché.
    Cette fonction bloque les lettrees déjà utilisées et lance les fonctions de victoire et de défaite."""
    global nb_erreurs, lettres_utilisees, nombre_lettre_trouvees, mot_cache
    bouton_lettre=event.widget
    lettre=bouton_lettre["text"]
    if lettre in lettres_utilisees:
        messagebox.showwarning("Lettre utilisée", "Cette lettre a déjà été utilisée !")
    else:
        lettres_utilisees.append(lettre)
        if lettre in mot_choisi:
            for i in range(len(mot_choisi)):
                if lettre==mot_choisi[i]:
                    mot_cache[i]=lettre
                    nombre_lettre_trouvees=nombre_lettre_trouvees+1
                    bouton_lettre.config(bg='darkgreen')
            if nombre_lettre_trouvees==len(mot_choisi):
                fin_victoire()
            else:
                for c in mot_cache:
                    if c =="_":
                        play_music(f"music{DIRECTORY_SEP}mauvaise_reponse.mp3", False)
                        sleep(1.5)
                    else:
                        play_music(f"music{DIRECTORY_SEP}bonne_reponse.mp3", False)
                        sleep(1.5)
        else:
            bouton_lettre.config(state='disabled', bg='darkred')
            canvas_dessin.delete("all")
            img=tk.PhotoImage(file=f"pendu_img{DIRECTORY_SEP}pendu"+str(nb_erreurs)+".png")
            (l,h)=(img.width(),img.height())
            canvas_dessin.create_image(l/2, h/2, image=img)
            canvas_dessin.pack(side="top")
            canvas_dessin.image=img
            nb_erreurs = nb_erreurs + 1
            if nb_erreurs>=8:
                fin_perdu()
            else:
                play_music(f"music{DIRECTORY_SEP}mauvaise_reponse.mp3", False)

# Propose les dernières configurations de la fenêtre et lance la fenêtre
fenetre.protocol('WM_DELETE_WINDOW', on_close)
fenetre.config(menu=menu_bar)
frame.pack(expand='YES')
# fenetre.wm_resizable(0, 0)
fenetre.mainloop()
