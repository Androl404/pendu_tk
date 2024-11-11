# Importation des modules nécessaires au fonctionnement du programme
from random import randint
from time import sleep
import tkinter as tk
from tkinter import messagebox
from tkhtmlview import HTMLLabel
import webbrowser
import urllib.request
import os

# Importation du mixeur de "Pygame" et suppression de son message de bienvenue dans la console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

# Initialisation du mixeur de pygame
mixer.init()

# Création de la fenêtre
fenetre=tk.Tk()
fenetre.title("Le jeu du pendu")
# fenetre.iconbitmap("@./icone.xbm")
fenetre.iconbitmap("icone.ico")
fenetre.minsize(900, 600)
fenetre.geometry("900x600")
frame = tk.Frame(fenetre)

pendu_version = '1.4.2'

class Score():
    def __init__(self, mode, fichier):
        self.score = 0
        self.best_score = 0
        self.mode = mode
        self.fichier = fichier
    
    def verifier_fichiers(self):
        global dir
        dir = os.getenv('APPDATA')+"\\Jeu du pendu\\score\\"
        if os.path.exists(dir)==False:
            os.makedirs(dir)
        if os.path.exists(dir+self.fichier)==False:
            contenu_fichier = open(dir+self.fichier, "w", encoding="utf-8")
            contenu_fichier.write("0")
            contenu_fichier.close()
    
    def recup_best_score(self):
        contenu_fichier = open(dir+self.fichier, "r", encoding="utf-8")
        self.best_score = contenu_fichier.read()
        contenu_fichier.close()
    
    def ecrire_best_score(self, reset):
        contenu_fichier = open(dir+self.fichier, "w", encoding="utf-8")
        if reset:
            contenu_fichier.write("0")
            self.best_score = 0
            contenu_fichier.close()
            messagebox.showinfo(f'Meilleur score {self.mode}', f'Le meilleur score {self.mode} a été réinitialisé et est maintenant de : {self.best_score}.')
        else:
            contenu_fichier.write(str(self.best_score))
            contenu_fichier.close()
            self.best_score = self.score
    
    def afficher_best_score(self):
        messagebox.showinfo(f'Meilleur score {self.mode}', f'Le meilleur score {self.mode} est de : {self.best_score}.')

# Création des scores pour les différents modes
score_normal = Score("normal", "score.txt")
score_normal.verifier_fichiers()
score_normal.recup_best_score()

score_diff = Score("difficile", "score_diff.txt")
score_diff.verifier_fichiers()
score_diff.recup_best_score()

score_aveugle = Score("aveugle", "score_aveugle.txt")
score_aveugle.verifier_fichiers()
score_aveugle.recup_best_score()

score_grec = Score("grec", "score_grec.txt")
score_grec.verifier_fichiers()
score_grec.recup_best_score()

class Window(tk.Toplevel):
    """Permet de créer une sous-fenêtre pour l'aide ou les notes de mises à jour par exemple"""
    def __init__(self, parent):
        super().__init__(parent)
    
    def titre_icone(self, titre):
        self.title(titre)
        self.iconbitmap("icone.ico")
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
    texte_update = """<ul><li><b>Version 1.4.2</b><ol><li>Les mots déjà apparus dans une partie ne devrait plus ré-apparaître sauf si vous enchaînez 190 parties de pendu en utilisant la même fenêtre</li><li>Mise à jour du dictionnaire grec qui contient désormais 192 mots</li><li>Ajout d'un raccourci pour fermer les sous-fenêtres</li><li>Correction d'un bug en mode Grec qui affichait deux fois la dernière lettre</li><li>Optimisation du code du jeu du pendu</li><li>Mise à jour de la section &laquo; Contributeurs &raquo; et de la section &laquo; Aide &raquo; du jeu du pendu</li></ol></li>
        <li><b>Version 1.4.1</b><ol><li>Correction d'un bug qui empêchait de lancer une partie en mode Normal et diverses corrections</li></ol></li>
        <li><b>Version 1.4.0</b><ol><li>Séparation du mode normal et des autres modes dans le menu principal en les déplaçant dans une partie accessible à l'aide du bouton sur le menu principal</li></ol></li>
        <li><b>Version 1.3.6</b><ol><li>Mise à jour de la section &laquo; Aide &raquo; du jeu du pendu</li><li>Le jeu du pendu prend désormais en charge plusieurs versions de Windows (7, 8, 8.1, 10 et 11) !</li><li>Ajout d'une option pour vérifier les mises à jour du jeu du pendu</li><li>Ajout d'un bouton dans la barre de menu pour ouvrir le dépôt GitHub</li><li>Déplacement du bouton pour fermer les fenêtres &laquo; Aide &raquo;, &laquo; Notes de mises à jour &raquo; et &laquo; Contributeurs &raquo;.</li></ol></li>
        <li><b>Version 1.3.5</b><ol><li>Correction d'un bug sur la création des répertoires pour le stockage du score</li><li>Correction d'une erreur dans un des mots du mode Grec</li><li>Mise à jour des sections &laquo; Contributeurs&raquo;, &laquo; Aide &raquo; et &laquo; À propos &raquo;</li><li>Ajout de mots au mode Grec</li><li>Les mots déjà apparus dans une partie ne devrait plus ré-apparaître sauf si vous enchaînez 105 parties de pendu en utilisant la même fenêtre</li></ol></li>
        <li><b>Version 1.3.4</b><ol><li>Changement de l'emplacement du stockage du score, pour une meilleure compatibilité pour l'installation dans le dossier "Programs Files" de Windows</li></ol></li>
        <li><b>Version 1.3.3</b><ol><li>Optimisation du code</li><li>Ajout de la section &laquo; Contributeurs &raquo;</li><li>Correction d'un bug qui bloquait le lancement d'une partie en mode &laquo; Normal &raquo;</li><li>Correction d'un bug qui empêchait le meilleur score de monter à plus de 9</li></ol></li>
        <li><b>Version 1.3.2</b><ol><li>Optimisation du jeu et du code</li><li>Correction de bugs mineurs</li><li>Les mots déjà apparus dans une partie ne devrait plus ré-apparaître sauf si vous enchaînez 36 parties de pendu en utilisant la même fenêtre</li><li>Diminution de la taille du jeu du pendu (musiques désormais en .MP3)</li></ol></li>
        <li><b>Version 1.3.1</b><ol><li>Dans le mode de jeu &laquo; Grec &raquo;, certaines lettres grecques n'apparaissaient pas comme bouton. Ce but a été partiellement corrigé puisque la dernière lettre est en doublon mais cela ne devrait pas affecter la partie.</li></ol></li>
        <li><b>Version 1.3</b><ol><li>Ajout du mode de jeu &laquo; Grec &raquo;, de ses bruitages, de son aide, de son score et mise à jour de la barre de menus</li><li>Correction de l'affichage des boutons de l'écran de fin en mode &laquo; Aveugle &raquo;</li></ol></li>
        <li><b>Version 1.2</b><ol><li>Ajout du mode de jeu &laquo; Aveugle &raquo;, de ses bruitages, de sa couleur de fond, de son aide, de son score et mise à jour de la barre de menus</li><li>Ajout d'un raccourci clavier pour ouvrir l'aide</li><li>Ajout de boutons pour fermer l'aide et les notes de mises à jour</li></ol></li>
        <li><b>Version 1.1.2</b><ol><li>Ajout des sections &laquo; Aide &raquo; et &laquo; Notes de mises à jour &raquo;</li><li>Changement des musiques de victoire et de perte</li><li>Correction d'un bug d'espacement des éléments</li><li>Suppression du verbe &laquo; branler &raquo; ainsi que de toutes ses conjugaisons du dictionnaire de mot difficile.</li></ol></li>
        <li><b>Version 1.1.1</b><ol><li>Fenêtre de jeu plus grande et espacement de certains éléments du jeu</li><li>Changement de certaines polices (invisible sur certaines machines)</li><li>Le titre se met en gras en fonction des différents modes de jeu</li></ol></li>
        <li><b>Version 1.1</b><ol><li>Ajout du mode de jeu &laquo; Difficile &raquo; et implémentation de son score et meilleur score</li><li>Ré-organisation et ajout d'éléments dans la barre de menus</li><li>Ajout d'un raccourci clavier pour quitter le jeu</li><li>Ajout de la possibilité de retourner au menu principal après avoir terminé une partie</li><li>Ajout et changement des musiques</li><li>Changement de couleur du titre en fonction du mode de jeu</li></ol></li>
        <li><b>Version 1.0.2</b><ol><li>Ajout d'images pour la victoire et la perte</li><li>Ajout de différentes musiques</li></ol></li>
        <li><b>Version 1.0</b><ol><li>Publication de la première version stable du jeu du pendu avec une interface graphique</li></ol></li></ul>
        <p>Section fournie et mise à jour par Andrei Zeucianu</p>"""

    update = Window(fenetre)
    update.titre_icone("Notes de mises à jour")
    update.main_titre("Notes de mises à jour")
    update.contenu(texte_update)
    update.lancer()

def help():
    """Crée une sous-fenêtre à l'aide de la classe Window pour afficher l'aide du jeu du pendu"""
    texte_help = """<p>Voici l'aide du jeu du pendu. Vous trouverez ici les règles et le fonctionnement de cette application ainsi que des différents modes de jeu disponibles.</p>
    <p>Le jeu du pendu en lui-même est très simple : un mot est choisi au hasard et vous devez le retrouvez en vous servant de toutes les lettres de l'alphabet. Si vous choissisez une lettre qui se trouve une ou plusieurs fois dans le mot, alors elle(s) s'affiche(nt). Sinon, vous progressez dans votre pendu. Mais attention, si vous faites 7 erreurs, la partie s'arrête et vous avez perdu.</p>
    <p>Dans cette application, vous retrouverez plusieurs modes de jeu vous tous plus difficile les uns que les autres et vous poussant à donner votre maximum.</p>
    <p>Voici les règles des différents modes de jeu :</p>
    <ul><li><b>Mode normal :</b> Une partie de pendu, tout ce qu'il y a de plus normal. Un mot facile est choisi parmi 889 mots. Votre score représente le nombre de victoire(s) réalisée(s) d'affilée. Le meilleur score est mis à jour et sauvegardée chaque fois que le score devient plus grand que le meilleur score. Le meilleur score peut être réinitialisé depuis la barre de menus.</li>
    <li><b>Mode difficile :</b> Une partie de pendu, mais des mots beaucoup plus difficiles venants essentiellement du XVIIème siècle. Ce mot est choisi parmis 328 969 mots. Votre score représente le nombre de victoire(s) réalisée(s) d'affilée. Le meilleur score est mis à jour et sauvegardée chaque fois que le score devient plus grand que le meilleur score. Le meilleur score peut être réinitialisé depuis la barre de menus.</li>
    <li><b>Mode aveugle :</b> Une partie de pendu avec des mots faciles. Cependant, vous ne voyez pas les lettres au fur et à mesure dans votre mot. Vous devez vous fier au sons émis lorsque vous cliquez sur une lettre pour savoir si cette lettre se trouve dans le mot ou pas. Il s'agit du principe MOTUS. Les lettres présentent dans le mot que vous avez trouvé émettent un bruit positif lorsque vous cliquez sur une autre lettre toujours présente dans le mot. Si une lettre n'est pas dans le mot, alors un bruit négatif est émis. Votre score représente le nombre de victoire(s) réalisée(s) d'affilée. Le meilleur score est mis à jour et sauvegardée chaque fois que le score devient plus grand que le meilleur score. Le meilleur score peut être réinitialisé depuis la barre de menus.</li>
    <li><b>Mode Grec :</b> Une partie de pendu normale avec des mots grecs choisit parmis 107 mots. Votre score représente le nombre de victoire(s) réalisée(s) d'affilée. Le meilleur score est mis à jour et sauvegardée chaque fois que le score devient plus grand que le meilleur score. Le meilleur score peut être réinitialisé depuis la barre de menus.<br>Créé dans le cadre du cours de latin avec M. Jean-François Bothera.</li></ul>
    <p>Si vous rencontrez des bugs ou des soucis avec les différents fonctionnalités de cette application, n'hésitez pas à ouvrir un ticket sur le <a href='https://github.com/Androl404/pendu_tk'>dépôt GitHub</a> du jeu.</p>
    <p><strong>Astuce pour les pros :</strong> Si vous souhaitez fermer une sous-fenêtre comme celle-ci, vous pouvez appuyer sur <i>Espace</i>.</p>
    <br><br><br>Section d'aide fournie et mise à jour par Andrei Zeucianu"""

    help = Window(fenetre)
    help.titre_icone("Aide du jeu du pendu")
    help.main_titre("Aide du jeu du pendu")
    help.contenu(texte_help)
    help.lancer()

def contributeurs():
    """Crée une sous-fenêtre à l'aide de la classe Window pour afficher les contributeurs du jeu du pendu"""
    texte_contributeurs = """<p>Voici la liste des personnes ayant contribué à ce projet ainsi que l'aide concrète apportée :
    <ul><li><b>Anthony GAGO--KLIMENKO</b> : Aide mineure au développement et composition des musiques du mode &laquo; Normal &raquo;</li>
    <li><b>Corentin DOMENICHINI</b> : Bêta-testing du jeu pour différentes versions, mode &laquo; Aveugle &raquo; basé sur une de ses idées, fourniture de la liste de mots difficiles et revue générale du jeu</li></ul></p>
    <p>Section fournie et mise à jour par Andrei Zeucianu<br>N'hésitez pas à allez voir ma <a href="https://www.youtube.com/@tiroirdandrol">chaîne YouTube</a> !</p>"""

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
menu_normal.add_command(label="Voir le meilleur score", command=lambda:score_normal.afficher_best_score())
menu_normal.add_command(label="Réinitialiser le meilleur score", command=lambda:score_normal.ecrire_best_score(True))
file_menu.add_cascade(label="Mode normal", underline=0, menu=menu_normal)

menu_aveugle = tk.Menu(menu_bar, tearoff=0)
menu_aveugle.add_command(label="Voir le meilleur score aveugle", command=lambda:score_aveugle.afficher_best_score())
menu_aveugle.add_command(label="Réinitialiser le meilleur score auveugle", command=lambda:score_aveugle.ecrire_best_score(True))
file_menu.add_cascade(label="Mode aveugle", underline=0, menu=menu_aveugle)

menu_grec = tk.Menu(menu_bar, tearoff=0)
menu_grec.add_command(label="Voir le meilleur score grec", command=lambda:score_grec.afficher_best_score())
menu_grec.add_command(label="Réinitialiser le meilleur score grec", command=lambda:score_grec.ecrire_best_score(True))
file_menu.add_cascade(label="Mode grec", underline=0, menu=menu_grec)

menu_diff = tk.Menu(menu_bar, tearoff=0)
menu_diff.add_command(label="Voir le meilleur score difficile", command=lambda:score_diff.afficher_best_score())
menu_diff.add_command(label="Réinitialiser le meilleur score difficile", command=lambda:score_diff.ecrire_best_score(True))
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
    if loops==True:
        mixer.music.play(loops=-1)
    else:
        mixer.music.play()

def stop_music():
    """Arrête n'importe quel musique en train de jouer sur Pygame"""
    mixer.music.stop()

def about():
    """Définit le message à propos des auteurs."""
    lines = ['Jeu du pendu', 'Développé par Andrei Zeucianu','Merci aux contributeurs ❤' , 'Copyright 2023, Tous droits réservés', f'Version {pendu_version} (Stable)']
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
    play_music("music\\Menu.mp3", True)
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
    img = tk.PhotoImage(file="pendu_img\\pendu0.png")
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
            score_normal.score += 1
            if int(score_normal.score) > int(score_normal.best_score):
                score_normal.best_score = score_normal.score
                score_normal.ecrire_best_score(False)
            label_score = tk.Label(frame, text=f"Votre score est de : {score_normal.score}. Le meilleur score est de : {score_normal.best_score}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Continuer la série ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
        else:
            label_score = tk.Label(frame, text=f"Votre score était de : {score_normal.score}. Le meilleur score est de : {score_normal.best_score}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Voulez vous rejouer ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
            score_normal.score = 0
        button_rejouer_oui=tk.Button(canvas_rejouer, text="Oui", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(True, 'normal')])
        button_rejouer_oui.grid(row=0, column=1)
        button_rejouer_non=tk.Button(canvas_rejouer, text="Revenir au menu principal", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), texte_principal('black', False), button(True)])
        button_rejouer_non.grid(row=0, column=3)
    if mode == "diff":
        if victoire==True:
            score_diff.score += 1
            if int(score_diff.score) > int(score_diff.best_score):
                score_diff.best_score = score_diff.score
                score_diff.ecrire_best_score(False)
            label_score = tk.Label(frame, text=f"Votre score est de : {score_diff.score}. Le meilleur score est de : {score_diff.best_score}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Continuer la série ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
        else:
            label_score = tk.Label(frame, text=f"Votre score était de : {score_diff.score}. Le meilleur score est de : {score_diff.best_score}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Voulez vous rejouer ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
            score_diff.score = 0
        button_rejouer_oui=tk.Button(canvas_rejouer, text="Oui", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(True, 'diff')])
        button_rejouer_oui.grid(row=0, column=1)
        button_rejouer_non=tk.Button(canvas_rejouer, text="Revenir au menu principal", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), texte_principal('black', False), button(True)])
        button_rejouer_non.grid(row=0, column=2)
    if mode == "aveugle":
        if victoire==True:
            score_aveugle.score += 1
            if int(score_aveugle.score) > int(score_aveugle.best_score):
                score_aveugle.best_score = score_aveugle.score
                score_aveugle.ecrire_best_score(False)
            label_score = tk.Label(frame, text=f"Votre score est de : {score_aveugle.score}. Le meilleur score est de : {score_aveugle.best_score}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Continuer la série ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
        else:
            label_score = tk.Label(frame, text=f"Votre score était de : {score_aveugle.score}. Le meilleur score est de : {score_aveugle.best_score}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Voulez vous rejouer ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
            score_aveugle.score = 0
        label_score.configure(bg='#ffffff')
        label_rejouer.configure(bg='#ffffff')
        button_rejouer_oui=tk.Button(canvas_rejouer, text="Oui", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), initialisation(True, 'aveugle')])
        button_rejouer_oui.grid(row=0, column=1)
        button_rejouer_non=tk.Button(canvas_rejouer, text="Revenir au menu principal", font=("Calibri", 15), bg="lightblue", cursor="hand2", bd=1, command=lambda:[stop_music(), texte_principal('black', False), button(True)])
        button_rejouer_non.grid(row=0, column=2)
    if mode == "grec":
        if victoire==True:
            score_grec.score += 1
            if int(score_grec.score) > int(score_grec.best_score):
                score_grec.best_score = score_grec.score
                score_grec.ecrire_best_score(False)
            label_score = tk.Label(frame, text=f"Votre score est de : {score_grec.score}. Le meilleur score est de : {score_grec.best_score}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Continuer la série ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
        else:
            label_score = tk.Label(frame, text=f"Votre score était de : {score_grec.score}. Le meilleur score est de : {score_grec.best_score}.", font=("Comic Sans MS", 16))
            label_rejouer=tk.Label(frame, text="Voulez vous rejouer ?", font=("Garamond",18), pady=10)
            label_rejouer.pack(side="bottom")
            label_score.pack(side="bottom")
            score_grec.score = 0
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
    img=tk.PhotoImage(file="pleur\\pleur"+str(nb_image)+".png")
    (l,h)=(img.width(),img.height())
    canvas_dessin.config(width=l, height=h)
    canvas_dessin.create_image(l/2, h/2, image=img)
    canvas_dessin.pack(side="top")
    canvas_dessin.image=img
    mot_cache_label.config(text="Perdu, le mot à trouver était " + mot_choisi + " !", font=('Calibri',30))
    stop_music()
    if randint(1,2) == 1:
        play_music("music\\defaite.mp3", False)
    else:
        play_music("music\\nope_court.mp3", False)
    rejouer(False)

def fin_victoire():
    """Propose une fin où le joueur a réussit à trouver le mot caché."""
    global mot_cache_label
    canvas_alphabet.destroy()
    mot_cache_label.config(text="Bravo, le mot à trouver était bien " + mot_choisi + " !", font=('Calibri',28))
    nb_image=randint(1,7)
    canvas_dessin.delete("all")
    img=tk.PhotoImage(file="vic\\vic"+str(nb_image)+".png")
    (l,h)=(img.width(),img.height())
    canvas_dessin.config(width=l, height=h)
    canvas_dessin.create_image(l/2, h/2, image=img)
    canvas_dessin.pack(side="top")
    canvas_dessin.image=img
    stop_music()
    if randint(1,2)==1:
        play_music("music\\victoire.mp3", False)
    else:
        play_music("music\\ole.mp3", False)
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
        choix_mot("dico\\dico_diff.txt")
        cacher_mot()
        play_music("music\\jeu_diff.mp3", True)
    if mode=='grec':
        texte_principal('grec', False) 
        pendu0() 
        choix_mot("dico\\dico_grec.txt")
        cacher_mot()
        play_music("music\\jeu_grec.mp3", True)
    if mode=='aveugle':
        texte_principal('black', False)
        pendu0()
        choix_mot("dico\\dico.txt")
        cacher_mot()
        fond_color("#ffffff")
    if mode=='normal':
        texte_principal('black', False)
        pendu0()
        choix_mot("dico\\dico.txt")
        cacher_mot()
        play_music("music\\jeu.mp3", True)
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
            img=tk.PhotoImage(file="pendu_img\\pendu"+str(nb_erreurs)+".png")
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
                        play_music("music\\mauvaise_reponse.mp3", False)
                        sleep(1.5)
                    else:
                        play_music("music\\bonne_reponse.mp3", False)
                        sleep(1.5)
        else:
            bouton_lettre.config(state='disabled', bg='darkred')
            canvas_dessin.delete("all")
            img=tk.PhotoImage(file="pendu_img\\pendu"+str(nb_erreurs)+".png")
            (l,h)=(img.width(),img.height())
            canvas_dessin.create_image(l/2, h/2, image=img)
            canvas_dessin.pack(side="top")
            canvas_dessin.image=img
            nb_erreurs = nb_erreurs + 1
            if nb_erreurs>=8:
                fin_perdu()
            else:
                play_music("music\\mauvaise_reponse.mp3", False)

# Propose les dernières configurations de la fenêtre et lance la fenêtre
fenetre.protocol('WM_DELETE_WINDOW', on_close)
fenetre.config(menu=menu_bar)
frame.pack(expand='YES')
fenetre.wm_resizable(0, 0)
fenetre.mainloop()
