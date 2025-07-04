"""
Service d'export pour le simulateur de feu de forêt.
Responsable de la sauvegarde des fichiers HTML.
"""

import os
from typing import Dict, Any, List, Tuple

from config.report_config import DEFAULT_EXPORT_FOLDER, DEFAULT_ENCODING


class ExportService:
    """Service d'export des rapports HTML."""
    
    @staticmethod
    def create_export_directory(dossier_sortie: str) -> None:
        """
        Crée le dossier de sortie s'il n'existe pas.
        
        Args:
            dossier_sortie: Chemin du dossier de sortie
        """
        os.makedirs(dossier_sortie, exist_ok=True)
    
    @staticmethod
    def save_html_files(files_data: List[Tuple[str, str]], dossier_sortie: str) -> None:
        """
        Sauvegarde les fichiers HTML dans le dossier de sortie.
        
        Args:
            files_data: Liste de tuples (nom_fichier, contenu_html)
            dossier_sortie: Chemin du dossier de sortie
        """
        ExportService.create_export_directory(dossier_sortie)
        
        for nom_fichier, contenu_html in files_data:
            chemin_fichier = os.path.join(dossier_sortie, nom_fichier)
            ExportService._save_single_file(chemin_fichier, contenu_html)
            print(f"✅ Fichier généré: {chemin_fichier}")
    
    @staticmethod
    def _save_single_file(chemin_fichier: str, contenu_html: str) -> None:
        """
        Sauvegarde un fichier HTML unique.
        
        Args:
            chemin_fichier: Chemin complet du fichier
            contenu_html: Contenu HTML à écrire
        """
        with open(chemin_fichier, 'w', encoding=DEFAULT_ENCODING) as f:
            f.write(contenu_html)
    
    @staticmethod
    def print_export_summary(dossier_sortie: str) -> None:
        """
        Affiche un résumé de l'export.
        
        Args:
            dossier_sortie: Chemin du dossier de sortie
        """
        print(f"\n🎉 Export HTML terminé! Fichiers sauvegardés dans le dossier '{dossier_sortie}'")
        print("Ouvrez les fichiers .html dans votre navigateur pour visualiser les résultats.")
    
    @staticmethod
    def get_default_export_folder() -> str:
        """
        Retourne le dossier d'export par défaut.
        
        Returns:
            Nom du dossier d'export par défaut
        """
        return DEFAULT_EXPORT_FOLDER