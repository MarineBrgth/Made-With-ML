"""
Valeur stratégique d'un deal = marge immédiate + option value future (CLV).

Référence : PRJ2025_868 — docs/01_diagnostic_myopie.md
"""

from typing import Literal

ClientSegment = Literal["nouveau_client", "client_actif", "client_at_risk", "one_shot"]

# Incréments CLV estimés par segment (à calibrer sur données historiques)
# via modèle de survie client (Weibull ou Cox)
CLV_INCREMENTS: dict[ClientSegment, float] = {
    "nouveau_client": 15_000,   # acquisition → pipeline futur
    "client_actif": 8_000,      # fidélisation → renouvellement
    "client_at_risk": 25_000,   # rétention critique
    "one_shot": 0,              # pas de récurrence attendue
}


def deal_value(
    prix: float,
    cout: float,
    p_accept: float,
    client_segment: ClientSegment,
) -> float:
    """
    Valeur totale d'un deal intégrant la marge immédiate et l'incrément CLV.

    Args:
        prix:           Prix recommandé
        cout:           Coût du deal
        p_accept:       P(acceptation | prix, features) — sortie du modèle ML
        client_segment: Segment du client

    Returns:
        Valeur stratégique du deal (marge immédiate + CLV pondéré)
    """
    margin_immediate = (prix - cout) * p_accept
    clv_increment = CLV_INCREMENTS[client_segment] * p_accept
    return margin_immediate + clv_increment


def optimize_price(
    cout: float,
    p_accept_fn,  # callable(prix) -> float
    client_segment: ClientSegment,
    prix_min: float,
    prix_max: float,
    n_grid: int = 500,
) -> float:
    """
    Grid search 1D pour trouver le prix maximisant la valeur stratégique.

    Args:
        cout:           Coût du deal
        p_accept_fn:    Fonction prix -> P(acceptation), issue du modèle ML
        client_segment: Segment du client
        prix_min:       Borne inférieure du prix
        prix_max:       Borne supérieure du prix
        n_grid:         Résolution de la grille

    Returns:
        Prix optimal
    """
    import numpy as np

    grid = np.linspace(prix_min, prix_max, n_grid)
    values = [
        deal_value(p, cout, p_accept_fn(p), client_segment)
        for p in grid
    ]
    return float(grid[int(np.argmax(values))])
