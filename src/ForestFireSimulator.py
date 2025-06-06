import random
import numpy as np

from TerrainType import TerrainType


"""
Simulateur de feux de forêts avec génération de carte aléatoire
"""
class ForestFireSimulator:
    
    def __init__(self, largeur: int = 50, hauteur: int = 50):
        
        self.largeur = largeur
        self.hauteur = hauteur
        self.carte = np.zeros((hauteur, largeur), dtype=int)
    

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
    

    def afficher_carte(self, utiliser_symboles: bool = True):
        symboles_affichage = {
            TerrainType.TERRAIN_NU: '.',
            TerrainType.ARBRE: '🌲',
            TerrainType.EAU: '💧'
        }
        
        print("\n" + "="*50)
        print("CARTE DE LA FORÊT")
        print("="*50)
        
        for i in range(self.hauteur):
            ligne = ""
            for j in range(self.largeur):
                terrain = TerrainType(self.carte[i, j])
                ligne += symboles_affichage[terrain] + " "
            print(ligne)
        
        print("="*50)
    

    def obtenir_statistiques(self) -> dict:
        
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
        np.save(nom_fichier, self.carte)
        print(f"Carte sauvegardée dans {nom_fichier}.npy")
    

    def charger_carte(self, nom_fichier: str):
        try:
            self.carte = np.load(nom_fichier)
            self.hauteur, self.largeur = self.carte.shape
            print(f"Carte chargée depuis {nom_fichier}")
        except FileNotFoundError:
            print(f"Erreur: Fichier {nom_fichier} non trouvé")
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")


