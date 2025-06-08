from ForestFireSimulator import ForestFireSimulator

if __name__ == "__main__":
    print("🌲 SIMULATEUR DE FEUX DE FORÊT 🔥")
    print("=" * 50)

    simulateur = ForestFireSimulator(largeur=30, hauteur=15)

    print(" Génération de la carte aléatoire...")
    simulateur.generer_carte_aleatoire(pourcentage_arbres=65, pourcentage_eau=10)

    print("\n DÉMARRAGE DE LA SIMULATION COMPLÈTE AVEC DÉBOISEMENT OPTIMAL")
    print("-" * 60)

    donnees_simulation = simulateur.simulation_complete_avec_deboisement()

    print("\n" + "=" * 60)
    print(" GÉNÉRATION DES EXPORTS HTML")
    print("=" * 60)

    simulateur.exporter_html()

    print("\n Simulation terminée avec succès!")
    print("Consultez le dossier 'exports_html' pour voir les visualisations.")