# survie si 2 ou 3 voisine
# sinon meure
# si case vide avec 3 voisine -> naissance

import tkinter as tk
from _thread import start_new_thread
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog
from time import sleep, time

def resource_path(relative_path):
    """
    Recupere le chemin absolu d'un fichier selon son nom (besoin pour le .exe)
    source : https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    """
    import os, sys
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def generer(case, x, y, contenu=[]):

    global liste_case, casse, nb_update

    # paramètres
    casse = case #pixel
    x_fenetre = x
    y_fenetre = y

    #init
    nb_update = 0
    liste_case = []

    # pour que sa tombe pille
    x_fenetre -= x_fenetre % casse
    y_fenetre -= y_fenetre % casse
    
    fenetre = tk.Tk()
    fenetre.attributes('-fullscreen', False)
    fenetre.iconbitmap(resource_path('icone.ico'))
    fenetre.geometry(f"{x_fenetre+50}x{y_fenetre}")
    fenetre.resizable(width=0, height=0)
    fenetre.title("jeu de la vie")

    class customb():
        def __init__(self,x,y,couleur="#ffffff"):
            self.x = x
            self.y = y
            self.couleur = couleur

            self.b = tk.Button(fenetre ,bg = self.couleur, activebackground="gray",command=lambda : liste_case[x][y].change_couleur())
            self.b.place(x=x*casse, y=y*casse, width=casse, height=casse)

        def change_couleur(self):
            self.couleur = "#000000" if self.couleur == "#ffffff" else "#ffffff"
            self.b.configure(bg=self.couleur)

        def update(self):
            def tryexcept(x, y):
                try:
                    # Ne devrait normalement pas marcher
                    return liste_case[(self.x+x)%x_fenetre][(self.y+y)%y_fenetre].couleur == "#000000"
                except:  
                    return False
            nb1 = tryexcept(1, -1)
            nb2 = tryexcept(0, -1)
            nb3 = tryexcept(-1, -1)
            nb4 = tryexcept(1, 0)
            nb6 = tryexcept(-1, 0)
            nb7 = tryexcept(1, 1)
            nb8 = tryexcept(0, 1)
            nb9 = tryexcept(-1, 1)
            total = nb1 + nb2 + nb3 + nb4 + nb6 + nb7 + nb8 + nb9
            if total == 3 and self.couleur == "#ffffff" : return self
            elif total != 2 and total != 3 and self.couleur == "#000000" : return self

        def reset(self):
            self.couleur = "#ffffff"
            self.b.configure(bg=self.couleur)

    global stop
    stop=False

    def update(event=None):
        global nb_update
        liste_changements = []
        for colonne in liste_case:
            for case in colonne:
                temp = case.update()
                if temp != None: liste_changements.append(temp)
        for case in liste_changements:
            case.change_couleur()
        nb_update += 1

    def ups():
        fps = tk.Label(text="  u/s : \n 0", font = (16,))
        fps.place(x=x_fenetre, y=10, width=40, height=30)
        global nb_update
        while True:
            fps.configure(text = f"  u/s : \n {nb_update}")
            nb_update = 0
            global stop
            if stop == True:
                break
            sleep(1)

    for x in range(x_fenetre//casse):
        col = []
        for y in range(y_fenetre//casse):
            col.append(customb(x,y))
        liste_case.append(col)

    if contenu != []:
        for colonne in liste_case:
            for case in colonne:
                if contenu[case.x][case.y] == True:
                    case.change_couleur()

    start_new_thread(ups,())

    def ouvrir(event=None):
        try:
            chemin = filedialog.askopenfilename()
            fichier = open(chemin, "r").readlines()
            fenetre.destroy()
            generer(int(fichier[0].split(",")[0]), int(fichier[0].split(",")[1]), int(fichier[0].split(",")[2]), eval(fichier[1]))
        except:
            pass

    def save(event=None):
        try:
            files = [('All Files', '*.*'),('Game of life', '*.gol'), ('Text Document', '*.txt')]
            fichier = asksaveasfile(filetypes = files, defaultextension = files)
            fichier.write(f"{casse},{x_fenetre},{y_fenetre}\n")
            liste = []
            for colonne in liste_case:
                col = []
                for case in colonne:
                    if case.couleur == "#000000": col.append(True)
                    if case.couleur == "#ffffff": col.append(False)
                liste.append(col)
            fichier.write(str(liste)+"\n")
        except:
            pass
        
    def reset(event=None):
        for colonne in liste_case:
            for case in colonne:
                if case.couleur == "#000000" :
                    case.change_couleur()

    def basic(event=None, case=20, x=500, y=500):
        fenetre.destroy()
        generer(case, x, y)
        
    def change(event=None):
        newWindow = tk.Toplevel(fenetre)
        newWindow.title("Parametres")
        newWindow.geometry("200x100")
        label1 = tk.Entry(newWindow)
        label2 = tk.Entry(newWindow)
        label3 = tk.Entry(newWindow)
        label1.insert(0, "taille de la case")
        label2.insert(0, "nb de cases en x")
        label3.insert(0, "nb de cases en y")
        label1.pack()
        label2.pack()
        label3.pack()
        def commande():
            temp = [int(label1.get()), int(label2.get())*int(label1.get()), int(label3.get())*int(label1.get())]
            newWindow.destroy()
            fenetre.destroy()
            global stop
            stop=True
            generer(temp[0], temp[1], temp[2])
        tk.Button(newWindow,text ="VALIDER", font=(12), command = commande).place(x=50, y=60, width=100, height=25)
        
    def aleatoire(event=None):
        reset()
        liste = []
        for _ in range(x_fenetre//casse):
            colonne = []
            for _ in range(y_fenetre//casse):
                import random
                colonne.append(bool(random.randint(0, 1)))
            liste.append(colonne)
        for x in range(x_fenetre//casse):
            for y in range(y_fenetre//casse):
                if liste[x][y] == True:
                    liste_case[x][y].change_couleur()
                    
    step = tk.Button(text="step", command=update, bg= "red", activebackground="red")
    step.place(x=x_fenetre, y=50, width=50, height=30)
    
    global stop2, stop3
    stop2, stop3 = True, True

    def repeater():
        while stop2 == False: update()

    def lent_repeater():
        while stop3 == False:
            debut = time()
            update()
            while time() - debut < 0.1: pass

    def loop_10(): # 1/0 pour on/off :)
        global stop2
        if stop3 == False: lent_loop_10()
        if stop2 == True:
            stop2 = False
            start_new_thread(repeater,())
            loopb.configure(bg= "#00ff00")
        else:
            stop2 = True
            loopb.configure(bg= "red")

    def lent_loop_10(): # 1/0 pour on/off :)
        global stop3
        if stop2 == False: loop_10()
        if stop3 == True:
            stop3 = False
            start_new_thread(lent_repeater,())
            lent_loopb.configure(bg= "#00ff00")
        else:
            stop3 = True
            lent_loopb.configure(bg= "red")
        

    loopb = tk.Button(text="loop inf", command=loop_10, bg= "red", activebackground="#ffff00")
    loopb.place(x=x_fenetre, y=80, width=50, height=30)
    lent_loopb = tk.Button(text="10 loop/s", command=lent_loop_10, bg= "red", activebackground="#ffff00")
    lent_loopb.place(x=x_fenetre, y=110, width=50, height=30)
    tk.Button(text="save", command=save, bg= "red", activebackground="red").place(x=x_fenetre, y=140, width=50, height=30)
    tk.Button(text="open", command=ouvrir, bg= "red", activebackground="red").place(x=x_fenetre, y=170, width=50, height=30)
    tk.Button(text="reset", command=reset, bg= "red", activebackground="red").place(x=x_fenetre, y=200, width=50, height=30)
    tk.Button(text="fullreset", command=basic, bg= "red", activebackground="red").place(x=x_fenetre, y=230, width=50, height=30)
    tk.Button(text="custom", command=change, bg= "red", activebackground="red").place(x=x_fenetre, y=260, width=50, height=30)
    tk.Button(text="quit", command=fenetre.destroy, bg= "red", activebackground="red").place(x=x_fenetre, y=290, width=50, height=30)
    tk.Button(text="random", command=aleatoire, bg= "red", activebackground="red").place(x=x_fenetre, y=320, width=50, height=30)

    fenetre.bind("<space>", update)
    fenetre.bind("<s>", save)      
    fenetre.bind("<o>", ouvrir)
    fenetre.bind("<r>", reset)
    fenetre.bind("<a>", aleatoire)
    fenetre.bind("<b>", basic)
    fenetre.bind("<c>", change)
    fenetre.bind("<e>", lambda : fenetre.destroy())
    fenetre.mainloop()

generer(20, 500, 500)