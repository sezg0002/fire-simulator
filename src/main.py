from ForestFireSimulator import ForestFireSimulator

if __name__ == "__main__":
    simulateur = ForestFireSimulator(largeur=30, hauteur=15)
    
    simulateur.generer_carte_aleatoire(pourcentage_arbres=65, pourcentage_eau=10)
    
    print("DÉMARRAGE DE LA SIMULATION AVEC DÉBOISEMENT OPTIMAL")
    simulateur.simulation_complete_avec_deboisement()