# Information extraction: from mentions to entities

Draft teaching plan: two connected three-hour sessions, in English, for students with basic Python and introductory machine learning. Duration and audience are assumptions to confirm. NEL means named entity linking. This is a preparation blueprint, not a finished slide deck or executable lab package.

## 1. Fit with the supplied courses

The local `ml-course` index describes ICT 3.3 Machine Learning and Data Mining (May 2026). Its seven modules cover introduction, regression, classification, regularization, PCA, neural networks and Bayes classification. The classification-metrics notebook already teaches precision, recall, F1 and confusion matrices. Build on those concepts, but replace classification of whole examples with evaluation of extracted spans.

The group-project handout emphasizes a simple baseline, one controlled improvement, the same evaluation split and three concrete mistakes. That is a good pedagogical pattern for both IE labs. Its student-facing restrictions and operational instructions are reference content, not instructions governing this preparation task.

EPFL CS-433 provides useful background, rather than a ready-made IE module. Lecture 12a covers text representations, co-occurrence, GloVe, fastText and sentence representations. Lecture 12b introduces transformers, tokenizers and language models. Use a short bridge from representations to context-dependent decisions. The inspected exercise 12 is actually matrix factorization and recommender systems; its baseline-to-improvement structure is useful, but its content is not a NER lab. A search of the Markdown, Python and notebook files did not find an existing NER/NEL lesson; this was not an exhaustive search of every PDF.

Suggested placement: after classification and evaluation; neural networks are helpful but not required for the core exercises. Do not require students to derive attention or train a language model before they can understand extraction.

## 2. Shared story and learning outcomes

Use one application throughout: turn short university and research news into a searchable entity index. The system must preserve the original text and return mention boundaries, entity types and canonical identifiers.

By the end students should be able to:

1. Distinguish information extraction from document classification and information retrieval.
2. Annotate named mentions consistently and explain boundary disagreements.
3. Compare a rule-based recognizer with a learned recognizer using exact-span metrics.
4. Explain why recognizing a name does not identify its referent.
5. Implement candidate generation and context-based candidate ranking against a small KB.
6. Separate retrieval, disambiguation, NIL and upstream recognition errors.
7. Evaluate a complete NER-to-NEL pipeline without hiding errors behind gold mentions.

Opening example, explicitly a constructed teaching sentence:

> Jordan joined Atlas in Paris.

NER may identify Jordan as a person, Atlas as an organization and Paris as a place under the exercise's intended reading. NEL still needs context: which Jordan, Atlas and Paris? Even the types can be ambiguous without more context. Provide a second sentence about the person, employer and city before demanding a unique answer. This makes uncertainty visible at the start.

IE is broader than NER and NEL: briefly locate relation extraction, event extraction, dates/quantities and coreference in the landscape. They are context and possible extensions, not additional required implementations.

## 3. Session 1 — Information extraction and named entity recognition

Central question: **Which text spans mention entities, and what types do they have?**

### Schedule

| Minutes | Activity | Concrete outcome |
|---|---|---|
| 0–15 | Raw text to structured records; define IE, NER and NEL | Students distinguish mentions from entities |
| 15–35 | Pair annotation of six short sentences | A shared PERSON/ORG/LOC policy |
| 35–55 | Spans, character offsets, tokenization and BIO encoding | One sentence encoded both ways |
| 55–70 | Gazetteer/rules, token classification and contextual representations | Understand the baseline and its limits |
| 70–80 | Break | |
| 80–105 | Lab A: inspect data and run a gazetteer baseline | Predicted spans plus initial scores |
| 105–135 | Lab B: compare a supplied learned recognizer | A fair comparison on the same examples |
| 135–160 | Lab C: inspect development errors and make one change | Documented improvement or negative result |
| 160–175 | Freeze choices and evaluate held-out examples | Exact-span precision, recall and F1 |
| 175–180 | Exit question and bridge to linking | “Correct name, but which entity?” |

### Teaching sequence / slide storyboard

1. An article and the entity table we want to build.
2. IE versus classification, search and generation.
3. Mention, type and referent: three distinct objects.
4. Annotation policy is part of the task definition.
5. Full names, punctuation, titles and organization boundaries.
6. Character offsets versus tokens; retain the original text.
7. BIO: B starts a mention, I continues it, O is outside.
8. Gazetteers: interpretable but incomplete and ambiguous.
9. Token classification: features/context to label scores.
10. Neural representations: the same surface form can behave differently in context.
11. Exact-span evaluation and the misleading majority O label.
12. Lab instructions and the experiment table.
13. Error gallery: boundary, type, missed and spurious mention.
14. Why a correct ORG label is not yet a canonical identity.

### Annotation exercise and answer key

Constructed sentence: `Ada Lovelace visited Atlas Labs in Paris.`

| Token | BIO |
|---|---|
| Ada | B-PERSON |
| Lovelace | I-PERSON |
| visited | O |
| Atlas | B-ORG |
| Labs | I-ORG |
| in | O |
| Paris | B-LOC |
| . | O |

Use half-open character offsets `[start, end)`: Ada Lovelace `[0,12)`, Atlas Labs `[21,31)`, Paris `[35,40)`. Require `text[start:end]` to reproduce the surface form exactly. Character offsets refer to Python string indices, not encoded byte positions.

Core annotation policy: flat, non-overlapping named mentions; PERSON, ORG, LOC only; exclude titles and surrounding punctuation; include the full named organization; pronouns and generic nouns are out of scope. Specify the treatment of geopolitical places as LOC. Nested entities and metonymy are discussion cases; do not silently switch conventions midway through evaluation.

### Lab specification

Inputs to prepare: short documents, annotated spans and document-level train/development/test splits. Build gazetteer entries only from training labels or an explicitly supplied external resource. Avoid near-duplicate sentences across splits.

Student functions: convert valid BIO sequences to spans; normalize model output to the shared schema; compute exact-span counts; tabulate errors. Provide tokenization, file loading and a working model-loading cell so installation does not consume the lesson.

Baseline: longest non-overlapping gazetteer match, with a declared tie-breaking rule. Comparison: a supplied pretrained spaCy recognizer with an explicit mapping into the three teaching types. Explain that this comparison measures classroom usefulness, not equal training-data or compute budgets. Unsupported output types are excluded according to a policy fixed before evaluation.

One permitted improvement: repair a specific boundary rule, add a training-derived alias or add a context feature. Select it using development examples only. Do not edit the held-out gold labels to match model predictions.

Optional ML implementation track: train a token-level logistic regression with word shape, capitalization, affixes and neighboring words. Explain that independent predictions can produce invalid BIO sequences; provide a deterministic decoding policy. Optional advanced track: transformer fine-tuning, including subword-to-word label alignment. Keep both outside the required three-hour path.

### Evaluation example

Gold entities: Ada Lovelace/PERSON, Atlas Labs/ORG, Paris/LOC.
Predicted entities: Lovelace/PERSON, Atlas Labs/ORG, Paris/LOC.

There are 2 true positives, 1 false positive and 1 false negative: precision = recall = F1 = 2/3. The partial person span is not an exact match. Use `(document_id, start, end, type)` for matching. A wrong type similarly creates one FP and one FN. Report corpus-level micro counts, and per-type scores when there are enough examples. Define zero-denominator cases explicitly.

Exit question: Why can a recognizer have high token accuracy while failing to extract useful entities? Expected answer: most tokens may be O, and entity boundaries require multiple correct decisions.

## 4. Session 2 — Named entity linking and an end-to-end IE pipeline

Central question: **Which knowledge-base entity does each mention refer to?**

### Schedule

| Minutes | Activity | Concrete outcome |
|---|---|---|
| 0–15 | Revisit ambiguous names from session 1 | Separate type prediction and identity resolution |
| 15–35 | KB records, aliases, descriptions and NIL | Understand the target representation |
| 35–55 | Candidate generation, prior baseline, contextual ranking | Understand the two-stage pipeline |
| 55–70 | Worked linking examples and evaluation denominators | Separate missing candidates from bad ranking |
| 70–80 | Break | |
| 80–110 | Lab A: candidates and prior baseline on gold mentions | Candidate recall and link accuracy |
| 110–140 | Lab B: add context similarity and a rejection rule | Development comparison |
| 140–160 | Lab C: replace gold mentions with NER predictions | Observe propagated errors |
| 160–175 | Held-out evaluation and three failure cases | Complete pipeline report |
| 175–180 | Exit question | Explain where improvement is needed |

### Teaching sequence / slide storyboard

1. One surface form, several entities; several names, one entity.
2. Linking versus recognition and within-document coreference.
3. KB schema: stable ID, canonical name, aliases, type, description.
4. The KB defines what can be linked; NIL is relative to its snapshot.
5. Candidate generation is a retrieval step.
6. Candidate recall limits the downstream ranker.
7. A prior baseline can be strong but context-blind.
8. Mention context versus candidate descriptions.
9. A simple ranking score and its tunable weight.
10. Missing entities versus low-confidence abstention.
11. Gold-mention linking isolates the linking component.
12. Predicted-mention linking measures the whole system.
13. Error propagation and the experiment table.
14. Extension: embeddings or candidate-constrained LLM ranking.

### Lab specification

Use a frozen local KB of roughly 30–50 teaching entities. This is a proposed resource to author, not a dataset already found in the folders. Include repeated aliases, multiple aliases per entity, same-type ambiguous candidates, and people or organizations absent from the KB. Use local IDs such as `ORG_01`, clearly distinguished from real Wikidata identifiers.

KB fields: `entity_id`, `canonical_name`, `aliases`, `type`, `description`. Gold mentions have an `entity_id` or `NIL`. Supply development examples where an in-KB gold entity is missed by exact alias retrieval: an empty candidate set does not prove the entity is absent from the KB.

1. Start with **gold mentions** to isolate NEL.
2. Normalize aliases using a documented policy; retrieve all matching candidates.
3. Rank by an alias-conditioned prior estimated from training mentions. Smooth unseen cases or use a documented uniform fallback. Never estimate priors from test labels.
4. Add context using TF-IDF cosine similarity between the surrounding sentence and candidate descriptions. Fit the vectorizer on training contexts and the fixed KB descriptions; transform development/test contexts without refitting. Compare the combined score with the prior baseline.
5. Use `score(e) = alpha × prior(e | alias) + (1-alpha) × cosine(context, description(e))`. This is a teaching heuristic, not a calibrated posterior. Choose alpha and any rejection thresholds on development data.
6. Return NIL when rejecting all candidates, but preserve a diagnostic reason such as `no_candidates` or `low_score`. Distinguish a system's abstention from the gold fact that the entity is absent from the KB.
7. Repeat with session 1's predicted spans. Keep the KB, ranker and thresholds fixed.

Use lexical context first so students can inspect why scores change. Embedding similarity is an optional replacement experiment, rather than a prerequisite.

### Metrics and worked interpretation

- **Candidate recall@k:** fraction of gold in-KB mentions whose gold ID is in the retrieved top k. Exclude gold NIL mentions from this denominator. Empty candidate lists count as misses.
- **Gold-mention in-KB accuracy:** fraction of all gold in-KB mentions assigned the correct ID. Candidate misses and erroneous NIL predictions count as errors.
- **Conditional ranking accuracy:** accuracy only on mentions whose gold ID was retrieved. Label this diagnostic clearly; it excludes retrieval failures.
- **NIL precision/recall/F1:** treat gold NIL as the positive class, evaluated on gold mentions.
- **End-to-end linking micro precision/recall/F1:** match `(document_id, start, end, entity_id)` for non-NIL links. A wrong ID or boundary produces an FP and an FN. Report typed NER separately; if adding type to the link match, call the metric a stricter typed variant.

Worked numbers, hypothetical: 8 gold in-KB mentions, gold candidate retrieved for 6, correct final links for 5. Candidate recall = 6/8; in-KB accuracy = 5/8; conditional ranking accuracy = 5/6. These answer different questions. Add 2 gold NIL examples and ask students to construct the NIL confusion matrix from actual predictions.

For end-to-end evaluation, also report the number of predicted mentions and the gold/predicted NIL counts. Do not describe gold-mention linking accuracy as end-to-end performance. A comparison of gold versus predicted mentions is an experiment; do not assume their scores simply multiply.

Exit question: If the correct entity never reaches the ranker, can a better ranker fix that example? Expected answer: no, candidate generation must improve.

## 5. Shared practical resources to build next

Recommended preparation scope: 80–120 short constructed documents, with fixed train/development/test splits and several mentions per document. This is small teaching data, not a benchmark supporting broad model claims. Include ambiguous aliases in different contexts, unseen surface forms, entity-free text, multiword organizations and NIL examples. Ensure each split has useful coverage of these cases; record counts instead of assuming that random splitting achieves it.

Keep related or template-derived examples in the same split. Repeated entities across splits are acceptable for the declared known-KB task; hold out some aliases to test generalization. Separate an unseen-entity experiment if desired. Annotation exercises use training examples, not the test set.

Planned files:

- `01-ner.ipynb`: student notebook with short implementation tasks and a results table.
- `02-nel.ipynb`: candidate retrieval, ranking, NIL and pipeline evaluation.
- Separate instructor solution notebooks with executed outputs.
- `data/train.jsonl`, `dev.jsonl`, `test.jsonl`, and `kb.json`.
- `annotation-guidelines.md`, an environment file and a short run guide.
- Cached model predictions as a fallback when model downloads are unavailable.

Core path should run on CPU without paid APIs. Verify the chosen model installation in the intended classroom environment before teaching. A pretrained NER component does not automatically provide a trained linker for the custom KB: this lab implements its own retrieval and ranking.

Illustrative output record:

```json
{"doc_id":"demo_01","text":"Ada Lovelace visited Atlas Labs in Paris.","mentions":[{"start":0,"end":12,"type":"PERSON","entity_id":"PERSON_01"},{"start":21,"end":31,"type":"ORG","entity_id":"ORG_01"},{"start":35,"end":40,"type":"LOC","entity_id":"LOC_01"}]}
```

These IDs are teaching placeholders, to be defined in the classroom KB. They are not externally verified identifiers.

## 6. Assessment

Pairs submit two notebooks and a short report. Require a baseline/improvement table, a description of the data splits and three errors per session. For each error: show input, gold output, predicted output, stage responsible and one plausible next action. Score the quality of experimental reasoning rather than the highest score.

| Criterion | Weight |
|---|---:|
| Correct task formulation, schema and annotation | 20% |
| Working baseline and controlled improvement | 25% |
| Correct evaluation and leakage prevention | 25% |
| Concrete error analysis and interpretation | 20% |
| Reproducibility and clear explanation | 10% |

Optional LLM comparison: provide the same retrieved candidates and descriptions, ask for one candidate ID or NIL, validate that returned IDs belong to that set, and use the same held-out examples. Record prompt/model/version and malformed outputs. The LLM does not define the gold labels. Keep this optional to avoid API access becoming a course prerequisite.

## 7. Shorter-session adaptation

For two 90-minute sessions, use 25 minutes of concepts, 10 minutes of annotation/worked examples, 45 minutes of guided lab and 10 minutes of discussion in each session. Supply all infrastructure, scoring functions and model predictions. Students change one rule in NER and one context-ranking choice in NEL. Move model training and full reports to homework.

## 8. Source map and further reading

Local materials reviewed:

- `/Users/ema/projects/_courses/ml-course/docs/index.md`: existing course sequence and assessment.
- `/Users/ema/projects/_courses/ml-course/docs/3-Logistic-Regression/02-classification-metrics.ipynb`: metric refresher.
- `/Users/ema/projects/_courses/ml-course/docs/8-Group-Projects/group_project_ml_ai.md`: baseline, controlled improvement and error-analysis pattern.
- `/Users/ema/projects/_courses/ml-course-epfl/lectures/12/lecture12a_text.pdf`: text representations, especially pages 2–9.
- `/Users/ema/projects/_courses/ml-course-epfl/lectures/12/lecture12b_llms.pdf`: transformer recap and tokenizers, especially pages 4 and 8–10.
- `/Users/ema/projects/_courses/ml-course-epfl/labs/ex12/template/ex12.ipynb`: example of progressively stronger baselines, not an IE exercise.

Primary implementation references checked during preparation:

- [spaCy linguistic features](https://spacy.io/usage/linguistic-features): NER and entity-linking concepts and data structures.
- [spaCy EntityLinker](https://spacy.io/api/entitylinker/): linking to KB identifiers and component requirements.
- [spaCy rule-based matching](https://spacy.io/usage/rule-based-matching/): inspectable recognition rules.
- [Hugging Face token-classification guide](https://github.com/huggingface/transformers/blob/main/docs/source/en/tasks/token_classification.md): optional advanced token-classification implementation.

This plan adapts pedagogical structure and proposes new IE content; it does not reproduce the supplied lecture decks.
