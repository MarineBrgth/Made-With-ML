# Pricing Strategy — PRJ2025_868

> **Au-delà de l'optimisation myope : vers une stratégie de pricing B2B orientée valeur relationnelle**

## Problème central

L'objectif classique `max (prix - coût) × P(acceptation)` maximise la **marge espérée par deal isolé**. Ce faisant, il ignore que chaque deal est un nœud dans un graphe de relations commerciales — avec des effets de réputation, de fidélisation et de positionnement concurrentiel.

## Structure du dépôt

```
pricing-strategy/
├── README.md                          ← Ce fichier
├── docs/
│   ├── 01_diagnostic_myopie.md        ← Biais structurels du modèle actuel
│   ├── 02_reformulation_objectif.md   ← Approches A / B / C
│   ├── 03_metriques_evaluation.md     ← 5 métriques + design A/B test
│   └── 04_advanced_rl_concurrence.md  ← RL + game theory Stackelberg
└── src/
    ├── deal_value.py                  ← CLV + valeur stratégique d'un deal
    ├── penalty_functions.py           ← Fonctions de pénalisation φ
    └── ab_test_design.py              ← Design expérimental randomisé
```

## Synthèse pour décideurs

| Horizon | Recommandation | Risque |
|---------|---------------|--------|
| **Immédiat** | Approche A : contrainte de win rate par segment (τ_min) | Faible — auditabilité totale |
| **3-6 mois** | Approche C : modèles segmentés (maturité × taille deal) | Moyen — nécessite données de récurrence |
| **18-24 mois** | Architecture RL avec récompenses différées (CLV) | Élevé — dépend de la qualité des données |

> Le modèle actuel est **mathématiquement correct sur sa question** — mais la question est mal posée.
> Il optimise la marge du deal, pas la valeur de la relation.

## Références

- [01 — Diagnostic de l'optimisation myope](docs/01_diagnostic_myopie.md)
- [02 — Reformulation de l'objectif](docs/02_reformulation_objectif.md)
- [03 — Métriques d'évaluation stratégique](docs/03_metriques_evaluation.md)
- [04 — Sujets avancés : RL & concurrence](docs/04_advanced_rl_concurrence.md)
