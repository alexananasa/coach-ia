# Coach Muscu Perso — programme source

Ce document est la source de vérité du programme. Le tableau de bord lit les blocs Python avec `ast.literal_eval` ; il ne lance pas le code contenu ici.

## Organisation

Quatre séances hebdomadaires, conservées depuis le programme d’origine :

- **Lundi — Bas**
- **Mardi — Haut A**
- **Jeudi — Haut B**
- **Samedi — Haut C**

Les autres jours sont des jours sans séance prescrite par cet outil. La répartition est reprise telle quelle. Dans le projet d’origine, le volume jambes avait été choisi dans un contexte qui comprenait aussi de la course ; ce nouveau projet ne suit pas cette activité et ne réévalue donc pas ce choix.

## Progression

- Trois semaines de développement, avec le RIR qui passe de 3 à 1.
- La quatrième semaine réduit le nombre de séries de 40 % et ramène les répétitions au bas de la fourchette.
- La charge reste stable pendant le cycle. Les répétitions montent d’abord ; un cycle réussi peut ensuite ouvrir le prochain petit palier que le matériel permet.
- Le journal est prérempli. Laisser `reps` vide signifie « séance faite comme prescrit ». Saisir les répétitions seulement si elles sont inférieures à la prescription. Une absence se marque avec `"absent": true`.

## Blocs lus par le tableau de bord

### Programme hebdomadaire

```python
PROGRAMME = {
    "lundi": {
        "nom": "Bas",
        "type": "force_bas",
        "exercices": [
            {"nom": "Squat barre haute",        "materiel": "barre",    "series": 3, "reps": (6, 8), "repos": "3-5 min"},
            {"nom": "Soulevé de terre roumain", "materiel": "barre",    "series": 3, "reps": (8, 10), "repos": "3 min"},
            {"nom": "Squat bulgare",            "materiel": "haltères", "series": 3, "reps": (8, 12), "par_jambe": True, "repos": "2-3 min"},
            {"nom": "Leg curl assis",           "materiel": "machine",  "series": 3, "reps": (12, 15), "repos": "1-2 min"},
            {"nom": "Mollets assis",            "materiel": "machine",  "series": 2, "reps": (12, 15), "repos": "1-2 min"},
        ],
    },
    "mardi": {
        "nom": "Haut A",
        "type": "force_haut",
        "exercices": [
            {"nom": "Développé couché",         "materiel": "barre",    "series": 3, "reps": (6, 8), "repos": "3-5 min"},
            {"nom": "Traction lestée",          "materiel": "lest",     "series": 3, "reps": (8, 10), "repos": "3 min"},
            {"nom": "Rowing buste penché",      "materiel": "barre",    "series": 3, "reps": (10, 12), "repos": "2-3 min"},
            {"nom": "Dips buste penché",        "materiel": "barres parallèles", "series": 3, "reps": (8, 12), "repos": "2-3 min"},
            {"nom": "Élévations latérales poulie", "materiel": "poulie", "series": 3, "reps": (12, 15), "par_bras": True, "repos": "1-2 min"},
            {"nom": "Curl biceps machine",      "materiel": "machine",  "series": 2, "reps": (10, 12), "repos": "1-2 min"},
        ],
    },
    "jeudi": {
        "nom": "Haut B",
        "type": "force_haut",
        "exercices": [
            {"nom": "Développé incliné",            "materiel": "haltères", "series": 3, "reps": (8, 10), "repos": "3 min"},
            {"nom": "Tirage vertical prise neutre", "materiel": "poulie",   "series": 3, "reps": (10, 12), "repos": "2-3 min"},
            {"nom": "Rowing assis, prise large pronation", "materiel": "poulie", "series": 3, "reps": (10, 12), "repos": "2-3 min"},
            {"nom": "Élévations latérales poulie",  "materiel": "poulie",   "series": 3, "reps": (12, 15), "par_bras": True, "repos": "1-2 min"},
            {"nom": "Deltoïde postérieur",          "materiel": "poulie",   "series": 3, "reps": (12, 15), "repos": "1-2 min"},
            {"nom": "Curl Bayesian poulie",         "materiel": "poulie",   "series": 2, "reps": (10, 12), "par_bras": True, "repos": "1-2 min"},
            {"nom": "Extension triceps overhead",   "materiel": "poulie",   "series": 2, "reps": (12, 15), "repos": "1-2 min"},
        ],
    },
    "samedi": {
        "nom": "Haut C",
        "type": "force_haut",
        "exercices": [
            {"nom": "Développé pectoraux",             "materiel": "machine",  "series": 3, "reps": (12, 15), "par_bras": True, "repos": "2 min"},
            {"nom": "Tirage grand dorsal unilatéral", "materiel": "poulie haute", "series": 3, "reps": (8, 12), "par_bras": True, "repos": "2 min"},
            {"nom": "Élévations latérales poulie",     "materiel": "poulie",   "series": 3, "reps": (15, 20), "par_bras": True, "repos": "1-2 min"},
            {"nom": "Deltoïde postérieur",             "materiel": "poulie",   "series": 3, "reps": (12, 15), "repos": "1-2 min"},
            {"nom": "Curl marteau au pupitre",         "materiel": "haltères", "series": 2, "reps": (10, 12), "repos": "1-2 min"},
            {"nom": "Pressdown barre droite",          "materiel": "poulie",   "series": 2, "reps": (12, 15), "repos": "1-2 min"},
        ],
    },
}
```

### RIR par semaine

```python
CYCLE_RIR = {1: 3, 2: 2, 3: 1, 4: 4}
```

### Semaine de décharge

```python
SEMAINE_DECHARGE = 4
```

### Facteur de volume en décharge

```python
FACTEUR_DECHARGE = 0.6
```

### Maxima de départ

```python
MAXES = {
    # Bas (lundi)
    "Squat barre haute":                   79,     # recalé 2026-08-08 : 67,5 kg jugés trop lourds
    "Soulevé de terre roumain":            99,     # recalé 2026-08-09 : fait à 70 kg aux reps prescrites
    "Squat bulgare":                       23,     # par haltère — recalé 2026-08-08, viser 16 kg
    "Leg curl assis":                      43,     # recalé 2026-08-13 : 32 kg est le cran réel (colonne 32/39/45/52)
    # confirmé par l'usage 2026-09-20 : les 35 kg prescrits conviennent. Valeur
    # de départ à l'origine, jamais mesurée, mais validée par la série.
    "Mollets assis":                       52.5,   # mesure 2026-09-28 : 40 kg x 8 a RIR 1

    # Haut A (mardi)
    # 2026-09-20 : recalé à 93 sur la foi de « séances déjà faites à 70 kg ».
    # ERREUR, annulée le 2026-09-21 : 70 kg N'ÉTAIT PAS la charge de base, c'était
    # la base (67,5) PLUS le cycle déjà crédité. Le comparer à la base revenait à
    # compter ce cycle deux fois, et la séance suivante sautait à 72,5 kg sans
    # que rien ne l'ait mérité.
    #
    # La règle : une charge rapportée se compare à la charge PRESCRITE DU JOUR,
    # crédits compris — jamais à la base. Ici les deux valaient 70 : rien à
    # recaler, la valeur d'origine était juste.
    "Développé couché":                    90,
    "Traction lestée":                     101,     # total corps+lest ; cale pour un ajout NUL a 71,7 kg, suit ensuite le poids
    "Rowing buste penché":                 77,     # recalé 2026-08-12 : viser 50 kg de série
    "Dips buste penché":                   101,     # total corps+lest ; cale pour un ajout NUL a 71,7 kg, suit ensuite le poids
    "Pressdown barre droite":              52,     # recale 2026-08-21 : 29,3 kg encore a RIR 4, trop leger
    "Curl biceps machine":                 31,     # recalé 2026-08-13 : 23 kg est le cran réel (colonne 23/27/32/36)

    # Haut B (jeudi)
    "Développé incliné":                   31,     # par haltère — recalé sur 22 kg de série
    # confirmé par l'usage 2026-09-20 : les 52 kg prescrits conviennent. Le max
    # lui-même n'a jamais été mesuré, mais c'est la charge de travail qui compte
    # et elle est validée — le 1RM n'est ici qu'un intermédiaire de calcul.
    "Tirage vertical prise neutre":        80,
    "Rowing assis, prise large pronation": 57,     # confirmé 2026-08-13 : 39 kg réalisé, cran exact prescrit
    "Élévations latérales poulie":         10,     # confirmé 2026-08-13 : 4,5 kg réalisé, cran exact prescrit
    "Curl Bayesian poulie":                17,     # recalé 2026-08-13 : 11,3 kg par bras
    "Extension triceps overhead":          27,     # recalé 2026-08-13 : fait à 15,8 kg

    # Haut C (samedi)
    # PAR BRAS : la machine se charge côté par côté, chaque chariot pesant 6,8 kg.
    # Comme tous les unilatéraux du document, le max est celui d'UN côté.
    # recalé 2026-09-20 : 15 kg de disques + 6,8 de chariot = 21,8 kg par bras
    # tenus sur 3x12-15. 21,8 / 0,5917 = 36,8 — arrondi à 37.
    "Développé pectoraux":                 37,
    "Tirage grand dorsal unilatéral":      52,     # déduit de 40 kg x 8 à RIR 1
    # Même exercice jeudi et samedi depuis le 2026-08-06, donc une seule entrée.
    # 16 kg repris de l'ancien oiseau aux haltères (9 kg x 15) sur décision du
    # propriétaire le 2026-08-07 : à recaler après une séance à la poulie.
    "Deltoïde postérieur":                  8,     # recalé 2026-08-13 : fait à 4,5 kg, pas 9
    # 2026-08-21 : 12 kg atteint a l'échec, max ramené à 15. 2026-09-19 : les
    # mêmes 12 kg tenus sur 10-12 reps avec 2-3 en réserve — c'est un progrès,
    # pas une erreur de mesure.
    "Curl marteau au pupitre":             18,
}
```

### Paliers réels des machines

```python
MACHINES = {
    # Colonne partagée par trois postes — pas d'environ 6,8 kg (empilage en livres).
    "Leg curl assis":                       [32, 39, 45, 52, 59, 66, 73, 79],
    "Tirage vertical prise neutre":         [32, 39, 45, 52, 59, 66, 73, 79],
    "Rowing assis, prise large pronation":  [32, 39, 45, 52, 59, 66, 73, 79],

    # Machine à biceps — pas d'environ 4,5 kg.
    "Curl biceps machine":                  [23, 27, 32, 36, 41, 45, 50, 54, 59],

    # Stations à poulie classiques. Les chiffres viennent d'un empilage en
    # livres : le pas vaut donc environ 2,25 kg, pas exactement. Le 14e cran
    # est relevé à 32 sur la machine (2026-09-20) et non 31,5 comme le
    # calcul le donnait — les autres crans restent déduits, à corriger de la
    # même façon au fur et à mesure qu'ils sont lus.
    "Élévations latérales poulie":          [2.3, 4.5, 6.8, 9, 11.3, 13.5, 15.8, 18, 20.3, 22.5,
                                             24.8, 27, 29.3, 32, 33.8, 36, 38.3, 40.5, 42.8, 45],
    "Deltoïde postérieur":                  [2.3, 4.5, 6.8, 9, 11.3, 13.5, 15.8, 18, 20.3, 22.5,
                                             24.8, 27, 29.3, 32, 33.8, 36, 38.3, 40.5, 42.8, 45],
    "Curl Bayesian poulie":                 [2.3, 4.5, 6.8, 9, 11.3, 13.5, 15.8, 18, 20.3, 22.5,
                                             24.8, 27, 29.3, 32, 33.8, 36, 38.3, 40.5, 42.8, 45],
    "Extension triceps overhead":           [2.3, 4.5, 6.8, 9, 11.3, 13.5, 15.8, 18, 20.3, 22.5,
                                             24.8, 27, 29.3, 32, 33.8, 36, 38.3, 40.5, 42.8, 45],
    "Pressdown barre droite":               [2.3, 4.5, 6.8, 9, 11.3, 13.5, 15.8, 18, 20.3, 22.5,
                                             24.8, 27, 29.3, 32, 33.8, 36, 38.3, 40.5, 42.8, 45],
    "Tirage grand dorsal unilatéral":       [2.3, 4.5, 6.8, 9, 11.3, 13.5, 15.8, 18, 20.3, 22.5,
                                             24.8, 27, 29.3, 32, 33.8, 36, 38.3, 40.5, 42.8, 45],

    # Encore à relever : la colonne des mollets assis.
}
```

### Tares des machines à disques

```python
TARES = {
    "Développé pectoraux": 6.8,     # relevé 2026-09-20
}
```

### Incréments spécifiques

```python
PAS = {
    "Développé pectoraux": 1.25,    # un seul disque par bras (confirmé 2026-09-20)
}
```

### Ordre d’affichage des groupes musculaires

```python
ORDRE_MUSCLES = ["jambes", "pectoraux", "dos", "épaules", "biceps", "triceps", "mollets"]
```

### Groupe musculaire par exercice

```python
MUSCLES = {
    "Squat barre haute":                    "jambes",
    "Soulevé de terre roumain":             "jambes",
    "Squat bulgare":                        "jambes",
    "Leg curl assis":                       "jambes",
    "Mollets assis":                        "mollets",

    "Développé couché":                     "pectoraux",
    "Développé incliné":                    "pectoraux",
    "Développé pectoraux":                  "pectoraux",
    # Buste penché : le document l'oriente explicitement vers les pectoraux,
    # « vertical, il devient un mouvement triceps ».
    "Dips buste penché":                    "pectoraux",

    "Traction lestée":                      "dos",
    "Tirage vertical prise neutre":         "dos",
    "Tirage grand dorsal unilatéral":       "dos",
    "Rowing buste penché":                  "dos",
    "Rowing assis, prise large pronation":  "dos",

    "Élévations latérales poulie":          "épaules",
    "Deltoïde postérieur":                  "épaules",

    "Curl biceps machine":                  "biceps",
    "Curl Bayesian poulie":                 "biceps",
    "Curl marteau au pupitre":              "biceps",

    "Pressdown barre droite":               "triceps",
    "Extension triceps overhead":           "triceps",
}
```

### Consignes techniques

```python
TECHNIQUE = {
    # --- Lundi
    "Squat barre haute": {
        "reglages": "Pieds au moins à largeur d'épaules, rotation externe de 15 à 30°. Barre en haut des trapèzes, mains aussi près des épaules que possible. Grande inspiration dans le ventre avant chaque descente.",
        "execution": "Barre sur une ligne verticale, centrée au-dessus du milieu du pied. Buste le plus vertical possible ; à la remontée, pousser le dos dans la barre. Descendre au minimum à la parallèle, idéalement pli de hanche sous le haut du genou.",
        "erreurs": "Genoux qui rentrent vers l'intérieur · charger trop et ne descendre qu'à moitié · arrondissement du bas du dos en position basse. Signal de surcharge : trajectoire ou profondeur perdues, talons qui décollent.",
    },
    "Soulevé de terre roumain": {
        "reglages": "Pieds à largeur d'épaules, pointes droit devant. Départ debout, barre sortie du rack. Poitrine levée, colonne verrouillée avant de descendre.",
        "execution": "Pousser les hanches loin vers l'arrière, tibias verticaux. La barre reste en contact avec les jambes. Descendre seulement jusqu'où les hanches reculent sans arrondir le dos — entre bas du genou et mi-tibia. Ne pas chercher le sol.",
        "erreurs": "Descendre trop bas et arrondir · genoux qui avancent, ce qui en fait un semi-squat · barre qui dérive vers l'avant. Signal de surcharge : les genoux avancent pour aider.",
    },
    "Squat bulgare": {
        "reglages": "Distance au banc réglée pour que le genou avant puisse avancer au maximum. Fixer ce réglage une fois : s'il change, les comparaisons de charge ne valent plus rien.",
        "execution": "Trajectoire du buste verticale pour un focus quadriceps. Si le genou se rapproche trop du corps en bas, réduire légèrement l'amplitude.",
        "erreurs": "Trajectoire d'avant en arrière au lieu de verticale · ne pas laisser le genou avancer assez.",
    },
    "Leg curl assis": {
        "reglages": "MACHINE (relevé le 2026-08-12) : butée de longueur de jambe sur le cran 6, les deux disques d'amplitude sur le cran 1. Fixer ces deux réglages une fois pour toutes : s'ils changent, les comparaisons de charge d'un cycle à l'autre ne valent plus rien. Bassin en position neutre, ne pas sortir la poitrine ni cambrer les lombaires avant de commencer.",
        "execution": "Verrouiller la colonne en contractant abdominaux et lombaires simultanément. Le bassin ne bouge pas de la série.",
        "erreurs": "Initier par une cambrure lombaire · laisser le bassin bouger. Dès que le dos se cambre en fin de contraction, réduire l'amplitude plutôt que tricher.",
    },
    "Mollets assis": {
        "reglages": "Genou fléchi : c'est ce qui cible le soléaire plutôt que les jumeaux.",
        "execution": "Contrôler la phase d'étirement, pause de 1 à 2 s en position basse. Utiliser la stabilité de la machine pour produire un maximum de force.",
        "erreurs": "Rebondir en bas · amplitude écourtée.",
    },

    # --- Mardi
    "Développé couché": {
        "reglages": "Prise à ~1,5 fois la largeur des épaules, poignets empilés sous les articulations. Omoplates serrées et tirées vers le bas. Léger arc lombaire, pas le dos plat. Appui des pieds au sol.",
        "execution": "Coudes à 45° du torse, alignés sous la barre. La barre touche la poitrine juste sous les mamelons. La trajectoire n'est pas verticale : elle descend un peu vers l'avant puis remonte en arc vers le visage.",
        "erreurs": "Rebondir sur la cage thoracique · dos complètement plat · omoplates non verrouillées.",
    },
    "Traction lestée": {
        "reglages": "Prise en pronation, ~1,5 fois la largeur des épaules. Plus large réduit l'amplitude et fait mal aux poignets.",
        "execution": "Initier en abaissant les omoplates, comme pour mettre les coudes dans les poches arrière. Monter menton au-dessus de la barre. Descendre en extension quasi complète. Corps rigide, fessiers et abdos contractés.",
        "erreurs": "Élan des jambes · amplitude incomplète en haut comme en bas, l'erreur la plus fréquente.",
    },
    "Rowing buste penché": {
        "reglages": "Buste quasiment parallèle au sol. Repère : si vous voyez le logo de votre t-shirt dans le miroir, vous êtes trop redressé.",
        "execution": "Coudes qui montent et reculent à 45-65° du torse. Départ omoplates étirées, initier en les serrant, contracter en haut. La barre touche le bas du sternum.",
        "erreurs": "Élan des jambes ou des hanches · charger trop, ce qui dégrade la technique et coûte cher en fatigue nerveuse. Si c'est le bas du dos qui fait arrêter, passer au rowing haltère sur banc incliné.",
    },
    "Dips buste penché": {
        "reglages": "Prise de largeur moyenne. Buste penché vers l'avant d'environ 30° pour cibler les pectoraux — rester vertical bascule le travail sur les triceps.",
        "execution": "Descendre jusqu'à un étirement profond des pectoraux, sans forcer au-delà de ce que l'épaule supporte. Coudes légèrement ouverts. Lester dès que 12 reps passent proprement.",
        "erreurs": "Hausser les épaules ou les laisser rouler vers l'avant · forcer malgré un pincement à l'épaule : réduire la descente ou se pencher davantage.",
    },
    "Curl biceps machine": {
        "reglages": "Bas du bras à plat contre le pupitre, épaules basses qui ne remontent jamais.",
        "execution": "Supination maximale pour recruter pleinement le biceps. En bas, humérus perpendiculaire au sol pour garder la tension. Court arrêt en contraction haute. Créneau d'échec réel : aller au bout sur la dernière série.",
        "erreurs": "Décoller les épaules du pupitre · laisser le coude bouger.",
    },

    # --- Jeudi
    "Développé incliné": {
        "reglages": "Banc à 30°. Au-delà de 45°, c'est le deltoïde antérieur qui prend le relais et le haut des pectoraux est perdu. Omoplates resserrées et abaissées. Démarrer bras tendus.",
        "execution": "Trajectoire la plus verticale possible, mains pile au-dessus des coudes surtout en position basse. Angle bras-buste d'environ 70°.",
        "erreurs": "Trop incliner le banc · écarter excessivement les coudes · faire se toucher les haltères en haut, ce qui supprime la tension.",
    },
    "Tirage vertical prise neutre": {
        "reglages": "Largeur moyenne, environ 1 à 1,5 fois la largeur des épaules — ni la poignée en V serrée, ni une barre neutre très large. En prise serrée les biceps prennent le dessus et lâchent avant les dorsaux ; en prise trop large l'amplitude se raccourcit et la contraction basse est perdue. Posture verticale et stable, légère inclinaison arrière tolérée, pas davantage.",
        "execution": "Initier par la dépression des omoplates, avant toute flexion de coude. Conduire avec les coudes, tirés vers le bas et vers l'intérieur. Descendre jusqu'au haut de la poitrine ; en haut, étirer sans relâcher la tension.",
        "erreurs": "Amplitude incomplète · élan du corps · se pencher en arrière et transformer le tirage en rowing.",
    },
    "Rowing assis, prise large pronation": {
        "reglages": "Prise large, coudes écartés à 45-60°. Cette prise vise trapèzes moyens et rhomboïdes — l'épaisseur — là où le tirage vertical fait la largeur.",
        "execution": "Se pencher légèrement vers l'avant sur la phase négative pour accentuer l'étirement, dos neutre à la contraction. Rétraction des omoplates en fin de tirage.",
        "erreurs": "Balancement du buste · tirer les coudes trop loin derrière la ligne du torse, sans bénéfice et au prix d'un stress d'épaule.",
    },
    "Élévations latérales poulie": {
        "reglages": "POULIE (relevé le 2026-08-20) : hauteur sur le cran 4, câble perpendiculaire au bras au milieu du mouvement, là où le muscle est le plus fort. Se tenir bien droit.",
        "execution": "Monter le bras sur le côté, ou légèrement vers l'avant à 45°, plus confortable pour l'articulation d'après les tests EMG. Jeudi = travail en charge (12-15), samedi = volume (15-20).",
        "erreurs": "Se pencher sur le côté pour tricher, ce qui annule l'intérêt de la poulie · hausser les trapèzes · laisser la main descendre trop bas et perdre la tension.",
    },
    "Deltoïde postérieur": {
        "reglages": "POULIE (relevé le 2026-08-20) : hauteur sur le cran 11. À la poulie unilatérale, câble perpendiculaire à l'humérus au moment de l'étirement maximal, bras croisé devant le buste. Au pec deck inversé ou à l'oiseau, banc incliné pour que les haltères frôlent le sol.",
        "execution": "Les omoplates ne bougent pas — elles restent écartées, décrochées, pour isoler le deltoïde. Trajectoire non horizontale : partir à hauteur des yeux, finir légèrement sous le niveau des épaules.",
        "erreurs": "Resserrer les omoplates, ce qui bascule le travail sur trapèzes et rhomboïdes — c'est l'erreur qui rend l'exercice inutile · charge trop lourde · trajectoire trop haute.",
    },
    "Curl Bayesian poulie": {
        "reglages": "POULIE (relevé le 2026-08-20) : hauteur sur le cran 6. Dos à la poulie. L'humérus reste perpendiculaire au sol, bras le long du corps.",
        "execution": "Exécution contrôlée, surtout au début du mouvement où l'étirement est maximal. Tension continue du début à la fin.",
        "erreurs": "Se pencher en avant ou reculer les coudes : ces compensations annulent exactement la courbe de résistance qui justifie cet exercice.",
    },
    "Extension triceps overhead": {
        "reglages": "Bras derrière la tête. Sans poulie réglable, utiliser un siège pour stabiliser le buste — le manque de stabilité est le principal défaut de cet exercice.",
        "execution": "Chercher l'étirement complet du chef long en descendant loin derrière la tête, puis extension totale. Phase excentrique lente.",
        "erreurs": "Trop écarter les coudes vers l'extérieur.",
    },

    # --- Samedi
    "Développé pectoraux": {
        "reglages": "Siège réglé pour que les poignées arrivent au milieu ou bas des pectoraux. Trop haut, le mouvement devient un incliné et charge les deltoïdes antérieurs.",
        "execution": "Buste verrouillé, omoplates fixes et resserrées du début à la fin, tête immobile. Amplitude active (75-80 %) : ne pas tendre complètement si la résistance chute en fin de course. Excentrique 3 s, concentrique explosive. Créneau d'échec réel : dernière série jusqu'au bout.",
        "erreurs": "Décoller les omoplates pour pousser plus loin · utiliser l'inertie.",
    },
    "Tirage grand dorsal unilatéral": {
        "reglages": "Poulie haute, assis sur un banc — la stabilité extérieure est l'argument central, debout on dépense de la force à se tenir. De profil ou de trois-quarts, buste orienté pour que le câble s'aligne sur les fibres. Poignée simple, prise au ressenti.",
        "execution": "Visualiser que l'on pousse le coude vers le bas et vers l'arrière, vers la crête iliaque, plutôt que de tirer vers soi. Amplitude active. En bas, coude contre le buste.",
        "erreurs": "Écarter le coude vers l'extérieur en fin de mouvement, l'erreur la plus fréquente : le dorsal perd presque tout son engagement · initier avec le biceps · se servir de l'élan du buste.",
    },
    "Curl marteau au pupitre": {
        "reglages": "Coudes fixés sur le support, comme au curl classique.",
        "execution": "Prise neutre, pouces vers le haut tout du long. Mouvement contrôlé, sans élan. Possible bras par bras si le banc est étroit, ce qui aide à contrôler la descente.",
        "erreurs": "Charge trop lourde qui force une rotation du buste ou un décollage du bras.",
    },
    "Pressdown barre droite": {
        "reglages": "Coudes serrés contre le buste et fixes. Se reculer d'environ un mètre de la poulie pour garder la tension jusqu'en fin de contraction.",
        "execution": "Extension complète des bras. Pause d'une seconde en bas, en contraction maximale.",
        "erreurs": "Prise en supination, inutile puisque le triceps n'a aucun rôle dans la rotation de l'avant-bras · tricher en écrasant la barre avec le poids du corps.",
    },
}
```

## Données à personnaliser

Les maxima, le poids de corps et les réglages des machines proviennent du projet d’origine. Vérifie-les et corrige-les si tes mesures ou ton matériel ont changé. Une valeur absente ou nulle ne donne pas lieu à une charge inventée.


