#!/usr/bin/env python3
"""
Test unitaire pour vérifier le bon fonctionnement des services refactorisés.
"""

import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.data.data_processor import DataProcessor
from services.html.html_template_builder import HtmlTemplateBuilder
from services.export.export_service import ExportService
from src.TerrainType import TerrainType


class TestRefactoredServices(unittest.TestCase):
    
    def setUp(self):
        self.sample_simulation_data = {
            'carte_originale': np.array([[1, 0, 2], [1, 1, 0], [0, 1, 1]]),
            'carte_sans_deboisement': np.array([[4, 0, 2], [4, 4, 0], [0, 4, 4]]),
            'carte_avec_deboisement': np.array([[4, 0, 2], [4, 1, 0], [0, 4, 4]]),
            'stats_originales': {
                'arbres': 5,
                'eau': 1,
                'terrain_nu': 3,
                'total': 9,
                'arbres_pct': 55.6,
                'eau_pct': 11.1,
                'terrain_nu_pct': 33.3
            },
            'stats_sans_deboisement': {
                'position_depart': (0, 0),
                'arbres_brules': 5,
                'arbres_originaux': 5,
                'pourcentage_brule': 100.0
            },
            'stats_avec_deboisement': {
                'position_depart': (0, 0),
                'arbres_brules': 4,
                'arbres_originaux': 4,
                'pourcentage_brule': 100.0
            },
            'position_incendie': (0, 0),
            'position_deboisement': (1, 1),
            'comparaison': {
                'arbres_sauves': 1,
                'taux_reduction': 20.0
            }
        }
    
    def test_data_processor_prepare_export_data(self):
        """Test de la préparation des données d'export."""
        export_data = DataProcessor.prepare_export_data(
            self.sample_simulation_data, 3, 3
        )
        
        # Vérifier que les trois types de cartes sont présents
        self.assertIn('original', export_data)
        self.assertIn('sans_deboisement', export_data)
        self.assertIn('avec_deboisement', export_data)
        
        # Vérifier que chaque type contient les clés nécessaires
        for key in export_data:
            data = export_data[key]
            self.assertIn('carte', data)
            self.assertIn('title', data)
            self.assertIn('description', data)
            self.assertIn('filename', data)
    
    def test_data_processor_format_statistics(self):
        """Test du formatage des statistiques."""
        # Test des statistiques originales
        original_stats = {
            'hauteur': 3,
            'largeur': 3,
            'stats': self.sample_simulation_data['stats_originales'],
            'position_incendie': (0, 0)
        }
        description = DataProcessor.format_statistics_description(
            original_stats, 'original'
        )
        self.assertIn('Statistiques de la carte originale', description)
        self.assertIn('3 × 3', description)
        self.assertIn('5 cases', description)
        
        # Test des statistiques sans déboisement
        description = DataProcessor.format_statistics_description(
            self.sample_simulation_data['stats_sans_deboisement'], 'sans_deboisement'
        )
        self.assertIn('Résultats de l\'incendie sans déboisement', description)
        self.assertIn('5 / 5', description)
    
    def test_html_template_builder(self):
        """Test de la génération de templates HTML."""
        builder = HtmlTemplateBuilder(3, 3)
        
        carte = np.array([[1, 0, 2], [1, 1, 0], [0, 1, 1]])
        html = builder.generate_html_carte(
            carte, 
            "Test Carte", 
            "Description de test"
        )
        
        # Vérifier que le HTML contient les éléments essentiels
        self.assertIn('<!DOCTYPE html>', html)
        self.assertIn('Test Carte', html)
        self.assertIn('Description de test', html)
        self.assertIn('grid-template-columns: repeat(3, 1fr)', html)
        self.assertIn('🌲', html)  # Symbole d'arbre
        self.assertIn('💧', html)  # Symbole d'eau
        self.assertIn('#228B22', html)  # Couleur des arbres
        self.assertIn('#4169E1', html)  # Couleur de l'eau
        self.assertIn('Généré le', html)
        
    def test_export_service_methods(self):
        """Test des méthodes du service d'export."""
        # Test du dossier par défaut
        default_folder = ExportService.get_default_export_folder()
        self.assertEqual(default_folder, 'exports_html')
        
        # Test de création de dossier (sans fichiers)
        test_folder = '/tmp/test_export_service'
        ExportService.create_export_directory(test_folder)
        self.assertTrue(os.path.exists(test_folder))
        
        # Nettoyer
        if os.path.exists(test_folder):
            os.rmdir(test_folder)
    
    def test_integration_with_terrain_types(self):
        """Test d'intégration avec les types de terrain."""
        builder = HtmlTemplateBuilder(2, 2)
        
        # Créer une carte avec tous les types de terrain
        carte = np.array([
            [TerrainType.TERRAIN_NU.value, TerrainType.ARBRE.value],
            [TerrainType.EAU.value, TerrainType.BRULE.value]
        ])
        
        html = builder.generate_html_carte(carte, "Test Types", "")
        
        # Vérifier que tous les symboles et couleurs sont présents
        self.assertIn('.', html)      # Terrain nu
        self.assertIn('🌲', html)     # Arbre
        self.assertIn('💧', html)     # Eau
        self.assertIn('🔥', html)     # Brûlé
        
        # Vérifier les couleurs dans la légende
        self.assertIn('#D2B48C', html)  # Beige terrain nu
        self.assertIn('#228B22', html)  # Vert arbres
        self.assertIn('#4169E1', html)  # Bleu eau
        self.assertIn('#DC143C', html)  # Rouge brûlé


if __name__ == '__main__':
    unittest.main()