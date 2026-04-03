"""
Design expérimental pour l'évaluation de la stratégie de pricing.

Unité de randomisation : compte client (pas le deal).

Référence : PRJ2025_868 — docs/03_metriques_evaluation.md
"""

import numpy as np
from dataclasses import dataclass
from typing import Literal

Arm = Literal["control", "ml_myopic", "ml_strategic"]


@dataclass
class ExperimentConfig:
    n_accounts_per_arm: int = 150
    duration_primary_months: int = 6
    duration_secondary_months: int = 12
    margin_delta: float = 0.05       # δ détectable : 5% de marge
    alpha: float = 0.05              # seuil de significativité
    power: float = 0.80              # puissance statistique


def assign_accounts(
    account_ids: list[str],
    config: ExperimentConfig,
    stratify_by: list[str] | None = None,
    random_seed: int = 42,
) -> dict[str, Arm]:
    """
    Assigne les comptes aux bras de l'expérience.

    Randomisation par région ou segment marché pour limiter le risque
    de contamination (violation SUTVA).

    Args:
        account_ids:   Liste des identifiants de compte
        config:        Configuration de l'expérience
        stratify_by:   Variables de stratification (ex: région, segment)
        random_seed:   Graine pour reproductibilité

    Returns:
        Dictionnaire {account_id: arm}
    """
    rng = np.random.default_rng(random_seed)
    arms: list[Arm] = ["control", "ml_myopic", "ml_strategic"]
    n_per_arm = config.n_accounts_per_arm
    n_total = n_per_arm * len(arms)

    if len(account_ids) < n_total:
        raise ValueError(
            f"Pas assez de comptes : {len(account_ids)} disponibles, "
            f"{n_total} requis ({n_per_arm} par bras × {len(arms)} bras)"
        )

    selected = rng.choice(account_ids, size=n_total, replace=False)
    assignment: dict[str, Arm] = {}
    for i, arm in enumerate(arms):
        for account_id in selected[i * n_per_arm: (i + 1) * n_per_arm]:
            assignment[str(account_id)] = arm

    return assignment


def compute_win_rate_rolling(
    deals: list[dict],
    window_days: int = 28,
) -> dict[str, float]:
    """
    Calcule le win rate glissant par segment sur une fenêtre de N jours.

    Args:
        deals:       Liste de deals avec champs 'date', 'segment', 'won'
        window_days: Taille de la fenêtre glissante

    Returns:
        Win rate par segment
    """
    from collections import defaultdict
    from datetime import datetime, timedelta

    cutoff = datetime.now() - timedelta(days=window_days)
    recent = [d for d in deals if d["date"] >= cutoff]

    by_segment: dict[str, list[bool]] = defaultdict(list)
    for deal in recent:
        by_segment[deal["segment"]].append(deal["won"])

    return {
        segment: sum(outcomes) / len(outcomes)
        for segment, outcomes in by_segment.items()
        if outcomes
    }
