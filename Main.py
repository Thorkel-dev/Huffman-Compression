import os as os  # Manipulation des fichiers/dossiers
import winsound as sound  # Gestion des sons sous Window
import tkinter.messagebox as tkmessage  # Messages d'alertes
import tkinter.filedialog as tkfile  # Récuperation des Chemins des fichiers
import json as json  # Manipulation de dictionnaire dans des fichiers
import math  # Utilisation du logarithme
import time as temps  # Capture de l'horloge de l'ordinateur
from operator import itemgetter  # Permet de manipuler des objets pythons
import tkinter as tk
information = "Compression de Huffman\
                \nRéalisé par Edouard GAUTIER et Antoine LAURENT\
                \nPromotion Meitner, P2A\
                \nProjet Maths-Info, année 2019"

# Import des bibliothéques natives


class Temps():
    """
    Calcule le temps d'éxecution du programme
    """

    def __init__(self):
        self.debut = float()
        self.fin = float()
        self.chrono = float()

    def start(self):
        """
        Capture de l'heure de l'odinateur quand on lance le programme
        """
        self.debut = temps.time()

    def stop(self):
        """
        Capture de l'heure de l'odinateur au moment ou le programme est fini
        """
        self.fin = temps.time()
        self.chrono = self.fin - self.debut  # On fait la différence


class Compression():
    """
    Compression de fichier par la méthode de Huffman
    """

    def __init__(self, fichier):
        self.fichier = fichier
        self.dico_frequences = dict()
        self.entropie = float()
        self.longueur = float()
        self.nb_octet = int()
        self.nb_octet_diff = int()
        self.liste_noeud = list()
        self.liste_feuille = list()
        self.fichier_compression = str(os.path.splitext(
            fichier)[0]) + str(".hf")  # Chemin du fichier compréssé
        self.dico_code = dict()
        self.fichier_taille = os.path.getsize(self.fichier)
        return None

    def compression(self):
        """
        Compression du fichier sélectionner
        """
        nom_fichier = os.path.splitext(os.path.basename(self.fichier))[0]
        fichier_sortie = tkfile.asksaveasfilename(
            title="Choix de la destination",
            filetypes=[('txt files', '.hf')],
            defaultextension="hf",
            initialdir=self.fichier,
            initialfile=nom_fichier)  # On choisi où enregistrer le fichier
        temps_1 = Temps()  # On lance le chronomètre
        temps_1.start()
        # On effectue les différentes étapes
        self.lecture_fichier(self.fichier)
        self.arbre(self.liste_feuille)
        self.racine.codage()
        temps_1.stop()  # Fin de la création de l'arbre et arrêt du chronomêtre
        self.chrono_1 = temps_1.chrono
        temps_2 = Temps()
        temps_2.start()
        self.ecrire_entete(self.fichier, fichier_sortie,
                           self.dico_code)
        self.encodage(self.fichier, fichier_sortie, self.dico_code)
        self.fichier_compression_taille = os.path.getsize(
            self.fichier_compression)
        temps_2.stop()
        self.chrono_2 = temps_2.chrono
        self.gain = (self.nb_octet - self.fichier_compression_taille) / \
            self.nb_octet * 100
        self.definir_entropie(self.dico_frequences)
        self.definir_longueur_symboles(self.dico_code)
        self.donne = f"\nCompression du fichier: \
            {os.path.basename(self.fichier)}\
                        \nFichier de taille:{self.fichier_taille:53} octets\
                        \n\n1-Construction de l'arbre\
                        \nNombre d'octet différent:\
                        {self.nb_octet_diff:17} octets\
                        \nTemps d'éxcution:{self.chrono_1:39} s\
                        \n\n2-Ecriture du fichier .hf\
                        \nFichier de taille:\
                        {self.fichier_compression_taille:30} octets\
                        \nGain:{self.gain:68.2f} %\
                        \nEntropie:{self.entropie:65.2f}\
                        \nTaille moyenne d'un symbole:{self.longueur:28.2f}\
                        \nTemps d'éxcution:{self.chrono_2:39} s"

    def lecture_fichier(self, fichier):
        """
        Lecture complète du fichier et comptage des fréquences
        """
        liste_octet = list()
        with open(fichier, "rb") as f:
            for ligne in f:
                for octet in ligne:
                    self.nb_octet += 1  # On compte le nombre de caractère
                    if octet in liste_octet:  # Si son dictionnaire existe
                        # On incrémente ses apparitions
                        self.dico_frequences[octet] += 1
                    else:  # Sinon on créé son dictionnaire
                        liste_octet.append(octet)
                        self.dico_frequences[octet] = 1
            # On transforme les dictionnaires en tuples, que l'on trie dans
            # dans l'ordre croissant
            liste_donnees = sorted(
                self.dico_frequences.items(), key=lambda k: k[1])
            for objet in liste_donnees:
                # Chaque caractère est transformer en "feuille", qu'il faut placer
                self.liste_feuille.append(
                    Noeud(None, None, objet[1], objet[0]))
        f.close()
        self.nb_octet_diff = len(liste_octet)

    def definir_entropie(self, dictionnaire):
        """
        Met à jour l'entropie du fichier
        """
        self.entropie = 0
        for key, value in dictionnaire.items():
            proba = int(value)/int(self.nb_octet)
            self.entropie -= proba * math.log(proba, 2)
            # Formule de l'entropie : H(X) = Somme des -Pi*log2(Pi)

    def definir_longueur_symboles(self, dictionnaire):
        """
        Donne la longueur moyenne d'un symbole

        Args:
            dictionnaire (dict): dictionnaire avec les symboles
        """
        self.longueur = 0
        for key, value in dictionnaire.items():
            self.longueur += len(str(value)) \
                * (self.dico_frequences[key]/self.nb_octet)

    def arbre(self, liste):
        """
        Construction de l'arbre de Huffman avec tout ses noeuds

        Args:
            liste (list): liste des feuilles à traiter
        """
        if len(liste) > 1:  # Jusqu'a navoir plus qu'un seul noeud
            noeud = Noeud(liste[0], liste[1], liste[0].frequence +
                          liste[1].frequence)  # Nouveau noeud parent créé
            # avec les fils
            del liste[0: 2]  # On supprime les fils
            liste.append(noeud)  # Mais on ajoute le noeud parent
            self.liste_noeud.append(noeud)
            # On refait le trie
            liste = sorted(liste, key=lambda k: k.frequence)
            return self.arbre(liste)  # On recommence avec cette nouvel liste
        self.racine = self.liste_noeud[-1]  # c'est la racine de l'arbre
        # On libère de la mémoire, variable plus utile pour la suite
        del self.liste_feuille
        del self.liste_noeud
        return None

    def encodage(self, fichier, fichier_sortie, dico):
        """
        On créer le nouveau fichier .hf à parti de l'arbre

        Args:
            fichier (path): fichier à encoder
            fichier_sortie (path): fichier de sorti
            dico (dict): Ensemble des symboles avec leur encodage
        """
        tampon = str()
        lecture = True
        # On lit le fichier à l'entrée et on écrit le fichier de sortie
        with open(fichier, "rb") as fichier_entree:
            with open(fichier_sortie, 'ab') \
                    as fichier_s:  # On créer le fichier avec une extention .hf
                while lecture == True:  # Tant qu'il reste des octets à lire
                    octet = fichier_entree.read(1)
                    if octet == b"":  # On est arrivé au dernier octet
                        lecture = False
                    else:
                        # On transforme l'octet en bits tout retirant le b''
                        mot = bin(ord(octet))[2:]
                        # On créer une mémoire tampon pour écrire des octets
                        tampon += (dico[int(mot, 2)])
                        while len(tampon) >= 8:
                            fichier_s.write(bytes([int(tampon[:8], 2)]))
                            tampon = tampon[8:]  # On garde les bits en trop
                if tampon != "":
                    # S'il reste des bits dans le tampon à la fin de la lecture
                    while len(tampon) != 8:
                        tampon = tampon + str(0)
                    fichier_s.write(bytes([int(tampon[:8], 2)]))
        fichier_s.close()
        fichier_entree.close()

    def ecrire_entete(self, fichier, fichier_sortie, dictionnaire):
        """
        Ecrit l'entete dans le fichier fichier_sortie.
        Format de l'entete sous forme d'octets :
            sur 12 octets : nombre de bytes encodes,
            sur 4 octets : l'extension,
            sur 8 octets : taille du dictionnaire,
            sur un nombre variable d'octets : dictionnaire

        Args:
            fichier (path): fichier à encoder
            fichier_sortie (path): fichier de sorti
            dictionnaire (dicy): Dictionnaire avec l'entête
        """
        nb_octets = os.path.getsize(fichier)
        extension = os.path.splitext(fichier)[1][1:]
        taille_dictionnaire = len(json.dumps(dictionnaire))
        with open(fichier_sortie, 'wb') as sortie:
            self.combler_octets(str(nb_octets), sortie, 12)
            self.combler_octets(extension, sortie, 4)
            self.combler_octets(str(taille_dictionnaire), sortie, 8)
            self.combler_octets(json.dumps(dictionnaire), sortie, 0)
        sortie.close()

    def combler_octets(self, mot, fichier, nombre):
        """
        Permet de rajouter des bits de zéros pour avoir des octes complets

        Args:
            mot (str): symbole à écrire
            fichier (path): fichier à écrire
            nombre (int): nombre de bits manquant

        Returns:
            [type]: [description]
        """
        while len(mot) < nombre:
            mot = str(0) + mot
        fichier.write(bytes(mot, encoding="utf8"))
        return None


class Noeud():
    """
    Tout les noeuds de l'abre de Huffman
    """

    def __init__(self, gauche=None, droite=None, frequence=int(),
                 symbole=None):
        """
        Tout les noeuds de l'abre de Huffman

        Args:
            gauche (Noeud, optional): Noeud de gauche. Defaults to None.
            droite (Noeud, optional): Noeud de droite. Defaults to None.
            frequence (int, optional): fréquence du Noeud. Defaults to int().
            symbole (str, optional): symbole du Noeud. Defaults to None.
        """
        self.gauche = gauche
        self.droite = droite
        self.frequence = frequence
        self.symbole = symbole
        self.code = ""

    def codage(self, code=str()):
        """
        On donne un code à toute les feuilles de l'arbre

        Args:
            code (str, optional): code obtenu avec les présedent Noeud. Defaults to str().
        """
        if self.gauche is not None and self.gauche.symbole is None:
            # Branche de gauche:
            self.code = code + str(1)  # On code le côté gauche par "1"
            # On descend d'un cran dans la branche
            self.gauche.codage(self.code)
        # On arrive sur une feuille
        else:  # Feuille de gauche
            self.code = code + str(1)
            # Dictionnaire créé durant la lecture du fichier
            huffman_c.dico_code[self.gauche.symbole] = self.code
            # print(f"octet:{self.gauche.symbole:10} code:{self.code:15} \
            #    fréquence:{self.gauche.frequence}")
        # Branche de droite
        if self.droite is not None and self.droite.symbole is None:
            self.code = code + str(0)
            self.droite.codage(self.code)
        else:  # Feuille de droite
            self.code = code + str(0)
            huffman_c.dico_code[self.droite.symbole] = self.code
            # print(f"octet:{self.droite.symbole:10} code:{self.code:15} \
            #    fréquence:{self.droite.frequence}")


class Decompression():
    """
    Décompression d'un fichier .hf
    """

    def __init__(self, fichier):
        self.fichier = fichier
        return None

    def decompression(self):
        """
        Décompression du fichier
        """
        tampon = str()
        compteur = int()
        lecture = True
        temps = Temps()  # On lance le chronomètre
        temps.start()
        with open(self.fichier, "rb") as fichier_e:
            # On récupére les informations dans l'entête du fichier d'origine
            # On lit le fichier dan son ensemble
            nb_octets = int(fichier_e.read(12))
            extension = fichier_e.read(4).decode("utf8").replace("0", "")
            taille_dictionnaire = int(fichier_e.read(8))
            dictionnaire = json.loads(fichier_e.read(
                taille_dictionnaire).decode("utf8"))
            dictionnaire = dict([(v, k) for k, v in dictionnaire.items()])
            chemin = os.path.splitext(self.fichier)[0]
            nom_fichier = os.path.splitext(os.path.basename(self.fichier))[0]
            fichier_sortie = tkfile.asksaveasfilename(
                title="Choix de la destination",
                filetypes=[('All files', '.*')],
                defaultextension=extension,
                initialdir=chemin,
                initialfile=nom_fichier)  # On choisi où enregistrer le fichier
            with open(fichier_sortie, "wb") as fichier_s:
                # On crée et écrie le fichier décompréssé
                while compteur < nb_octets:
                    # Tant qu'il n'a pas autant d'octet cas l'origine
                    if lecture == True:  # Tant qu'il reste des octets à lire
                        octet = fichier_e.read(1)
                        if octet == b"":  # On est arrivé au dernier octet
                            lecture = False
                        else:
                            # On transforme l'octet en bits tout retirant le b''
                            mot = bin(ord(octet))[2:]
                            while len(mot) < 8:
                                # On rajoute les 0 disparuent
                                mot = str(0) + mot
                    tampon += mot
                    i = 0
                    while i <= len(tampon) and compteur < nb_octets:
                        # On teste tout les ensembles de bits possible
                        i += 1
                        if tampon[:i] in dictionnaire:
                            # Si le code correspond à un octet
                            fichier_s.write(bytes([
                                int(dictionnaire[tampon[:i]])]))
                            tampon = tampon[i:]  # On efface les bits utilisés
                            compteur += 1  # On compte l'octet créé
                            i = 0  # On reprend on début de la mémoire tampon
        fichier_e.close()
        fichier_s.close()
        temps.stop()
        self.chrono = temps.chrono
        self.donne = f"\nDécompression du fichier:\
            {os.path.basename(self.fichier)}\
                        \n\nNom du fichier: \
                        {os.path.basename(fichier_sortie)}\
                        \nDictionnaire de taille:\
                        {taille_dictionnaire:24} octets\
                        \nFichier de taille:\
                        {os.path.getsize(fichier_sortie):30} octets\
                        \nTemps d'éxcution:{self.chrono:39} s"


class Fenetre():
    """
    Création de l'interface
    """

    def initialisation(self):
        """
        On créé la fênetre
        """
        win = tk.Tk()
        win.title("Huffman")
        can = tk.Canvas(height=189, width=389)
        can.pack(side=tk.TOP)
        frm_1 = tk.Frame(win)
        frm_1.pack(side=tk.TOP)
        image = tk.PhotoImage(file='Programme\images\Logo.png')
        can.create_image(195, 95, image=image)
        lab_1 = tk.Label(frm_1, text=information, justify="left")
        lab_1.pack()
        tk.Button(frm_1, text='Compression',
                  command=self.compression).pack(padx=10, pady=10, side=tk.RIGHT)
        tk.Button(frm_1, text='Décompression',
                  command=self.decompression).pack(padx=10,
                                                   pady=10, side=tk.LEFT)
        frm_2 = tk.Frame(win)
        frm_2.pack(side=tk.BOTTOM, pady=10)
        self.lab_2 = tk.Label(frm_2, text=f'{""}', justify="left")
        self.lab_2.pack()
        win.mainloop()

    def compression(self):
        """
        Demande de compression d'un fichier
        """
        global huffman_c
        fichier = tkfile.askopenfilename(
            title="Choisir un fichier à comprésser",
            filetypes=[('all files', '.*')])  # On ouvre un boite de dialogue et
        # on récupére le chemin absolu du fichier
        try:
            if os.path.splitext(fichier)[1][1:] != "hf":
                huffman_c = Compression(fichier)
                huffman_c.compression()
                sound.PlaySound("SystemHand", sound.SND_ASYNC |
                                sound.SND_ALIAS)  # On avertie de la fin de l'opération
                self.lab_2['text'] = f'{huffman_c.donne}'
                # On affiche les stats
            else:  # Si on essaye avec un fichier déja compréssé
                tkmessage.showerror(title="Erreur",
                                    message="Types de fichier incorrecte.\
                    \nSélectioner un fichier autre que .hf")
        except PermissionError:  # Si on utilise déjà le fichier
            tkmessage.showerror("Erreur",
                                "Le fichier est déja ouvert dans une application.",)
        except FileNotFoundError:  # Si le fichier n'existe pas
            pass

    def decompression(self):
        """
        Demande de décompression d'un fichier
        """
        global huffman_d
        fichier = tkfile.askopenfilename(
            title="Choisir un fichier à décomprésser",
            filetypes=[('txt files', '.hf')])
        try:
            if fichier != '' and os.path.splitext(fichier)[1][1:] != "hf":
                tkmessage.showerror(title="Erreur",
                                    message="Types de fichier incorrecte.\
                    \nSélectioner un fichier .hf")
            else:
                huffman_d = Decompression(fichier)
                huffman_d.decompression()
                sound.PlaySound("SystemHand", sound.SND_ASYNC |
                                sound.SND_ALIAS)
                sound.MB_ICONASTERISK
                self.lab_2['text'] = f'{huffman_d.donne}'
        except PermissionError:
            tkmessage.showerror("Erreur",
                                "Le fichier est déja ouvert dans une application.",)
        except FileNotFoundError:
            pass
        return None


if __name__ == "__main__":
    fenetre = Fenetre()
    fenetre.initialisation()
