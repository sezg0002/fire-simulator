"""
Configuration centralisée pour le générateur de rapports HTML du simulateur de feu de forêt.
"""

from src.TerrainType import TerrainType

# Configuration des couleurs pour chaque type de terrain
TERRAIN_COLORS = {
    TerrainType.TERRAIN_NU.value: '#D2B48C',  # Beige pour terrain nu
    TerrainType.ARBRE.value: '#228B22',       # Vert pour les arbres
    TerrainType.EAU.value: '#4169E1',         # Bleu pour l'eau
    TerrainType.BRULE.value: '#DC143C'        # Rouge pour les zones brûlées
}

# Configuration des symboles pour chaque type de terrain
TERRAIN_SYMBOLS = {
    TerrainType.TERRAIN_NU.value: '.',
    TerrainType.ARBRE.value: '🌲',
    TerrainType.EAU.value: '💧',
    TerrainType.BRULE.value: '🔥'
}

# Configuration des styles CSS
CSS_STYLES = {
    'case_width': '20px',
    'case_height': '20px',
    'case_font_size': '12px',
    'case_border': '1px solid #888',
    'grid_gap': '1px',
    'grid_background': '#ddd',
    'grid_padding': '10px',
    'container_max_width': '1200px',
    'container_background': 'white',
    'container_padding': '20px',
    'container_border_radius': '10px',
    'container_box_shadow': '0 2px 10px rgba(0,0,0,0.1)',
    'body_background': '#f5f5f5',
    'description_background': '#e8f4f8',
    'description_border': '5px solid #007acc',
    'legende_background': '#f0f0f0',
    'legende_border_radius': '15px',
    'legende_couleur_size': '15px'
}

# Configuration des noms de fichiers d'export
EXPORT_FILENAMES = {
    'original': 'carte_originale.html',
    'sans_deboisement': 'carte_apres_incendie.html',
    'avec_deboisement': 'carte_avec_deboisement.html'
}

# Configuration des titres
TITLES = {
    'original': 'Carte Originale de la Forêt',
    'sans_deboisement': 'Carte Après Incendie (Sans Déboisement)',
    'avec_deboisement': 'Carte Après Incendie (Avec Déboisement Optimal)'
}

# Configuration des légendes
LEGENDE_LABELS = {
    TerrainType.TERRAIN_NU.value: 'Terrain nu (.)',
    TerrainType.ARBRE.value: 'Arbres (🌲)',
    TerrainType.EAU.value: 'Eau (💧)',
    TerrainType.BRULE.value: 'Zone brûlée (🔥)'
}

# Configuration par défaut
DEFAULT_EXPORT_FOLDER = 'exports_html'
DEFAULT_ENCODING = 'utf-8'
DATE_FORMAT = '%d/%m/%Y à %H:%M:%S'