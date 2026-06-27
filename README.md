# Costing Hiérarchique & Données Rares — PRJ2025_773

Comment estimer le coût de fabrication d'une variante de produit quand on n'a que 2 ou 3 commandes historiques ? Ce dépôt répond à cette question en 6 notebooks progressifs, du diagnostic au pipeline de production.

---

## Le problème

Un catalogue industriel (onduleurs, UPS) compte des centaines de variantes. Certaines sont **matures** (50+ commandes, données abondantes), d'autres sont **rares** (1-5 commandes, données insuffisantes). Pour les rares, un modèle classique par variante sur-apprend le bruit : R² = 1, mais RMSE hors-sample catastrophique.

**La solution** : exploiter la structure hiérarchique — variante ⊂ famille ⊂ gamme — pour "emprunter de la force" aux variantes bien représentées.

---

## Concepts clés

### Le biais-variance trade-off

Avec peu de données, un modèle flexible **mémorise le bruit** au lieu d'apprendre le signal. L'introduction volontaire de biais (via régularisation ou prior) réduit massivement la variance : c'est un bon échange.

| Catégorie | Risque dominant |
|-----------|----------------|
| < 6 obs (rare) | Sur-ajustement — variance explosive |
| 6-24 obs | Zone grise — compromis nécessaire |
| ≥ 25 obs (mature) | Modèle autonome viable |

### Le shrinkage

Plutôt qu'estimer le coût d'une variante rare à partir de ses seules observations, on pondère :

```
Estimé = λ × (moyenne locale) + (1 − λ) × (moyenne famille)
```

Quand les données sont rares (n petit) → λ → 0 → on s'appuie sur la famille.  
Quand les données abondent (n grand) → λ → 1 → on fait confiance aux données locales.

---

## Les 3 approches de modélisation

### A — Modèle Hiérarchique Bayésien
Le coût de chaque variante est tiré d'une distribution parente au niveau famille. Le shrinkage émerge naturellement du théorème de Bayes. **Avantage** : intervalles de confiance probabilistes, intégration facile de la connaissance experte via les priors.

### B — Mixed Effects Model *(recommandé en premier)*
Effets fixes par famille + effets aléatoires par variante. Les variantes rares ont des effets aléatoires shrinkés vers 0. **Avantage** : lisible en comité de direction, implémentation rapide avec `statsmodels`.

### C — Transfer Learning
Pré-entraînement d'un modèle global sur toutes les variantes, fine-tuning sur les variantes matures. Les variantes rares utilisent directement le modèle global (cold start). **Avantage** : scalable à l'arrivée de nouvelles variantes.

---

## Pipeline cold → warm → mature

```
Phase 0 — Cold start (0-2 obs)
  Stratégie : modèle global uniquement
  Incertitude : large (IC famille)

Phase 1 — Warm start (3-5 obs)
  Stratégie : shrinkage fort (λ ≈ 0.2)
  Incertitude : réduite par le prior

Phase 2 — Semi-mature (6-11 obs)
  Stratégie : shrinkage modéré (λ ≈ 0.5)
  Monitoring : détection du drift par rapport à la famille

Phase 3 — Mature (≥ 12 obs)
  Stratégie : fine-tuning possible (λ ≈ 0.8)
  Validation : LOO-CV fiable, modèle autonome
```

---

## Protocole de validation

Le train/test split classique est inutilisable sur 5 observations (1 point de test → IC infini).

| Niveau | Méthode | Cible |
|--------|---------|-------|
| 1 | **LOO-CV** | Toutes les variantes rares |
| 2 | **Heldout families** | Capacité de généralisation inter-famille |
| 3 | **Walk-forward** | Robustesse temporelle (inflation, évolution des prix) |

### Métriques recommandées

- **RMSE** : évaluation globale
- **Perte asymétrique** : pénalise 3× les sous-estimations (marge négative)
- **Taux de couverture** : % de commandes où le prix prédit couvre le coût réel
- **P90 erreur absolue** : surveille les erreurs extrêmes
- **Biais par famille** : détecte les dérives systématiques

---

## Structure du dépôt

```
notebooks/
├── 00_introduction_et_contexte.ipynb     # Données synthétiques, carte mentale
├── 01_diagnostic_variantes_rares.ipynb   # Biais-variance, LOO ratio, CV prédit
├── 02_mixed_effects_model.ipynb          # Approche B — statsmodels MixedLM
├── 03_hierarchical_bayesian.ipynb        # Approche A — estimateur de James-Stein
├── 04_transfer_learning.ipynb            # Approche C — cold start, fine-tuning
├── 05_validation_protocol.ipynb          # LOO-CV, métriques asymétriques
└── 06_integration_expert_et_cold_start.ipynb  # Prior expert, pipeline complet
```

---

## Démarrage rapide

```bash
pip install numpy pandas matplotlib seaborn scikit-learn statsmodels

# Démarrer par le notebook 00 — il génère les données partagées
jupyter notebook notebooks/00_introduction_et_contexte.ipynb
```

Pour PyMC (modèle bayésien complet) :
```bash
pip install pymc arviz
```

---

## Recommandation pour PRJ2025_773

1. **Court terme** — implémenter Mixed Effects (`statsmodels.MixedLM`), 1-2 semaines
2. **Moyen terme** — ajouter le modèle bayésien (PyMC) sur les familles à forte proportion de variantes rares, où le gain du shrinkage est le plus visible
3. **Long terme** — pipeline automatisé avec monitoring de phase et mise à jour online des posteriors
