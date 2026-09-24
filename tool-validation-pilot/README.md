> 12 hand-built vulnerable/fixed model pairs, one per check family, used to
> sanity-check the tool's mechanics. Separate from the 7 real-system results
> in `../RESULTS.md` and `../FINDINGS.md`. Run all 12 from the evaluation
> folder root with `python3 scripts/reproduce.py <path-to-jar>`; `run.sh`
> below is the original script and assumes it runs from inside the sam4c-cli
> repo, kept for reference only.

### Disponibilité (CWE-400)
Un service critique déclaré en haute disponibilité ne tourne qu'en un seul exemplaire, sans
répartition sur les zones. Une panne d'instance ou de zone le rend indisponible.

### Isolation (CWE-668)
Deux composants qu'une règle exige isolés (par exemple un frontend et une base de données sensible)
partagent le même connecteur : un chemin réseau existe entre eux, l'isolation est violée.

### Authentification manquante (CWE-306)
Un service est exposé à l'extérieur sans qu'aucune règle d'authentification ne le protège : point
d'entrée non authentifié.

### Exposed data (CWE-200 / 668)
Un magasin de données avec état (base de données) est directement exposé à la sphère externe, alors
qu'il ne devrait jamais l'être.

### Exposition contradiction (CWE-668)
Un composant déclaré interne est câblé à un connecteur marqué externe : son exposition réelle
contredit son exposition déclarée.

### Autorisation sans authentification (CWE-862)
Une règle d'autorisation accorde l'accès à une ressource qu'aucune règle d'authentification ne
protège : on autorise sans jamais authentifier.

### isolation contradictoire
La politique déclare à la fois une isolation et une exigence de communication (confidentialité)
entre les deux mêmes composants : on ne peut pas communiquer avec un composant dont on exige
l'isolation.
