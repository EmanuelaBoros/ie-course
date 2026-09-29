<p align="center">
  <img src="./ie_banner.png" width="100%" alt="Des documents textuels aux informations structurées">
</p>

## Extraction d’information : reconnaissance et liaison d’entités

**Enseignante :** Emanuela Boros  
**Format :** 1 h 30 de cours magistral et 3 h de travaux pratiques

Comment transformer un texte en informations structurées ? Ce cours présente les principales tâches et méthodes d’extraction d’information, puis les applique à la reconnaissance d’entités nommées (NER) et à leur liaison à une base de connaissances (NEL).

Le travail étudiant se limite au **TP de trois heures**, réalisé en binôme. Aucun projet de groupe ni présentation supplémentaire n’est demandé.

## Supports du cours

| Partie | Sujet | Supports |
|---|---|---|
| 1 | Extraction d’information et reconnaissance d’entités | [Présentation de la partie](./1-Information-Extraction-and-NER/01.md) · [Diapositives PDF](./1-Information-Extraction-and-NER/01-information-extraction.pdf) · [PowerPoint](./1-Information-Extraction-and-NER/01-information-extraction.pptx) |
| 2 | Liaison d’entités et représentations vectorielles | [Présentation de la partie](./2-Named-Entity-Linking/02.md) · [Diapositives 61 à 82](./1-Information-Extraction-and-NER/01-information-extraction.pdf#page=61) |
| TP | Reconnaissance, liaison et comparaison avec une IA générative | [Consignes et notebook en français](./4-Practical/04.md) |

Les deux parties composent un seul cours de 90 minutes, suivi d’un seul TP de trois heures.

## Notions abordées

- Utilité de l’extraction d’information et distinction avec la recherche d’information.
- Entités, coréférence, relations, événements et informations temporelles.
- Règles, dictionnaires, modèles statistiques, réseaux neuronaux et méthodes génératives.
- Conventions d’annotation, frontières des mentions, étiquettes BIO et évaluation exacte.
- Recherche de candidats, désambiguïsation et cas NIL.
- Représentations vectorielles d’entités, bi-encodeurs et reclassement.
- Comparaison contrôlée entre un algorithme étudiant et une IA générative.

## Déroulement du TP

Construisez un système de reconnaissance par dictionnaire et un système de liaison contextuelle. Comparez leurs sorties à celles d’un modèle génératif sur les mêmes exemples, avec le même schéma et les mêmes mesures.

| Durée | Activité |
|---|---|
| 0–30 min | Examiner les données, les annotations et les mesures |
| 30–75 min | Implémenter la NER et analyser les erreurs de frontières |
| 75–120 min | Rechercher les candidats et utiliser le contexte pour la NEL |
| 120–155 min | Exécuter la comparaison générative et figer les choix |
| 155–180 min | Évaluer les sorties et expliquer les différences |

**À rendre :** le notebook complété, les prédictions et réponses IA sauvegardées, les scores et une courte analyse de trois erreurs. Aucun service d’IA payant n’est nécessaire. Une difficulté d’accès doit être signalée, sans inventer de résultats.

## Données

Les [données françaises HIPE-2022 v2.1](https://github.com/EmanuelaBoros/ie-course/tree/main/data/hipe2020-fr) sont disponibles avec les colonnes `TOKEN`, `NE-COARSE-LIT`, `NEL-LIT` et `MISC`. Le dossier contient les partitions, les variantes de test masquées, un exemple de chargement et la licence.

Le notebook actuellement publié utilise encore des exemples synthétiques pour introduire les algorithmes. Son adaptation complète aux annotations HIPE et aux candidats Wikidata reste à effectuer. Les consignes du [TP](./4-Practical/04.md) précisent cette distinction.

## Ressources

- [Modèle de liaison d’entités historiques d’Emanuela Boros](https://huggingface.co/emanuelaboros/historical-nel).
- [Hugging Face : classification de tokens](https://huggingface.co/learn/llm-course/en/chapter7/2).
- [spaCy : reconnaissance par règles](https://spacy.io/usage/rule-based-matching/).
- [BLINK : recherche dense d’entités](https://aclanthology.org/2020.emnlp-main.519/).
- [Communauté L3i++ sur Hugging Face](https://huggingface.co/l3ipp) : vous pouvez demander à la rejoindre. Aucune publication de modèle n’est demandée dans ce TP.

## Accès au dépôt

```bash
git clone https://github.com/EmanuelaBoros/ie-course.git
```

## Contact

Emanuela Boros  
[emanuela.boros@univ-lr.fr](mailto:emanuela.boros@univ-lr.fr)

Structure du site adaptée du [cours de machine learning](https://github.com/USTH-classroom/ml-course). [Licence du modèle de site](./template-license.txt).
