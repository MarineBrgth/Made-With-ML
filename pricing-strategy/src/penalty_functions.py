"""
Fonctions de pénalisation φ pour l'Approche B.

max_{prix}  (prix - coût) × P(acceptation | prix)
            - λ × φ(prix, prix_historique)

Référence : PRJ2025_868 — docs/02_reformulation_objectif.md
"""


def phi_linear(prix: float, prix_hist: float) -> float:
    """Pénalité linéaire symétrique."""
    return abs(prix - prix_hist) / prix_hist


def phi_quadratic(prix: float, prix_hist: float) -> float:
    """Pénalité quadratique — plus douce près de l'historique."""
    return ((prix - prix_hist) / prix_hist) ** 2


def phi_asymmetric(
    prix: float,
    prix_hist: float,
    alpha: float = 2.0,
    beta: float = 0.5,
) -> float:
    """
    Pénalité asymétrique — pénalise davantage les hausses que les baisses.

    Args:
        alpha: Poids des hausses de prix (alpha >> beta recommandé)
        beta:  Poids des baisses de prix
    """
    deviation = (prix - prix_hist) / prix_hist
    hausse = max(0.0, deviation) * alpha
    baisse = max(0.0, -deviation) * beta
    return hausse + baisse


def penalized_objective(
    prix: float,
    cout: float,
    p_accept: float,
    prix_hist: float,
    lambda_: float,
    phi_fn=phi_asymmetric,
) -> float:
    """
    Objectif pénalisé complet.

    Args:
        prix:      Prix candidat
        cout:      Coût du deal
        p_accept:  P(acceptation | prix)
        prix_hist: Prix de référence historique
        lambda_:   Paramètre de préférence stratégique (calibré métier)
        phi_fn:    Fonction de pénalisation choisie

    Returns:
        Valeur de l'objectif pénalisé
    """
    marge_esperee = (prix - cout) * p_accept
    penalite = lambda_ * phi_fn(prix, prix_hist)
    return marge_esperee - penalite
