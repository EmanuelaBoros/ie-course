# HIPE-2022 v2.1 — HIPE-2020, français

Données du TP NER + NEL : articles de presse historique en français, issus du dossier officiel [HIPE-2022-data/data/v2.1/hipe2020/fr](https://github.com/hipe-eval/HIPE-2022-data/tree/main/data/v2.1/hipe2020/fr).

Cette adaptation conserve **uniquement quatre colonnes**, dans cet ordre :

```text
TOKEN	NE-COARSE-LIT	NEL-LIT	MISC
```

| Colonne | Contenu |
|---|---|
| `TOKEN` | Token original, y compris les erreurs d’OCR. |
| `NE-COARSE-LIT` | Étiquette NER littérale grossière, avec préfixe BIO : par exemple `B-pers`, `I-org`, `O`. |
| `NEL-LIT` | Annotation de liaison littérale originale : identifiant Wikidata, `NIL`, `_`, ou autre valeur du fichier source. |
| `MISC` | Informations originales : notamment `NoSpaceAfter`, `EndOfLine`, `EndOfSentence`, éventuellement combinées par `\|`. |

Aucun token, type d’entité ou identifiant n’est filtré ou normalisé. En particulier, `pers`, `org`, `loc`, `prod` et `time` sont conservés ; `NIL` et `_` restent distincts. Le texte n’est pas retokenisé.

Les lignes de commentaires (`# `), les identifiants de documents et les lignes vides sont conservés. Les commentaires `applicable_columns` décrivent le fichier **source** ; l’en-tête de cette adaptation fait autorité pour ses quatre colonnes. Les frontières de phrases sont signalées par `EndOfSentence` dans `MISC` : ne pas supposer qu’une ligne vide correspond à une phrase. Cette segmentation automatique peut être imparfaite.

## Fichiers

| Fichier | Documents | Tokens | Utilisation |
|---|---:|---:|---|
| [train](HIPE-2022-v2.1-hipe2020-train-fr.tsv) | 158 | 166 220 | Construire les modèles et dictionnaires. |
| [dev](HIPE-2022-v2.1-hipe2020-dev-fr.tsv) | 43 | 37 953 | Choisir règles, paramètres et prompts. |
| [test](HIPE-2022-v2.1-hipe2020-test-fr.tsv) | 43 | 40 854 | Évaluation finale annotée, après gel des choix. |
| [test_ELmasked](HIPE-2022-v2.1-hipe2020-test_ELmasked-fr.tsv) | 43 | 40 854 | Variante officielle avec annotations de liaison masquées. |
| [test_allmasked](HIPE-2022-v2.1-hipe2020-test_allmasked-fr.tsv) | 43 | 40 854 | Variante officielle avec annotations NER et NEL masquées. |

Les trois fichiers de test contiennent les **mêmes documents**, pas trois ensembles indépendants. Les références du test sont publiques : ne pas les utiliser pour concevoir les systèmes ou les prompts. Les variantes masquées ne fournissent pas les annotations nécessaires au calcul des scores.

## Chargement dans le notebook

Ce code fonctionne avec la bibliothèque standard, y compris dans Colab. Il conserve les données par document et n’interprète pas encore les segments BIO.

```python
import csv
from urllib.request import urlopen

BASE = "https://raw.githubusercontent.com/EmanuelaBoros/ie-course/main/data/hipe2020-fr"
COLUMNS = ["TOKEN", "NE-COARSE-LIT", "NEL-LIT", "MISC"]

def read_hipe(lines):
    rows = csv.reader(lines, delimiter="\t", quoting=csv.QUOTE_NONE)
    assert next(rows) == COLUMNS
    documents = []
    current = None
    for row in rows:
        if not row:
            continue
        if row[0].startswith("# "):
            if row[0].startswith("# hipe2022:document_id = "):
                current = {"doc_id": row[0].split(" = ", 1)[1], "rows": []}
                documents.append(current)
            continue
        assert current is not None and len(row) == 4
        current["rows"].append(dict(zip(COLUMNS, row)))
    return documents

# Colab / accès distant, une fois les fichiers publiés sur GitHub :
with urlopen(f"{BASE}/HIPE-2022-v2.1-hipe2020-train-fr.tsv") as response:
    train = read_hipe(response.read().decode("utf-8").splitlines())
print(len(train), train[0]["rows"][:3])

# En local, depuis la racine du dépôt :
# with open("data/hipe2020-fr/HIPE-2022-v2.1-hipe2020-train-fr.tsv", encoding="utf-8") as f:
#     train = read_hipe(f)
```

Pour les exercices NEL, ces fichiers fournissent des annotations de référence, **pas une base de candidats et de descriptions Wikidata**. Cette ressource doit être préparée séparément. Le notebook actuel contient encore un scénario synthétique : ses identifiants `PER_01` / `ORG_01` et sa petite base ne sont pas compatibles directement avec HIPE.

## Reproduire la préparation

Depuis la racine du dépôt, avec Python 3.10 ou plus récent :

```bash
python scripts/prepare_hipe2020_fr.py
```

Le script télécharge les fichiers depuis le commit fixé `147f5bc3c7fb7e5c6b024a9ffd6503cd019fb9ea`, sélectionne les colonnes par leur nom et produit les cinq TSV et `manifest.json`. Aucun paquet externe requis. Pour travailler hors ligne :

```bash
python scripts/prepare_hipe2020_fr.py --source-dir /chemin/HIPE-2022-data/data/v2.1/hipe2020/fr
```

Le manifeste enregistre les URL, les empreintes SHA-256 des fichiers sources et préparés, ainsi que les nombres de documents, tokens et marqueurs de fin de phrase.

## Provenance et licence

- Source : [HIPE-2022-data](https://github.com/hipe-eval/HIPE-2022-data), version v2.1, sous-corpus HIPE-2020, français.
- Jeu d’origine : [CLEF-HIPE-2020, DOI 10.5281/zenodo.6046853](https://doi.org/10.5281/zenodo.6046853).
- [Consignes d’annotation](https://doi.org/10.5281/zenodo.3585750).
- [Documentation originale du sous-corpus](UPSTREAM-README.md), conservée telle quelle. Sa remarque sur l’absence de train est historique ; le dossier v2.1 sélectionné contient bien un fichier `train`.
- Licence des données et de cette adaptation : **CC BY-NC-SA 4.0** ; voir [LICENSE](LICENSE). Conserver l’attribution, l’usage non commercial et le partage dans les mêmes conditions lors d’une redistribution.
- Modification pour ce cours : sélection des quatre colonnes ci-dessus. Les annotations restent celles du jeu original.
