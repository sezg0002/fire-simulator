"""
Service de génération de templates HTML pour le simulateur de feu de forêt.
Responsable de la création des fichiers HTML avec les cartes et statistiques.
"""

import numpy as np
from datetime import datetime
from typing import Dict, Any

from config.report_config import (
    TERRAIN_COLORS, TERRAIN_SYMBOLS, CSS_STYLES, LEGENDE_LABELS, DATE_FORMAT
)


class HtmlTemplateBuilder:
    """Générateur de templates HTML pour les cartes de simulation."""
    
    def __init__(self, largeur: int, hauteur: int):
        """
        Initialise le générateur de templates HTML.
        
        Args:
            largeur: Largeur de la carte
            hauteur: Hauteur de la carte
        """
        self.largeur = largeur
        self.hauteur = hauteur
    
    def generate_html_carte(self, carte: np.ndarray, titre: str, description: str = "") -> str:
        """
        Génère le HTML complet pour une carte donnée.
        
        Args:
            carte: Matrice numpy représentant la carte
            titre: Titre de la page HTML
            description: Description HTML à afficher
            
        Returns:
            String contenant le HTML complet
        """
        html = self._generate_html_header(titre)
        html += self._generate_html_body_start(titre, description)
        html += self._generate_carte_grid(carte)
        html += self._generate_legende()
        html += self._generate_html_footer()
        
        return html
    
    def _generate_html_header(self, titre: str) -> str:
        """Génère l'en-tête HTML avec les styles CSS."""
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titre}</title>
            <style>
                {self._generate_css_styles()}
            </style>
        </head>
        """
    
    def _generate_css_styles(self) -> str:
        """Génère les styles CSS à partir de la configuration."""
        styles = CSS_STYLES
        return f"""
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: {styles['body_background']};
                }}
                .container {{
                    max-width: {styles['container_max_width']};
                    margin: 0 auto;
                    background-color: {styles['container_background']};
                    padding: {styles['container_padding']};
                    border-radius: {styles['container_border_radius']};
                    box-shadow: {styles['container_box_shadow']};
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .description {{
                    background-color: {styles['description_background']};
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    border-left: {styles['description_border']};
                }}
                .carte {{
                    display: grid;
                    grid-template-columns: repeat({self.largeur}, 1fr);
                    gap: {styles['grid_gap']};
                    background-color: {styles['grid_background']};
                    padding: {styles['grid_padding']};
                    border-radius: 5px;
                    margin: 20px auto;
                    width: fit-content;
                }}
                .case {{
                    width: {styles['case_width']};
                    height: {styles['case_height']};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: {styles['case_font_size']};
                    border: {styles['case_border']};
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
                    background-color: {styles['legende_background']};
                    border-radius: {styles['legende_border_radius']};
                }}
                .legende-couleur {{
                    width: {styles['legende_couleur_size']};
                    height: {styles['legende_couleur_size']};
                    border: 1px solid #333;
                    border-radius: 3px;
                }}
                .timestamp {{
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                    margin-top: 20px;
                }}
        """
    
    def _generate_html_body_start(self, titre: str, description: str) -> str:
        """Génère le début du body HTML."""
        description_html = f'<div class="description">{description}</div>' if description else ''
        return f"""
        <body>
            <div class="container">
                <h1>{titre}</h1>
                {description_html}

                <div class="carte">
        """
    
    def _generate_carte_grid(self, carte: np.ndarray) -> str:
        """Génère la grille HTML représentant la carte."""
        grid_html = ""
        for i in range(self.hauteur):
            for j in range(self.largeur):
                valeur = carte[i, j]
                couleur = TERRAIN_COLORS.get(valeur, '#FFFFFF')
                symbole = TERRAIN_SYMBOLS.get(valeur, '?')
                tooltip = f"Ligne {i}, Colonne {j}: {symbole}"
                grid_html += f'<div class="case" style="background-color: {couleur};" title="{tooltip}">{symbole}</div>\n'
        return grid_html
    
    def _generate_legende(self) -> str:
        """Génère la légende HTML."""
        legende_html = """
                </div>

                <div class="legende">
        """
        
        for terrain_type, label in LEGENDE_LABELS.items():
            couleur = TERRAIN_COLORS[terrain_type]
            legende_html += f"""
                    <div class="legende-item">
                        <div class="legende-couleur" style="background-color: {couleur};"></div>
                        <span>{label}</span>
                    </div>
            """
        
        legende_html += """
                </div>
        """
        return legende_html
    
    def _generate_html_footer(self) -> str:
        """Génère le pied de page HTML."""
        timestamp = datetime.now().strftime(DATE_FORMAT)
        return f"""
                <div class="timestamp">
                    Généré le {timestamp}
                </div>
            </div>
        </body>
        </html>
        """