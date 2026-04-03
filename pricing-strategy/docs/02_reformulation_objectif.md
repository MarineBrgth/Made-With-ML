# 02 — Reformulation de l'objectif

## Approche A — Multi-objectifs avec contraintes

### Formulation

```
max_{prix}  (prix - coût) × P(acceptation | prix, features)

s.t.  P(acceptation | prix, features) ≥ τ_min(segment)
      prix ∈ [prix_plancher, prix_plafond]
      |prix - prix_historique| / prix_historique ≤ δ_max
```

### Calibration de τ_min par segment

| Segment | τ_min | Logique |
|---------|-------|--------|
| Nouveau client | 0.55 | Accepter plus de risque pour acquisition |
| Client stratégique | 0.70 | Protéger la relation |
| One-shot | 0.40 | Maximiser marge pure |

**Résolution** : grid search 1D sur `[prix_plancher, prix_plafond]` avec vérification des contraintes — trivial à implémenter, facile à auditer.

**Calibration de τ_min** : via frontière Pareto empirique — tracer marge espérée vs taux acceptation en faisant varier τ, identifier le coude de la courbe.

---

## Approche B — Pénalisation des déviations extrêmes

### Formulation

```
max_{prix}  (prix - coût) × P(acceptation | prix)
            - λ × φ(prix, prix_historique)
```

Voir les implémentations de φ : [`src/penalty_functions.py`](../src/penalty_functions.py)

### Calibration de λ — une conversation business déguisée

λ n'est pas un hyperparamètre technique — c'est un **paramètre de préférence stratégique** :

1. Fixer une grille `λ ∈ {0, 0.1, 0.5, 1, 2, 5, 10}`
2. Pour chaque λ, simuler les recommandations sur le hold-out historique
3. Tracer la frontière Pareto : (marge espérée, déviation moyenne vs historique)
4. Présenter la courbe au Directeur Commercial → il choisit le point acceptable
5. Back-calculer λ correspondant

---

## Approche C — Optimisation segmentée

### Matrice segment × objectif

| Segment | Objectif principal | Contrainte secondaire |
|---------|-------------------|----------------------|
| Nouveau / Grand | Acquisition stratégique | Prix ≤ prix_marché + 5% |
| Nouveau / Petit | Qualification rapide | Marge ≥ seuil_rentabilité |
| Actif / Grand | Défense part de marché | Taux acceptation ≥ 70% |
| Actif / Petit | Rentabilité | Libre (relation protégée) |
| At-risk / * | Rétention absolue | Prix = prix_historique ± 3% |

### Implémentation
- Un modèle `P(acceptation)` par segment (les élasticités-prix sont structurellement différentes)
- Routing vers le bon modèle **avant** l'optimisation
- **Validation** : shadow mode 3 mois avant déploiement
