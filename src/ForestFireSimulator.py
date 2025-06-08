import random
import numpy as np
from collections import deque
from enum import Enum
from typing import Tuple, List, Dict, Any
import os
from datetime import datetime

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
    Simulateur de feux de forêts avec génération de carte aléatoire et export HTML
    """

    def __init__(self, largeur: int = 50, hauteur: int = 50):
        self.largeur = largeur
        self.hauteur = hauteur
        self.carte = np.zeros((hauteur, largeur), dtype=int)
        self.carte_incendie = None
        self.donnees_simulation = {}  # Stockage des données pour l'export HTML

    def generer_carte_aleatoire(self, pourcentage_arbres: float = 60.0, pourcentage_eau: float = 10.0):
        """Génère une carte aléatoire avec des arbres et des plans d'eau"""
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

        # Stocker les informations de génération
        self.donnees_simulation['generation'] = {
            'nb_arbres': nb_arbres,
            'pourcentage_arbres': pourcentage_arbres,
            'nb_eau': nb_eau,
            'pourcentage_eau': pourcentage_eau,
            'terrain_nu': total_cases - nb_arbres - nb_eau,
            'total_cases': total_cases
        }

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
        print("\n" + "=" * 50)
        print(titre)
        print("=" * 50)

        for i in range(self.hauteur):
            ligne = ""
            for j in range(self.largeur):
                valeur = carte_a_afficher[i, j]
                symbole = symboles_affichage.get(valeur, '?')
                ligne += symbole + " "
            print(ligne)

        print("=" * 50)

        if afficher_incendie:
            print("Légende: . = terrain nu, T/🌲 = arbre, W/💧 = eau, F/🔥 = feu/brûlé, X = arbre brûlé")

    def demarrer_incendie_aleatoire(self) -> dict:
        """
        Démarre un incendie à une position aléatoire contenant un arbre
        """
        return self.simuler_incendie()

    def trouver_meilleure_case_a_deboiser(self, ligne_incendie: int, colonne_incendie: int) -> dict:
        if self.carte[ligne_incendie, colonne_incendie] != TerrainType.ARBRE.value:
            return {'erreur': 'Pas d\'arbre à la position d\'incendie spécifiée'}

        stats_reference = self.simuler_incendie(ligne_incendie, colonne_incendie)
        arbres_brules_reference = stats_reference['arbres_brules']

        positions_arbres = []
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if (self.carte[i, j] == TerrainType.ARBRE.value and
                        not (i == ligne_incendie and j == colonne_incendie)):
                    positions_arbres.append((i, j))

        if not positions_arbres:
            return {'erreur': 'Aucun autre arbre à déboiser sur la carte'}

        meilleure_position = None
        meilleure_reduction = 0
        meilleur_resultat = arbres_brules_reference

        for i, j in positions_arbres:
            valeur_originale = self.carte[i, j]
            self.carte[i, j] = TerrainType.TERRAIN_NU.value

            queue = deque([(ligne_incendie, colonne_incendie)])
            cases_brulees = set()
            cases_brulees.add((ligne_incendie, colonne_incendie))
            carte_temp = self.carte.copy()
            carte_temp[ligne_incendie, colonne_incendie] = TerrainType.BRULE.value

            while queue:
                ligne_actuelle, colonne_actuelle = queue.popleft()
                for ni, nj in self.obtenir_voisins(ligne_actuelle, colonne_actuelle):
                    if (carte_temp[ni, nj] == TerrainType.ARBRE.value and
                            (ni, nj) not in cases_brulees):
                        carte_temp[ni, nj] = TerrainType.BRULE.value
                        cases_brulees.add((ni, nj))
                        queue.append((ni, nj))

            arbres_brules_test = len(cases_brulees)
            reduction = arbres_brules_reference - arbres_brules_test

            if reduction > meilleure_reduction:
                meilleure_reduction = reduction
                meilleure_position = (i, j)
                meilleur_resultat = arbres_brules_test

            self.carte[i, j] = valeur_originale

        pourcentage_reduction = (
                    meilleure_reduction / arbres_brules_reference * 100) if arbres_brules_reference > 0 else 0

        return {
            'position_deboisement': meilleure_position,
            'arbres_brules_sans_deboisement': arbres_brules_reference,
            'arbres_brules_avec_deboisement': meilleur_resultat,
            'arbres_sauves': meilleure_reduction,
            'pourcentage_reduction': pourcentage_reduction,
            'position_incendie': (ligne_incendie, colonne_incendie)
        }

    def appliquer_deboisement_et_simuler(self, ligne_incendie: int, colonne_incendie: int,
                                         ligne_deboisement: int, colonne_deboisement: int) -> dict:
        if self.carte[ligne_deboisement, colonne_deboisement] != TerrainType.ARBRE.value:
            return {'erreur': 'Pas d\'arbre à la position de déboisement spécifiée'}

        valeur_originale = self.carte[ligne_deboisement, colonne_deboisement]
        self.carte[ligne_deboisement, colonne_deboisement] = TerrainType.TERRAIN_NU.value

        stats = self.simuler_incendie(ligne_incendie, colonne_incendie)

        self.carte[ligne_deboisement, colonne_deboisement] = valeur_originale

        return stats

    def simulation_complete_avec_deboisement(self, ligne_incendie: int = None, colonne_incendie: int = None) -> Dict[
        str, Any]:
        """
        Version modifiée qui retourne les données au lieu de seulement les afficher
        """
        if (ligne_incendie is None or colonne_incendie is None or
                not (0 <= ligne_incendie < self.hauteur and 0 <= colonne_incendie < self.largeur) or
                self.carte[ligne_incendie, colonne_incendie] != TerrainType.ARBRE.value):

            positions_arbres = []
            for i in range(self.hauteur):
                for j in range(self.largeur):
                    if self.carte[i, j] == TerrainType.ARBRE.value:
                        positions_arbres.append((i, j))

            if not positions_arbres:
                print("Erreur: Aucun arbre trouvé sur la carte!")
                return {}

            ligne_incendie, colonne_incendie = random.choice(positions_arbres)

        # Capturer les données pour l'export HTML
        donnees_export = {}

        # 1. Carte originale et statistiques
        stats_orig = self.obtenir_statistiques()
        donnees_export['carte_originale'] = self.carte.copy()
        donnees_export['stats_originales'] = stats_orig
        donnees_export['position_incendie'] = (ligne_incendie, colonne_incendie)

        # 2. Simulation sans déboisement
        stats_sans = self.simuler_incendie(ligne_incendie, colonne_incendie)
        donnees_export['carte_sans_deboisement'] = self.carte_incendie.copy()
        donnees_export['stats_sans_deboisement'] = stats_sans

        # 3. Trouver la meilleure case à déboiser
        resultat_deboisement = self.trouver_meilleure_case_a_deboiser(ligne_incendie, colonne_incendie)

        if 'erreur' in resultat_deboisement:
            print(f"Erreur: {resultat_deboisement['erreur']}")
            return donnees_export

        pos_deboisement = resultat_deboisement['position_deboisement']
        donnees_export['position_deboisement'] = pos_deboisement
        donnees_export['resultats_deboisement'] = resultat_deboisement

        # 4. Simulation avec déboisement
        stats_avec = self.appliquer_deboisement_et_simuler(ligne_incendie, colonne_incendie, pos_deboisement[0],
                                                           pos_deboisement[1])
        donnees_export['carte_avec_deboisement'] = self.carte_incendie.copy()
        donnees_export['stats_avec_deboisement'] = stats_avec

        # 5. Calculs de comparaison
        arbres_sauves = stats_sans['arbres_brules'] - stats_avec['arbres_brules']
        taux_reduction = (arbres_sauves / stats_sans['arbres_brules'] * 100) if stats_sans['arbres_brules'] > 0 else 0

        donnees_export['comparaison'] = {
            'arbres_sauves': arbres_sauves,
            'taux_reduction': taux_reduction
        }

        # Stocker pour utilisation ultérieure
        self.donnees_simulation = donnees_export

        # Affichage console (conservé pour compatibilité)
        print("=== CARTE ORIGINALE ===")
        self.afficher_carte(utiliser_symboles=True, afficher_incendie=False)

        print(f"\nStatistiques de la carte:")
        print(f"- Terrain nu: {stats_orig['terrain_nu']} cases ({stats_orig['terrain_nu_pct']:.1f}%)")
        print(f"- Arbres: {stats_orig['arbres']} cases ({stats_orig['arbres_pct']:.1f}%)")
        print(f"- Eau: {stats_orig['eau']} cases ({stats_orig['eau_pct']:.1f}%)")
        print(f"- Total: {stats_orig['total']} cases")

        print(f"\nPosition de l'incendie: ({ligne_incendie}, {colonne_incendie})")

        print("\n=== CARTE BRÛLÉE SANS DÉBOISEMENT ===")
        self.carte_incendie = donnees_export['carte_sans_deboisement']
        self.afficher_carte(utiliser_symboles=True, afficher_incendie=True)

        print(f"\nRésultats de l'incendie:")
        print(f"- Position de départ: {stats_sans['position_depart']}")
        print(f"- Arbres brûlés: {stats_sans['arbres_brules']}")
        print(f"- Arbres originaux: {stats_sans['arbres_originaux']}")
        print(f"- Pourcentage brûlé: {stats_sans['pourcentage_brule']:.1f}%")

        print(f"\n=== CARTE BRÛLÉE AVEC DÉBOISEMENT (case {pos_deboisement}) ===")
        self.carte_incendie = donnees_export['carte_avec_deboisement']
        self.afficher_carte(utiliser_symboles=True, afficher_incendie=True)

        print(f"\nRésultats de l'incendie avec déboisement:")
        print(f"- Position de départ: {stats_avec['position_depart']}")
        print(f"- Arbres brûlés: {stats_avec['arbres_brules']}")
        print(f"- Arbres originaux: {stats_avec['arbres_originaux']}")
        print(f"- Pourcentage brûlé: {stats_avec['pourcentage_brule']:.1f}%")

        print(f"\nComparaison:")
        print(f"- Case déboisée: {pos_deboisement}")
        print(f"- Arbres sauvés: {arbres_sauves}")
        print(f"- Taux de réduction: {taux_reduction:.1f}%")

        return donnees_export

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

    def _generer_html_carte(self, carte: np.ndarray, titre: str, description: str = "") -> str:
        """Génère le HTML pour une carte donnée"""
        # Couleurs pour chaque type de terrain
        couleurs = {
            TerrainType.TERRAIN_NU.value: '#D2B48C',  # Beige pour terrain nu
            TerrainType.ARBRE.value: '#228B22',  # Vert pour les arbres
            TerrainType.EAU.value: '#4169E1',  # Bleu pour l'eau
            TerrainType.BRULE.value: '#DC143C'  # Rouge pour les zones brûlées
        }

        symboles = {
            TerrainType.TERRAIN_NU.value: '.',
            TerrainType.ARBRE.value: '🌲',
            TerrainType.EAU.value: '💧',
            TerrainType.BRULE.value: '🔥'
        }

        html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titre}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .description {{
                    background-color: #e8f4f8;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    border-left: 5px solid #007acc;
                }}
                .carte {{
                    display: grid;
                    grid-template-columns: repeat({self.largeur}, 1fr);
                    gap: 1px;
                    background-color: #ddd;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 20px auto;
                    width: fit-content;
                }}
                .case {{
                    width: 20px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    border: 1px solid #888;
                }}
                .legende {{
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin-top: 20px;
                    flex-wrap: wrap;
                }}
                .legende-item {{
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    padding: 5px 10px;
                    background-color: #f0f0f0;
                    border-radius: 15px;
                }}
                .legende-couleur {{
                    width: 15px;
                    height: 15px;
                    border: 1px solid #333;
                    border-radius: 3px;
                }}
                .timestamp {{
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{titre}</h1>
                {f'<div class="description">{description}</div>' if description else ''}

                <div class="carte">
        """

        # Générer la grille
        for i in range(self.hauteur):
            for j in range(self.largeur):
                valeur = carte[i, j]
                couleur = couleurs.get(valeur, '#FFFFFF')
                symbole = symboles.get(valeur, '?')
                html += f'<div class="case" style="background-color: {couleur};" title="Ligne {i}, Colonne {j}: {symbole}">{symbole}</div>\n'

        html += """
                </div>

                <div class="legende">
                    <div class="legende-item">
                        <div class="legende-couleur" style="background-color: #D2B48C;"></div>
                        <span>Terrain nu (.)</span>
                    </div>
                    <div class="legende-item">
                        <div class="legende-couleur" style="background-color: #228B22;"></div>
                        <span>Arbres (🌲)</span>
                    </div>
                    <div class="legende-item">
                        <div class="legende-couleur" style="background-color: #4169E1;"></div>
                        <span>Eau (💧)</span>
                    </div>
                    <div class="legende-item">
                        <div class="legende-couleur" style="background-color: #DC143C;"></div>
                        <span>Zone brûlée (🔥)</span>
                    </div>
                </div>

                <div class="timestamp">
                    Généré le """ + datetime.now().strftime("%d/%m/%Y à %H:%M:%S") + """
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def exporter_html(self, dossier_sortie: str = "exports_html"):
        """
        Exporte les trois états de la simulation en HTML
        """
        if not self.donnees_simulation:
            print("Erreur: Aucune simulation n'a été effectuée. Lancez d'abord simulation_complete_avec_deboisement()")
            return

        # Créer le dossier de sortie
        os.makedirs(dossier_sortie, exist_ok=True)

        donnees = self.donnees_simulation

        # 1. Carte originale
        stats_orig = donnees['stats_originales']
        description_orig = f"""
        <strong>Statistiques de la carte originale :</strong><br>
        • Dimension : {self.hauteur} × {self.largeur} ({stats_orig['total']} cases)<br>
        • Arbres : {stats_orig['arbres']} cases ({stats_orig['arbres_pct']:.1f}%)<br>
        • Eau : {stats_orig['eau']} cases ({stats_orig['eau_pct']:.1f}%)<br>
        • Terrain nu : {stats_orig['terrain_nu']} cases ({stats_orig['terrain_nu_pct']:.1f}%)<br>
        • Position de l'incendie : {donnees['position_incendie']}
        """

        html_original = self._generer_html_carte(
            donnees['carte_originale'],
            "Carte Originale de la Forêt",
            description_orig
        )

        # 2. Carte après incendie (sans déboisement)
        stats_sans = donnees['stats_sans_deboisement']
        description_sans = f"""
        <strong>Résultats de l'incendie sans déboisement :</strong><br>
        • Position de départ : {stats_sans['position_depart']}<br>
        • Arbres brûlés : {stats_sans['arbres_brules']} / {stats_sans['arbres_originaux']}<br>
        • Pourcentage brûlé : {stats_sans['pourcentage_brule']:.1f}%
        """

        html_sans_deboisement = self._generer_html_carte(
            donnees['carte_sans_deboisement'],
            "Carte Après Incendie (Sans Déboisement)",
            description_sans
        )

        # 3. Carte après incendie avec déboisement
        stats_avec = donnees['stats_avec_deboisement']
        comp = donnees['comparaison']
        description_avec = f"""
        <strong>Résultats de l'incendie avec déboisement :</strong><br>
        • Position déboisée : {donnees['position_deboisement']}<br>
        • Arbres brûlés : {stats_avec['arbres_brules']} / {stats_avec['arbres_originaux']}<br>
        • Pourcentage brûlé : {stats_avec['pourcentage_brule']:.1f}%<br>
        <br>
        <strong>Efficacité du déboisement :</strong><br>
        • Arbres sauvés : {comp['arbres_sauves']}<br>
        • Taux de réduction : {comp['taux_reduction']:.1f}%
        """

        html_avec_deboisement = self._generer_html_carte(
            donnees['carte_avec_deboisement'],
            "Carte Après Incendie (Avec Déboisement Optimal)",
            description_avec
        )

        # Sauvegarder les fichiers
        fichiers = [
            ("carte_originale.html", html_original),
            ("carte_apres_incendie.html", html_sans_deboisement),
            ("carte_avec_deboisement.html", html_avec_deboisement)
        ]

        for nom_fichier, contenu_html in fichiers:
            chemin_fichier = os.path.join(dossier_sortie, nom_fichier)
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                f.write(contenu_html)
            print(f"✅ Fichier généré: {chemin_fichier}")

        print(f"\n🎉 Export HTML terminé! Fichiers sauvegardés dans le dossier '{dossier_sortie}'")
        print("Ouvrez les fichiers .html dans votre navigateur pour visualiser les résultats.")

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