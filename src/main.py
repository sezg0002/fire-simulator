from ForestFireSimulator import ForestFireSimulator

if __name__ == "__main__":
    
    simulateur = ForestFireSimulator(largeur=20, hauteur=20)
    
    simulateur.generer_carte_aleatoire(pourcentage_arbres=70, pourcentage_eau=5)
    
    simulateur.afficher_carte(utiliser_symboles=False)
    
    stats = simulateur.obtenir_statistiques()
    print(f"\nStatistiques de la carte:")
    print(f"- Terrain nu: {stats['terrain_nu']} cases ({stats['terrain_nu_pct']:.1f}%)")
    print(f"- Arbres: {stats['arbres']} cases ({stats['arbres_pct']:.1f}%)")
    print(f"- Eau: {stats['eau']} cases ({stats['eau_pct']:.1f}%)")
    print(f"- Total: {stats['total']} cases")
    
    
    simulateur.sauvegarder_carte("ma_foret")