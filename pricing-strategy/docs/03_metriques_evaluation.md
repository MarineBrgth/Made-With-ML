# 03 — Métriques d'évaluation stratégique

## 5 métriques complémentaires

### 1. Win rate glissant par segment (28j rolling)
Détecte une dérive avant qu'elle ne devienne structurelle.
> Alerte si win rate décile 8-10 descend sous 50%.

### 2. Prix de réouverture
Si le client revient systématiquement négocier après recommandation → le modèle **surévalue sa tolérance au prix**.

### 3. Taux de deals "fantômes" (RFQs attendues non reçues)
Proxy de réputation : comparer le nombre de RFQ reçues par compte vs historique.
> Si un client actif ne soumet plus de RFQ → signal fort avant le churn.

### 4. NPS commercial post-deal perdu
Enquête légère : *"Pourquoi avez-vous choisi un autre fournisseur ?"* — avec catégorie *"prix jugé trop élevé"*. Estime l'effet réputation.

### 5. Part de portefeuille client (share of wallet)
Pour les clients multi-fournisseurs : quelle fraction des achats dans la catégorie ?
> Si le pricing agressif réduit cette fraction, c'est visible **avant** le churn total.

---

## Design A/B test — randomisation au niveau compte

### Le piège classique
Randomiser au niveau deal → les effets long terme se diluent, le test manque de puissance.

### Design recommandé

```
Unité de randomisation : compte client (pas le deal)

Groupe A (contrôle)   : pricing règles historiques (jugement commercial)
Groupe B (traitement) : modèle ML avec objectif myope actuel
Groupe C (traitement) : modèle ML avec objectif stratégique reformulé

Métriques primaires (6 mois)  : marge cumulée / compte, win rate glissant
Métriques secondaires (12 mois): RFQs reçues / compte, CLV estimé, share of wallet

Taille : ~150 comptes par bras
         (power analysis : δ=5% marge, σ historique)
```

Voir l'implémentation : [`src/ab_test_design.py`](../src/ab_test_design.py)

### Attention au SUTVA
Si les comptes se parlent, la randomisation compte est contaminée.
> **Solution** : randomiser par région ou par segment marché isolé.

---

## Estimer l'impact sur la réputation

### Layer 1 — Observable direct
Modèle de régression :
```
P(deal_perdu_pour_prix) = f(déviation_vs_marché, taille_deal, segment)
```
Quantifie l'élasticité réputation.

### Layer 2 — Signal indirect
Comparer le **délai entre deals successifs** sur un même compte avant/après déploiement.
> Allongement du délai = réticence croissante à re-soumettre.

### Layer 3 — Modèle de diffusion
```
R(t+1) = ρ × R(t) + α × deals_gagnés(t) - β × deals_perdus_pour_prix(t)
```
Avec `ρ ∈ [0.8, 0.95]` (mémoire longue de la réputation), calibré sur données historiques.
