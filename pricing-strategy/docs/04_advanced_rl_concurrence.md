# 04 — Sujets avancés : RL & Positionnement Concurrentiel

## Intégrer la position concurrentielle

Le pricing n'est pas un problème de maximisation isolée — c'est un **jeu répété** contre des concurrents qui observent les outcomes.

### Formalisation Stackelberg (leader de marché)

```
max_{prix_i}  π_i(prix_i, prix_j*)
s.t.  prix_j* = argmax π_j(prix_j | prix_i)   ← réaction anticipée du concurrent
```

### En pratique
Enrichir les features de `P(acceptation)` avec des **proxies concurrentiels** :
- Appels d'offres publics (marchés publics)
- Win/loss analysis structurée
- Données de marché sectorielles

> Un modèle qui ignore la position relative au marché ne peut pas éviter les effets de renforcement concurrentiel sur les gros deals.

---

## Architecture Reinforcement Learning

### Formulation MDP

```
State s_t  : (features_deal, historique_compte, position_marché,
               win_rate_récent, réputation_estimée)

Action a_t : prix_recommandé ∈ [prix_min, prix_max]  (action continue)

Reward r_t : marge_immédiate × 1_{deal_gagné}
           + γ^k × CLV_increment  (récompense différée, k = délai en mois)
           - pénalité_réputation(déviation_prix)

Transition : P(s_{t+1} | s_t, a_t) — inclut évolution win rate et réputation

Algorithme : SAC (Soft Actor-Critic) pour espace d'action continu
             + reward shaping pour accélérer l'apprentissage
```

### Défi principal : horizon temporel

Le délai entre action et récompense différée est de **12-36 mois** — trop long pour un RL naïf.

| Solution | Description |
|----------|-------------|
| **Reward shaping** | Proxy immédiat de la récompense différée (ex: probabilité estimée de re-soumission) |
| **Model-based RL** | Apprendre `P(s_{t+1}|s_t, a_t)` et simuler des trajectoires longues |
| **Offline RL (CQL)** | Exploiter les données historiques avant déploiement live |

### Stratégie exploration-exploitation

> ε-greedy **par segment** :
> - Plus d'exploration sur les **petits deals** (faible coût d'erreur)
> - Exploiter la politique apprise sur les **gros deals stratégiques**

---

## Roadmap

```
Phase 1 (0-3 mois)   : Approche A — contraintes win rate, shadow mode
Phase 2 (3-6 mois)   : Approche C — modèles segmentés, A/B test
Phase 3 (6-12 mois)  : Enrichissement features concurrentielles
Phase 4 (18-24 mois) : Architecture RL, données CLV suffisantes
```
