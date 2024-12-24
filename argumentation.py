import argparse
from typing import List, Set, Tuple
from itertools import chain, combinations, product

class Argumentation:
    #Ici on initialise l'argumentation avec les arguments et les attaques
    def __init__(self, arguments, attacks):
        self.arguments = arguments
        self.attacks = attacks

    #Cette fonction permet de parser le fichier avec les arguments et les attaquants et cibles et les mettre dans
    #dans un résolveur d'argumentation
    def fichier_vers_arg(chemin):
        #On crée les ensembles de base du solveur d'argumentation
        arguments = set()
        attaquants = set()
        #On lit le fichier:
        with open(chemin, 'r') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                #Si la ligne contient un argument par exemple arg(A). et bien l'on va ajouter A
                # à l'ensemble des arguments: arg( pour le 4 et ). pour le -2
                if ligne.startswith("arg("):
                    arguments.add(ligne[4:-2])
                #Sinon, il s'agit d'une attaque par exemple att(A,B)., avec ligne
                # [4:-2] on a A,B et on split , du coup on a : A B qui sont les attaquants et cibles
                #et on les ajoute dans les attaques
                elif ligne.startswith("att("):
                    attaquant, cible = ligne[4:-2].split(',')
                    attaquants.add((attaquant.strip(), cible.strip()))
        #Enfin on retourne l'argumentation avec les arguments et les attaquants
        return Argumentation(arguments, attaquants)

  
    #Cette fonction s'occupe de vérifier si un sous ensemble est sans conflit
    def est_sans_conflit(self, sousens):
    #Vérifier s'il existe une attaque dans les paires générées
        return not any(map(lambda s: s in self.attacks, product(sousens, sousens)))
    
    
    #Cette fonction permet de savoir si un sous ensemble défend un arugment
    def defends(self, arg, sousens): 
        for attaquant, cible in self.attacks:
            #On va chercher donc dans les attaques si l'argument est la cible d'une attaque
            if cible == arg:
                #Si oui, on cherche s'il existe un défenseur à la cible
                #Si elle n'existe pas on renvoie False
                if not any((defenseur, attaquant) in self.attacks for defenseur in sousens):
                    return False
        #Sinon True
        return True

    #Cette fonction verifie si un sous ensemble est admissible
    def est_admissible(self, sousens):
       #Pour être admissible il faut qu'il n'y ait pas de conflits et qu'il
       # ne doit pas exister un argument dans sousens qui n'est pas défendu par sousens
       return self.est_sans_conflit(sousens) and not any(not self.defends(arg, sousens) for arg in sousens)
    
    #Cette fonction renvoie les extensions complètes d'une argumentation
    def complete_extensions(self):
        extensions = []
        #Pour chaque sous ensemble de l'argumentation, on va vérifier comme dans le cours:
        for sousens in self.multi_ensemble():
            #Premièrement s'il est admissible:
            if self.est_admissible(sousens):
                #et deuxièmement s'il contient tous les arguments qu'il défend
                defendu = set(arg for arg in self.arguments if self.defends(arg, sousens))
                if sousens == defendu:
                    #Si ces deux conditions passent on ajoute le sous ensemble aux extensions et ainsi de suite
                    extensions.append(sousens)
        return extensions

    #Cette fonction renvoie les extensions stables d'une argumentation
    def stable_extensions(self):
        extensions = []
        #Pour chaque sous ensemble de l'argumentation, on va vérifier comme dans le cours:
        for sousens in self.multi_ensemble():
            #Premièrement, on vérifie s'il est sans conflit
            if self.est_sans_conflit(sousens):
                # Deuxièmement, on cherche les arguments attaqués par le sous-ensemble
                attaques = {cible for attaquant, cible in self.attacks if attaquant in sousens}
                # Et enfin on vérifie si tout argument qui n'est pas dans sousens est attaqué
                if all(arg in attaques  for arg in self.arguments - sousens):
                    extensions.append(sousens)
        return extensions


    #Cette fonction revoie toutes les combinaisons de sous ensemble de l'argumentation
    #Elle est nécessaire pour la recherche d'extensions stables et complètes
    def multi_ensemble(self):
        ensemble = []
        for r in range(len(self.arguments) + 1):
            for combinaison in combinations(self.arguments, r):
                ensemble.append(set(combinaison))
        return ensemble 


