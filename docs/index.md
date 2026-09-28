<p align="center">
  <img src="./ie_banner.png" width="100%" alt="Turning news documents into structured information">
</p>

## Welcome to the Information Extraction course 🚀

**Course:** Information Extraction — Named Entity Recognition and Linking  
**Instructor:** Emanuela Boros  
**Format:** 1h30 lecture + 3h practical

How can we turn text into structured information? This course introduces the main information extraction tasks and methods, with hands-on work on named entity recognition (NER) and named entity linking (NEL).

Clone [the repository](https://github.com/EmanuelaBoros/ie-course) with `git clone https://github.com/EmanuelaBoros/ie-course.git`. Materials will be added before each session.

---

## Course Modules

| # | Topic | Slides / Materials | Practical | Status |
|--|------|--------------------|----------|----------|
| 1 | Information Extraction & Named Entity Recognition | [📄 Slides](./1-Information-Extraction-and-NER/01-information-extraction.pdf) · [PowerPoint](./1-Information-Extraction-and-NER/01-information-extraction.pptx) | [Module guide](./1-Information-Extraction-and-NER/01.md) | ✅ Slides available; notebook forthcoming |
| 2 | Named Entity Linking & Entity Embeddings | [📄 Shared lecture, slides 61–82](./1-Information-Extraction-and-NER/01-information-extraction.pdf#page=61) | [Module guide](./2-Named-Entity-Linking/02.md) | ✅ Slides available; notebook forthcoming |

The two modules form one 90-minute lecture and one three-hour practical. The 96-slide lecture also includes a comparison with generative AI and a practical briefing.

---

## Course Topics Overview

- Why information extraction matters; extraction versus retrieval
- Entities, coreference, relations, events and temporal information
- Rules, dictionaries, statistical models, neural models and generative extraction
- Annotation policies, mention boundaries, BIO labels and exact-span evaluation
- Candidate generation, disambiguation and NIL entities
- Entity embeddings, bi-encoders, reranking and knowledge graphs
- A controlled comparison between a student algorithm and a generative model

---

## Practical and Evaluation

Build a dictionary-based recognizer and a contextual entity linker. Compare their predictions with a generative model on the same held-out examples and output schema.

| Time | Activity |
|------|----------|
| 0–30 min | Inspect the schema, annotated examples and evaluation code |
| 30–75 min | Build dictionary NER and analyze boundary errors |
| 75–120 min | Implement candidate lookup and contextual NEL |
| 120–155 min | Run a generative baseline and freeze both methods |
| 155–180 min | Evaluate held-out outputs and explain differences |

Deliver code, saved predictions, metrics and a short error analysis. Notebook files, datasets and detailed submission instructions are forthcoming. No grading weights or deadlines have been announced.

---

## Resources

- [Hugging Face: token classification](https://huggingface.co/learn/llm-course/en/chapter7/2)
- [spaCy: rule-based matching](https://spacy.io/usage/rule-based-matching/)
- [BLINK: dense entity retrieval](https://aclanthology.org/2020.emnlp-main.519/)

---

## 💬 Contact

Assist. Prof.: *Emanuela Boros*  
Email: *emanuela.boros@univ-lr.fr*

---

Website structure adapted from the [ML course](https://github.com/USTH-classroom/ml-course). [Template license](./template-license.txt).
