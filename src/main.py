from ForestFireSimulator import ForestFireSimulator

if __name__ == "__main__":

    simulateur = ForestFireSimulator(largeur=20, hauteur=10)
    
    simulateur.generer_carte_aleatoire(pourcentage_arbres=50, pourcentage_eau=30)
    
    print("=== CARTE ORIGINALE ===")
    simulateur.afficher_carte(utiliser_symboles=True)
    
    stats_orig = simulateur.obtenir_statistiques()
    print(f"\nStatistiques originales:")
    print(f"- Terrain nu: {stats_orig['terrain_nu']} cases ({stats_orig['terrain_nu_pct']:.1f}%)")
    print(f"- Arbres: {stats_orig['arbres']} cases ({stats_orig['arbres_pct']:.1f}%)")
    print(f"- Eau: {stats_orig['eau']} cases ({stats_orig['eau_pct']:.1f}%)")
    
    
    # Simuler un incendie au centre de la carte 
    ligne_centre = simulateur.hauteur // 2
    colonne_centre = simulateur.largeur // 2
    
    print(f"\n=== SIMULATION D'INCENDIE ===")
    print(f"Tentative de déclenchement à la position ({ligne_centre}, {colonne_centre})")
    
    stats_incendie = simulateur.simuler_incendie(ligne_centre, colonne_centre)
    
    print("\n=== CARTE APRÈS INCENDIE (instantané) ===")
    simulateur.afficher_carte(utiliser_symboles=True, afficher_incendie=True)
    
    print(f"\nRésultats de l'incendie:")
    print(f"- Position de départ: {stats_incendie.get('position_depart', 'Non définie')}")
    print(f"- Arbres brûlés: {stats_incendie.get('arbres_brules', 0)}")
    print(f"- Arbres originaux: {stats_incendie.get('arbres_originaux', 0)}")
    print(f"- Pourcentage brûlé: {stats_incendie.get('pourcentage_brule', 0):.1f}%")
    
    # # Test de simulation instantanée
    # print(f"\n=== NOUVELLE CARTE POUR TEST ===")
    # print("Génération d'une nouvelle carte pour la démo...")
    # simulateur.generer_carte_aleatoire(pourcentage_arbres=60, pourcentage_eau=20)
    # simulateur.afficher_carte(utiliser_symboles=True)
    
    # # Simuler incendie et afficher résultat
    # stats_test = simulateur.simuler_incendie(simulateur.hauteur//2, simulateur.largeur//2)
    # print(f"\n=== CARTE APRÈS INCENDIE ===")
    # simulateur.afficher_carte(utiliser_symboles=True, afficher_incendie=True)
    
    # # Test avec différentes configurations
    # print(f"\n=== TESTS AVEC DIFFÉRENTES CONFIGURATIONS ===")
    
    # # Carte avec beaucoup d'eau (fragmentation)
    # print("\n1. Carte avec beaucoup d'eau (30%):")
    # simulateur.generer_carte_aleatoire(pourcentage_arbres=50, pourcentage_eau=30)
    # stats1 = simulateur.simuler_incendie(simulateur.hauteur//2, simulateur.largeur//2)
    # print(f"   Résultat: {stats1['arbres_brules']}/{stats1['arbres_originaux']} arbres brûlés ({stats1['pourcentage_brule']:.1f}%)")
    
    # # Carte très dense en arbres
    # print("\n2. Carte très dense (90% d'arbres, 5% d'eau):")
    # simulateur.generer_carte_aleatoire(pourcentage_arbres=90, pourcentage_eau=5)
    # stats2 = simulateur.simuler_incendie(0, 0)  # Coin
    # print(f"   Résultat: {stats2['arbres_brules']}/{stats2['arbres_originaux']} arbres brûlés ({stats2['pourcentage_brule']:.1f}%)")
    
    # # Carte clairsemée
    # print("\n3. Carte clairsemée (30% d'arbres, 10% d'eau):")
    # simulateur.generer_carte_aleatoire(pourcentage_arbres=30, pourcentage_eau=10)
    # stats3 = simulateur.simuler_incendie(simulateur.hauteur//2, simulateur.largeur//2)
    # print(f"   Résultat: {stats3['arbres_brules']}/{stats3['arbres_originaux']} arbres brûlés ({stats3['pourcentage_brule']:.1f}%)")