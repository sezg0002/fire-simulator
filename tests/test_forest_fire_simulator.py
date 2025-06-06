import unittest
import numpy as np
import os

from src.TerrainType import TerrainType
from src.ForestFireSimulator import ForestFireSimulator

class TestForestFireSimulator(unittest.TestCase):
    def setUp(self):
        self.largeur = 10
        self.hauteur = 10
        self.sim = ForestFireSimulator(largeur=self.largeur, hauteur=self.hauteur)

    def test_init(self):
        self.assertEqual(self.sim.largeur, self.largeur)
        self.assertEqual(self.sim.hauteur, self.hauteur)
        self.assertEqual(self.sim.carte.shape, (self.hauteur, self.largeur))
        self.assertTrue(np.all(self.sim.carte == TerrainType.TERRAIN_NU.value))

    def test_generer_carte_aleatoire(self):
        self.sim.generer_carte_aleatoire(pourcentage_arbres=60, pourcentage_eau=10)
        total_cases = self.largeur * self.hauteur
        nb_arbres = np.sum(self.sim.carte == TerrainType.ARBRE.value)
        nb_eau = np.sum(self.sim.carte == TerrainType.EAU.value)
        nb_nu = np.sum(self.sim.carte == TerrainType.TERRAIN_NU.value)
        self.assertAlmostEqual(nb_arbres, int(total_cases * 0.6), delta=2)
        self.assertAlmostEqual(nb_eau, int(total_cases * 0.1), delta=2)
        self.assertEqual(nb_arbres + nb_eau + nb_nu, total_cases)

        # Test pourcentage > 100
        with self.assertRaises(ValueError):
            self.sim.generer_carte_aleatoire(90, 20)

    def test_obtenir_statistiques(self):
        self.sim.generer_carte_aleatoire(50, 20)
        stats = self.sim.obtenir_statistiques()
        self.assertIn('arbres', stats)
        self.assertIn('eau', stats)
        self.assertIn('terrain_nu', stats)
        self.assertIn('arbres_pct', stats)
        self.assertIn('eau_pct', stats)
        self.assertIn('terrain_nu_pct', stats)
        self.assertAlmostEqual(stats['total'], self.largeur * self.hauteur)
        self.assertAlmostEqual(stats['arbres'] + stats['eau'] + stats['terrain_nu'], stats['total'])

    def test_sauvegarder_et_charger_carte(self):
        self.sim.generer_carte_aleatoire(20, 5)
        test_filename = "test_foret"
        self.sim.sauvegarder_carte(test_filename)
        self.assertTrue(os.path.exists(test_filename + ".npy"))
        # Changement de carte pour vérifier le chargement
        self.sim.carte.fill(TerrainType.TERRAIN_NU.value)
        self.sim.charger_carte(test_filename + ".npy")
        unique_values = np.unique(self.sim.carte)
        self.assertTrue(any(unique_values == TerrainType.ARBRE.value))
        self.assertTrue(
            any(unique_values == TerrainType.EAU.value) or any(unique_values == TerrainType.TERRAIN_NU.value))
        os.remove(test_filename + ".npy")  # Nettoyage


if __name__ == '__main__':
    unittest.main()