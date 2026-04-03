# 01 — Diagnostic de l'optimisation myope

## Pourquoi `(prix - coût) × P(acceptation)` est sous-optimal

L'objectif maximise la marge espérée **par deal isolé**, sans considérer que chaque deal est un nœud dans un graphe de relations commerciales.

## Trois biais structurels

### 1. Biais de stationnarité
Le modèle suppose que `P(acceptation)` est stable, alors que les prix recommandés **aujourd'hui modifient la distribution future**.

> Un client qui perd 3 appels d'offres de suite à des prix jugés excessifs ne remet plus de RFQ — `P(acceptation)` futur → 0, sans signal dans les données.

### 2. Biais de scope
Optimiser deal par deal ignore les **externalités inter-deals**.

> Le décile 10 illustre exactement ça : +22% de prix sur les gros deals, c'est un signal fort envoyé au marché ("Socomec est cher sur les grands projets"), avec des effets de réputation diffus mais durables.

### 3. Biais de sélection (survivorship bias silencieux)
Le modèle a été entraîné sur des deals historiquement soumis. Si le pricing agressif fait que les prospects ne soumettent plus de RFQ, ce biais **disparaît des données**.

## Effets stratégiques ignorés

| Effet | Mécanisme | Horizon |
|-------|-----------|--------|
| **CLV érosion** | Client mécontent → churn, moins d'upsell | 12-36 mois |
| **Réputation marché** | Deals perdus à prix élevé → bouche-à-oreille négatif | 6-24 mois |
| **Renforcement concurrentiel** | On cède les gros deals → concurrents montent en référence | 18-36 mois |
| **Ancrage prix** | Prix historique devient référence pour futures négos | Permanent |
| **Concentration portefeuille** | Décile 1 sur-accepté → saturation capacité sur petits deals | Court terme |

## Formalisation de la CLV

```
CLV(client_i) = Σ_{t=1}^{T} [ E(marge_t | client_i) × P(actif_t | actif_{t-1}) ] / (1+r)^t
              + P(upsell) × marge_upsell
              - coût_acquisition × 1_{t=0}
```

Voir l'implémentation : [`src/deal_value.py`](../src/deal_value.py)
