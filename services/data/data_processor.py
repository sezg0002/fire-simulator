"""
Service de traitement des données pour le simulateur de feu de forêt.
Responsable du formatage et de la préparation des données pour l'export HTML.
"""

from typing import Dict, Any


class DataProcessor:
    """Processeur de données pour la génération de rapports HTML."""
    
    @staticmethod
    def format_statistics_description(stats: Dict[str, Any], context: str) -> str:
        """
        Formate les statistiques pour l'affichage HTML.
        
        Args:
            stats: Dictionnaire des statistiques
            context: Contexte ('original', 'sans_deboisement', 'avec_deboisement')
            
        Returns:
            String HTML formatée avec les statistiques
        """
        if context == 'original':
            return DataProcessor._format_original_stats(stats)
        elif context == 'sans_deboisement':
            return DataProcessor._format_sans_deboisement_stats(stats)
        elif context == 'avec_deboisement':
            return DataProcessor._format_avec_deboisement_stats(stats)
        else:
            return ""
    
    @staticmethod
    def _format_original_stats(stats: Dict[str, Any]) -> str:
        """Formate les statistiques de la carte originale."""
        return f"""
        <strong>Statistiques de la carte originale :</strong><br>
        • Dimension : {stats['hauteur']} × {stats['largeur']} ({stats['stats']['total']} cases)<br>
        • Arbres : {stats['stats']['arbres']} cases ({stats['stats']['arbres_pct']:.1f}%)<br>
        • Eau : {stats['stats']['eau']} cases ({stats['stats']['eau_pct']:.1f}%)<br>
        • Terrain nu : {stats['stats']['terrain_nu']} cases ({stats['stats']['terrain_nu_pct']:.1f}%)<br>
        • Position de l'incendie : {stats['position_incendie']}
        """
    
    @staticmethod
    def _format_sans_deboisement_stats(stats: Dict[str, Any]) -> str:
        """Formate les statistiques sans déboisement."""
        return f"""
        <strong>Résultats de l'incendie sans déboisement :</strong><br>
        • Position de départ : {stats['position_depart']}<br>
        • Arbres brûlés : {stats['arbres_brules']} / {stats['arbres_originaux']}<br>
        • Pourcentage brûlé : {stats['pourcentage_brule']:.1f}%
        """
    
    @staticmethod
    def _format_avec_deboisement_stats(stats: Dict[str, Any]) -> str:
        """Formate les statistiques avec déboisement."""
        return f"""
        <strong>Résultats de l'incendie avec déboisement :</strong><br>
        • Position déboisée : {stats['position_deboisement']}<br>
        • Arbres brûlés : {stats['stats_avec']['arbres_brules']} / {stats['stats_avec']['arbres_originaux']}<br>
        • Pourcentage brûlé : {stats['stats_avec']['pourcentage_brule']:.1f}%<br>
        <br>
        <strong>Efficacité du déboisement :</strong><br>
        • Arbres sauvés : {stats['comparaison']['arbres_sauves']}<br>
        • Taux de réduction : {stats['comparaison']['taux_reduction']:.1f}%
        """
    
    @staticmethod
    def prepare_export_data(donnees_simulation: Dict[str, Any], hauteur: int, largeur: int) -> Dict[str, Dict[str, Any]]:
        """
        Prépare les données de simulation pour l'export HTML.
        
        Args:
            donnees_simulation: Données de simulation complètes
            hauteur: Hauteur de la carte
            largeur: Largeur de la carte
            
        Returns:
            Dictionnaire structuré avec les données formatées pour chaque type de carte
        """
        export_data = {
            'original': {
                'carte': donnees_simulation['carte_originale'],
                'title': 'Carte Originale de la Forêt',
                'description': DataProcessor.format_statistics_description({
                    'hauteur': hauteur,
                    'largeur': largeur,
                    'stats': donnees_simulation['stats_originales'],
                    'position_incendie': donnees_simulation['position_incendie']
                }, 'original'),
                'filename': 'carte_originale.html'
            },
            'sans_deboisement': {
                'carte': donnees_simulation['carte_sans_deboisement'],
                'title': 'Carte Après Incendie (Sans Déboisement)',
                'description': DataProcessor.format_statistics_description(
                    donnees_simulation['stats_sans_deboisement'], 'sans_deboisement'
                ),
                'filename': 'carte_apres_incendie.html'
            },
            'avec_deboisement': {
                'carte': donnees_simulation['carte_avec_deboisement'],
                'title': 'Carte Après Incendie (Avec Déboisement Optimal)',
                'description': DataProcessor.format_statistics_description({
                    'position_deboisement': donnees_simulation['position_deboisement'],
                    'stats_avec': donnees_simulation['stats_avec_deboisement'],
                    'comparaison': donnees_simulation['comparaison']
                }, 'avec_deboisement'),
                'filename': 'carte_avec_deboisement.html'
            }
        }
        
        return export_data