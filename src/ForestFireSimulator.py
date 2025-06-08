import random
import numpy as np
from collections import deque
from enum import Enum


class TerrainType(Enum):
    """Énumération des différents types de terrain"""
    TERRAIN_NU = 0     
    ARBRE = 1           
    EAU = 2             
    FEU = 3             
    BRULE = 4           

class ForestFireSimulator:
    """
    Simulateur de feux de forêts avec génération de carte aléatoire
    """
    
    def __init__(self, largeur: int = 50, hauteur: int = 50):
        self.largeur = largeur
        self.hauteur = hauteur
        self.carte = np.zeros((hauteur, largeur), dtype=int)
        self.carte_incendie = None  
    

    def generer_carte_aleatoire(self, pourcentage_arbres: float = 60.0, pourcentage_eau: float = 10.0):
        
        if pourcentage_arbres + pourcentage_eau > 100:
            raise ValueError("La somme des pourcentages ne peut pas dépasser 100%")
        
        total_cases = self.largeur * self.hauteur
        nb_arbres = int(total_cases * pourcentage_arbres / 100)
        nb_eau = int(total_cases * pourcentage_eau / 100)
        
        positions = [(i, j) for i in range(self.hauteur) for j in range(self.largeur)]
        random.shuffle(positions)
        
        self.carte.fill(TerrainType.TERRAIN_NU.value)
        
        for k in range(nb_arbres):
            i, j = positions[k]
            self.carte[i, j] = TerrainType.ARBRE.value
        
        for k in range(nb_arbres, nb_arbres + nb_eau):
            i, j = positions[k]
            self.carte[i, j] = TerrainType.EAU.value
        
        print(f"Carte générée: {nb_arbres} arbres ({pourcentage_arbres}%), "
              f"{nb_eau} plans d'eau ({pourcentage_eau}%), "
              f"{total_cases - nb_arbres - nb_eau} terrain nu")
    

    def obtenir_voisins(self, ligne: int, colonne: int) -> list:
        """
        Retourne les coordonnées des 8 voisins (y compris diagonales) d'une case
        """
        voisins = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:  
                    continue
                ni, nj = ligne + di, colonne + dj
                if 0 <= ni < self.hauteur and 0 <= nj < self.largeur:
                    voisins.append((ni, nj))
        return voisins
    
    def simuler_incendie(self, ligne_depart: int = None, colonne_depart: int = None) -> dict:
        """
        Simule un incendie en partant d'une position donnée ou d'une position aléatoire avec un arbre       
        """
        
        if (ligne_depart is None or colonne_depart is None or 
            not (0 <= ligne_depart < self.hauteur and 0 <= colonne_depart < self.largeur) or
            self.carte[ligne_depart, colonne_depart] != TerrainType.ARBRE.value):
            
            positions_arbres = []
            for i in range(self.hauteur):
                for j in range(self.largeur):
                    if self.carte[i, j] == TerrainType.ARBRE.value:
                        positions_arbres.append((i, j))
            
            if not positions_arbres:
                print("Erreur: Aucun arbre trouvé sur la carte!")
                return {
                    'arbres_brules': 0, 
                    'arbres_originaux': 0,
                    'pourcentage_brule': 0.0,
                    'position_depart': None
                }
            
            ligne_depart, colonne_depart = random.choice(positions_arbres)
            print(f"Position automatique choisie: ({ligne_depart}, {colonne_depart}) - arbre trouvé!")
        
        self.carte_incendie = self.carte.copy()
        
        print(f"🔥 Démarrage de l'incendie à la position ({ligne_depart}, {colonne_depart})")
        
        # Utiliser BFS (Breadth-First Search) pour simuler la propagation
        queue = deque([(ligne_depart, colonne_depart)])
        cases_brulees = set()
        cases_brulees.add((ligne_depart, colonne_depart))
        
        self.carte_incendie[ligne_depart, colonne_depart] = TerrainType.BRULE.value
        
        while queue:
            ligne_actuelle, colonne_actuelle = queue.popleft()
            
            for ni, nj in self.obtenir_voisins(ligne_actuelle, colonne_actuelle):
                if (self.carte_incendie[ni, nj] == TerrainType.ARBRE.value and 
                    (ni, nj) not in cases_brulees):
                    
                    self.carte_incendie[ni, nj] = TerrainType.BRULE.value
                    cases_brulees.add((ni, nj))
                    queue.append((ni, nj))
        
        nb_arbres_brules = len(cases_brulees)
        nb_arbres_originaux = np.sum(self.carte == TerrainType.ARBRE.value)
        pourcentage_brule = (nb_arbres_brules / nb_arbres_originaux * 100) if nb_arbres_originaux > 0 else 0
        
        stats = {
            'arbres_brules': nb_arbres_brules,
            'arbres_originaux': nb_arbres_originaux,
            'pourcentage_brule': pourcentage_brule,
            'position_depart': (ligne_depart, colonne_depart)
        }
        
        print(f"Incendie simulé: {nb_arbres_brules}/{nb_arbres_originaux} arbres brûlés ({pourcentage_brule:.1f}%)")
        return stats
    
    def afficher_carte(self, utiliser_symboles: bool = True, afficher_incendie: bool = False):
        """
        Affiche la carte dans la console
        """
        carte_a_afficher = self.carte_incendie if afficher_incendie and self.carte_incendie is not None else self.carte
        
        if utiliser_symboles:
            symboles_affichage = {
                TerrainType.TERRAIN_NU.value: '.',
                TerrainType.ARBRE.value: '🌲',
                TerrainType.EAU.value: '💧',
                TerrainType.FEU.value: '🔥',
                TerrainType.BRULE.value: '🔥'  
            }
        else:
            symboles_affichage = {
                TerrainType.TERRAIN_NU.value: '.',
                TerrainType.ARBRE.value: 'T',
                TerrainType.EAU.value: 'W',
                TerrainType.FEU.value: 'F',
                TerrainType.BRULE.value: 'X'  
            }
        
        titre = "CARTE APRÈS INCENDIE" if afficher_incendie else "CARTE DE LA FORÊT"
        print("\n" + "="*50)
        print(titre)
        print("="*50)
        
        for i in range(self.hauteur):
            ligne = ""
            for j in range(self.largeur):
                valeur = carte_a_afficher[i, j]
                symbole = symboles_affichage.get(valeur, '?')
                ligne += symbole + " "
            print(ligne)
        
        print("="*50)
        
        if afficher_incendie:
            print("Légende: . = terrain nu, T/🌲 = arbre, W/💧 = eau, F/🔥 = feu/brûlé, X = arbre brûlé")
    

    def demarrer_incendie_aleatoire(self) -> dict:
        """
        Démarre un incendie à une position aléatoire contenant un arbre
        """
        return self.simuler_incendie()
    

    def obtenir_statistiques(self) -> dict:
        """Retourne les statistiques de la carte actuelle"""
        total_cases = self.largeur * self.hauteur
        
        compteurs = {
            'terrain_nu': np.sum(self.carte == TerrainType.TERRAIN_NU.value),
            'arbres': np.sum(self.carte == TerrainType.ARBRE.value),
            'eau': np.sum(self.carte == TerrainType.EAU.value)
        }
        
        pourcentages = {
            f'{cle}_pct': (valeur / total_cases) * 100 
            for cle, valeur in compteurs.items()
        }
        
        return {**compteurs, **pourcentages, 'total': total_cases}
    
    def sauvegarder_carte(self, nom_fichier: str):
        """Sauvegarde la carte dans un fichier numpy"""
        np.save(nom_fichier, self.carte)
        print(f"Carte sauvegardée dans {nom_fichier}.npy")
    
    def charger_carte(self, nom_fichier: str):
        """Charge une carte depuis un fichier numpy"""
        try:
            self.carte = np.load(nom_fichier)
            self.hauteur, self.largeur = self.carte.shape
            print(f"Carte chargée depuis {nom_fichier}")
        except FileNotFoundError:
            print(f"Erreur: Fichier {nom_fichier} non trouvé")
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")