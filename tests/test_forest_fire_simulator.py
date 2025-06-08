import unittest
import numpy as np
import os
import io
from unittest.mock import patch
from src.ForestFireSimulator import ForestFireSimulator, TerrainType

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

    def test_simuler_incendie_centre(self):
        self.sim.carte.fill(TerrainType.ARBRE.value)
        stats = self.sim.simuler_incendie(self.hauteur // 2, self.largeur // 2)
        self.assertEqual(stats['arbres_brules'], self.largeur * self.hauteur)
        self.assertAlmostEqual(stats['pourcentage_brule'], 100.0)
        self.assertEqual(stats['arbres_originaux'], self.largeur * self.hauteur)

    def test_simuler_incendie_coin(self):
        self.sim.carte.fill(TerrainType.TERRAIN_NU.value)
        self.sim.carte[0, 0] = TerrainType.ARBRE.value
        self.sim.carte[0, 1] = TerrainType.ARBRE.value
        self.sim.carte[1, 0] = TerrainType.EAU.value
        stats = self.sim.simuler_incendie(0, 0)
        self.assertEqual(stats['arbres_brules'], 2)
        self.assertEqual(stats['arbres_originaux'], 2)
        self.assertAlmostEqual(stats['pourcentage_brule'], 100.0)

    def test_simuler_incendie_aucun_arbre(self):
        self.sim.carte.fill(TerrainType.TERRAIN_NU.value)
        stats = self.sim.simuler_incendie(0, 0)
        self.assertEqual(stats['arbres_brules'], 0)
        self.assertEqual(stats['arbres_originaux'], 0)
        self.assertEqual(stats['pourcentage_brule'], 0.0)
        self.assertIsNone(stats['position_depart'])

    def test_simuler_incendie_case_non_arbre(self):
        self.sim.carte.fill(TerrainType.TERRAIN_NU.value)
        self.sim.carte[3, 3] = TerrainType.EAU.value
        stats = self.sim.simuler_incendie(3, 3)
        self.assertEqual(stats['arbres_brules'], 0)
        self.assertEqual(stats['arbres_originaux'], 0)
        self.assertEqual(stats['pourcentage_brule'], 0.0)

    def test_simuler_incendie_fragmentation(self):
        self.sim.carte.fill(TerrainType.EAU.value)
        self.sim.carte[0, 0] = TerrainType.ARBRE.value
        self.sim.carte[0, 1] = TerrainType.ARBRE.value
        self.sim.carte[9, 9] = TerrainType.ARBRE.value
        stats = self.sim.simuler_incendie(0, 0)
        self.assertEqual(stats['arbres_brules'], 2)
        self.assertEqual(stats['arbres_originaux'], 3)
        self.assertAlmostEqual(stats['pourcentage_brule'], 2 / 3 * 100, delta=1)

    def test_obtenir_voisins_centre(self):
        voisins = self.sim.obtenir_voisins(5, 5)
        self.assertEqual(len(voisins), 8)
        self.assertIn((4, 4), voisins)
        self.assertIn((6, 6), voisins)

    def test_obtenir_voisins_coin(self):
        voisins = self.sim.obtenir_voisins(0, 0)
        self.assertEqual(len(voisins), 3)
        self.assertIn((0, 1), voisins)
        self.assertIn((1, 0), voisins)
        self.assertIn((1, 1), voisins)

    def test_obtenir_voisins_bord(self):
        voisins = self.sim.obtenir_voisins(0, 5)
        self.assertEqual(len(voisins), 5)

    def test_generer_carte_aleatoire_extreme(self):
        self.sim.generer_carte_aleatoire(100, 0)
        self.assertTrue(np.all(self.sim.carte == TerrainType.ARBRE.value))
        self.sim.generer_carte_aleatoire(0, 100)
        self.assertTrue(np.all(self.sim.carte == TerrainType.EAU.value))
        self.sim.generer_carte_aleatoire(0, 0)
        self.assertTrue(np.all(self.sim.carte == TerrainType.TERRAIN_NU.value))

    def test_console_output(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.sim.generer_carte_aleatoire(50, 20)
            output = fake_out.getvalue()
        self.assertIn("Carte générée", output)

    def test_console_output_simuler_incendie(self):
        self.sim.carte.fill(TerrainType.ARBRE.value)
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.sim.simuler_incendie(0, 0)
            output = fake_out.getvalue()
        self.assertIn("🔥 Démarrage de l'incendie", output)
        self.assertIn("Incendie simulé", output)

    def test_trouver_meilleure_case_a_deboiser(self):
        self.sim.carte.fill(TerrainType.ARBRE.value)
        result = self.sim.trouver_meilleure_case_a_deboiser(5, 5)
        self.assertIn("position_deboisement", result)
        self.assertIn("arbres_sauves", result)
        self.assertIn("pourcentage_reduction", result)
        self.assertTrue(result["arbres_sauves"] >= 0)
        self.assertTrue(result["pourcentage_reduction"] >= 0)

    def test_trouver_meilleure_case_a_deboiser_statistiques_coherentes(self):
        self.sim.carte.fill(TerrainType.ARBRE.value)
        result = self.sim.trouver_meilleure_case_a_deboiser(2, 2)
        self.assertLessEqual(result["arbres_brules_avec_deboisement"], result["arbres_brules_sans_deboisement"])
        self.assertGreaterEqual(result["pourcentage_reduction"], 0)

    def test_simulation_complete_avec_deboisement_integration(self):
        self.sim.generer_carte_aleatoire(pourcentage_arbres=70, pourcentage_eau=10)
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.sim.simulation_complete_avec_deboisement()
            output = fake_out.getvalue()
        self.assertIn("CARTE ORIGINALE", output)
        self.assertIn("Résultats de l'incendie avec déboisement", output)
        self.assertIn("Arbres brûlés", output)

    def test_afficher_carte_variantes(self):
        self.sim.carte.fill(TerrainType.ARBRE.value)
        for use_symbols in [True, False]:
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                self.sim.afficher_carte(utiliser_symboles=use_symbols, afficher_incendie=False)
                output = fake_out.getvalue()
            self.assertTrue(output.strip() != "")
        self.sim.carte[1, 1] = TerrainType.BRULE.value
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.sim.afficher_carte(utiliser_symboles=True, afficher_incendie=True)
            output = fake_out.getvalue()
        self.assertTrue("🔥" in output or "*" in output)

    def test_exporter_html(self):
        self.sim.generer_carte_aleatoire(60, 10)
        self.sim.simulation_complete_avec_deboisement()
        dossier_sortie = "test_exports_html"
        self.sim.exporter_html(dossier_sortie=dossier_sortie)
        fichiers_attendus = [
            "carte_originale.html",
            "carte_apres_incendie.html",
            "carte_avec_deboisement.html"
        ]
        for nom in fichiers_attendus:
            chemin = os.path.join(dossier_sortie, nom)
            self.assertTrue(os.path.exists(chemin))
            os.remove(chemin)
        os.rmdir(dossier_sortie)

    def test_integration_complete(self):
        self.sim.generer_carte_aleatoire(pourcentage_arbres=50, pourcentage_eau=10)
        stats_avant = self.sim.obtenir_statistiques()
        total_cases = self.sim.largeur * self.sim.hauteur

        self.sim.simulation_complete_avec_deboisement()
        donnees = self.sim.donnees_simulation

        self.assertIn('carte_originale', donnees)
        self.assertIn('carte_sans_deboisement', donnees)
        self.assertIn('carte_avec_deboisement', donnees)
        self.assertIn('resultats_deboisement', donnees)
        self.assertIn('stats_sans_deboisement', donnees)
        self.assertIn('stats_avec_deboisement', donnees)
        self.assertIn('comparaison', donnees)

        stats_sans = donnees['stats_sans_deboisement']
        stats_avec = donnees['stats_avec_deboisement']
        comp = donnees['comparaison']

        self.assertLessEqual(stats_avec['arbres_brules'], stats_sans['arbres_brules'])

        self.assertEqual(stats_avec['arbres_originaux'], stats_sans['arbres_originaux'] - 1)

        self.assertEqual(comp['arbres_sauves'], stats_sans['arbres_brules'] - stats_avec['arbres_brules'])

        dossier_sortie = "test_exports_html_integration"
        self.sim.exporter_html(dossier_sortie=dossier_sortie)
        fichiers_attendus = [
            "carte_originale.html",
            "carte_apres_incendie.html",
            "carte_avec_deboisement.html"
        ]
        for nom in fichiers_attendus:
            chemin = os.path.join(dossier_sortie, nom)
            self.assertTrue(os.path.exists(chemin))
            os.remove(chemin)
        os.rmdir(dossier_sortie)

if __name__ == '__main__':
    unittest.main()