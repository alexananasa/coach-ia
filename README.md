# Coach IA

Un coach de musculation personnel inspiré du dépôt `site_muscu_louis`, limité au programme de force, à son journal, à la progression des charges et à un tableau de bord statique.

## Ce que contient ce projet

- Quatre séances par semaine : Bas, Haut A, Haut B et Haut C.
- Un cycle de quatre semaines : trois semaines de progression, puis une semaine de décharge.
- Des charges de départ calculées à partir des maxima enregistrés, du RIR et du matériel réellement disponible.
- Une progression qui ne monte qu’après un cycle réussi. Les petites poulies et les machines à crans suivent leurs incréments propres.
- Un journal prérempli pour éviter de retaper les dates, séances et exercices.
- Un tableau de bord généré chaque jour par GitHub Actions, sans serveur ni service externe.
- Des graphiques de volume musculaire, de progression par exercice et de régularité.
- Un historique des charges basé uniquement sur les répétitions vraiment saisies.

**Ce dépôt ne contient pas la partie course, Garmin, nutrition ou collecte de données du projet d’origine.** Le programme de musculation reste déterministe : aucun modèle d’IA ne décide des séances ou des charges.

## Tableau de bord

Le fichier généré est `docs/index.html`. Pour le produire sur ton ordinateur :

```bash
python generate_dashboard.py
```

Ouvre ensuite `docs/index.html` dans un navigateur. Le workflow GitHub régénère le tableau de bord chaque jour et après les changements de programme ou de journal. Si GitHub Pages est activé pour ce dépôt, le même workflow publie ensuite `docs/` à l’adresse `https://alexananasa.github.io/coach-ia/`.

## Graphiques musculation

- **Volume par muscle** : séries prévues dans la semaine, avec le détail des sept groupes musculaires et leur variation sur les quatre semaines du cycle.
- **Progression des charges** : un graphique par exercice, projeté sur six cycles. Les paliers respectent les incréments de barre, haltères, poulies, machines et lest ; les semaines de décharge sont marquées en orange.
- **Régularité** : calendrier des séances prévues sur douze semaines. Une absence déclarée est exclue du taux ; une séance passée sans saisie suit la règle du journal et compte comme réussie.
- **Historique des charges** : les courbes apparaissent après deux séances datées avec répétitions saisies. Elles montrent les charges enregistrées, sans reconstruire de performances passées.

Les séries de sommeil, fréquence cardiaque, calories, VO2max, course et Garmin du dépôt source ne sont pas reprises. Il n’y a pas de données historiques de musculation disponibles dans ce dépôt ; les graphiques d’historique se rempliront au fil des séances consignées.

## Saisir une séance

Le journal est `data/seances.json`. Les séances sont ajoutées automatiquement par le générateur :

- Laisse `"reps": []` si tu as atteint les répétitions prescrites sur toutes les séries.
- Si tu es resté en dessous, saisis les répétitions réellement faites, par exemple `"reps": [8, 7, 5]`.
- Marque une séance non faite avec `"absent": true`. Sinon, l’absence de saisie signifie « séance réussie ».
- `"charge"` est facultatif : renseigne-la seulement si tu as réellement utilisé une charge différente de celle prescrite.
- Renseigne `"charge"` en kg si tu veux conserver une charge réellement utilisée. L’historique affichera la charge notée, pas une estimation Garmin.

Tu peux modifier le fichier depuis GitHub avec le bouton **Modifier mon journal** du tableau de bord. L’automatisation republie ensuite la page.

## Personnaliser le programme

`programme_muscu.md` est la source de vérité. Les blocs Python qu’il contient sont lus de façon sûre avec `ast.literal_eval`, jamais exécutés. Modifie les séances, les maxima, les machines ou les consignes techniques dans ce document. Les noms d’exercices doivent rester identiques entre `PROGRAMME`, `MAXES`, `MACHINES` et `TECHNIQUE`.

Le poids de corps et le début du cycle se règlent dans `data/settings.json`. Le cycle commence le lundi indiqué par `cycle_anchor`.

## Règle de progression

Le poids reste stable pendant le cycle. Les répétitions prescrites montent progressivement dans la fourchette. À la fin d’un cycle complet, chaque exercice reçoit un crédit si aucune série de cet exercice n’a été déclarée sous la prescription et si les séances prévues n’ont pas été marquées absentes.

Un crédit ouvre un incrément du matériel. Si cet incrément est trop grand en proportion de la charge, le code attend plusieurs cycles, dans la limite définie. La semaine 4 réduit le nombre de séries de 40 % et ramène les répétitions au bas de la fourchette.

La charge initiale est une estimation à partir du 1RM déclaré, via une formule Epley, puis arrondie au matériel disponible. Ajuste le maximum dans `programme_muscu.md` si la charge affichée ne correspond pas à ton niveau actuel. Le programme d’origine utilisait une table RPE qui n’est pas présente dans le dépôt GitHub ; cette version rend le calcul explicite et autonome.

## Confidentialité

Le dépôt GitHub et le site sont publics. Le dépôt contient des maxima de force, des réglages de salle, un poids de corps et le journal des séances ; le tableau de bord affiche ces données. Le site est déployé avec GitHub Pages via GitHub Actions. Ce projet n’appelle ni Garmin, ni Gemini, ni Firebase.

La répartition jambes/haut du corps a été reprise telle quelle du programme source. Dans ce programme, le faible volume jambes était en partie justifié par un entraînement de course qui n’est pas géré ici ; fais réévaluer cette répartition si tu veux un programme entièrement indépendant de la course.

Ce tableau de bord organise un entraînement et ne remplace pas l’avis d’un professionnel de santé. En cas de douleur persistante, arrête l’exercice concerné et demande conseil à un professionnel.

