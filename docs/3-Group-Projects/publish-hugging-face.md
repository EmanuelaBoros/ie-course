# Share your NER + NEL project on Hugging Face 🤗

Publishing is an **optional final step**, after evaluation. A reproducible release lets other students inspect and reuse your work. You do not need to train a large model or pay for hosted inference.

## 1. Join the L3i community

Create a [Hugging Face account](https://huggingface.co/join), then visit [L3i++ (`l3ipp`)](https://huggingface.co/l3ipp) and select **Request to join this org**. Identify yourself as an IE course student and give your group name if the request form allows it; otherwise send your username to the instructor.

Membership requests need approval. Membership does not necessarily grant repository write access. Start in your personal namespace; coordinate with the instructor before creating or updating a repository under `l3ipp`.

For an example of a research model release, explore [Emanuela Boros's historical NEL model](https://huggingface.co/emanuelaboros/historical-nel). Read its model card, intended task and license; it is a reference, not a required classroom dependency.

## 2. Choose what to release

| Your project | Suitable release |
|---|---|
| Fine-tuned NER or NEL model | Model repository with weights, configuration, tokenizer and model card |
| Dictionary + contextual linking pipeline | Custom pipeline repository with code, gazetteer, permitted KB snapshot, configuration and documentation; describe it accurately as rule-based |
| Prompt-only comparison with a hosted model | Prompts, evaluation code and results in your project repository; you do not own the provider's model weights |
| Interactive demonstration | Optional Hugging Face Space linked to the code/model repository |

Uploading a custom pipeline does not automatically create a working inference widget. A reproducible local loading example is sufficient. Hosting a demo is optional and separate from uploading files.

## 3. Prepare a small release folder

Copy only files intended for sharing into a new folder, for example:

```text
hf_release/
  README.md             # model/pipeline card
  LICENSE               # license you are entitled to apply
  requirements.txt      # tested dependencies
  predict.py            # your working loading/inference script
  config.json           # types, tokenizer policy, ranking settings
  gazetteer.json        # if your pipeline uses one
  kb.json               # only if redistribution is permitted
  evaluation.json       # measured metrics and split counts
```

For a trained Transformers model, export the actual trained model and tokenizer into this folder:

```python
# Run only if these variables contain your trained model and its tokenizer.
model.save_pretrained("hf_release", safe_serialization=True)
tokenizer.save_pretrained("hf_release")
```

For the classroom dictionary pipeline, export the resources in a JSON-friendly representation and provide the implemented functions in `predict.py`:

```python
import json
from pathlib import Path

folder = Path("hf_release")
folder.mkdir(exist_ok=True)
# Use your FINAL PROJECT resources, not the classroom toy KB by accident.
(folder / "kb.json").write_text(json.dumps(KB, indent=2), encoding="utf-8")
entries = [{"tokens": list(tokens), "types": sorted(types)}
           for tokens, types in gazetteer.items()]
(folder / "gazetteer.json").write_text(json.dumps(entries, indent=2), encoding="utf-8")
```

These two JSON files are not a complete release: another user also needs your inference implementation, configuration and instructions. Record the fixed KB version because a linking model's IDs depend on it.

Keep credentials, personal data and files you cannot redistribute out of the release. Preserve upstream licenses and attribution; choose a license compatible with any reused model, data and code. Do not label a rule-based system as a trained transformer or imply ownership of a hosted AI model.

## 4. Write the model or pipeline card

The repository's `README.md` is its card. Start with the template below and replace every TODO with your own evidence. Add license metadata only after choosing the correct license. For a compatible standalone NER model, you may add `pipeline_tag: token-classification`; do not use that tag to claim automatic support for an arbitrary NER + NEL pipeline.

````markdown
---
tags:
- information-extraction
- named-entity-recognition
- entity-linking
- student-project
---

# TODO: project name

## System and intended use
TODO: authors, course, language, domain; trained model or rule-based pipeline.
TODO: what the system recognizes and which fixed KB it links to.

## Inputs and outputs
TODO: text/tokenization, PERSON/ORG/LOC policy, half-open spans, IDs and NIL.

## How to run
TODO: tested Python/dependency versions and exact installation instructions.
TODO: one runnable command or code example, with actual expected output.

## Data and development
TODO: sources, reuse conditions, annotation review, document split sizes.
TODO: baseline, single improvement, KB snapshot and any base model.

## Evaluation
TODO: measured NER and end-to-end P/R/F1, linking accuracy, candidate recall,
NIL support/scores and invalid-output rate; include counts and split definition.
TODO: generative comparison model/date/prompts and resource differences.

## Limitations
TODO: three concrete errors, domain/language limits, ambiguous aliases,
missing KB entities and limits of the small test set.

## License, attribution and AI use
TODO: license(s), upstream sources, team contributions and AI assistance.
````

## 5. Upload — choose one route

### Route A: website (no token or coding needed)

1. Sign in and open [New model repository](https://huggingface.co/new).
2. Choose your own account as owner, for example `your-username/ie-group-03`. Use `l3ipp` only with the instructor's agreement and write permission.
3. Choose a suitable license and visibility. A private draft lets you check files first.
4. Open **Files and versions → Add file → Upload files** and upload the reviewed release files. Keep the intended folder structure.
5. Commit the upload, then inspect the model card and file list.
6. When ready to share, change visibility to public in repository settings. Confirm that every file is intended for public release.

### Route B: Python

Install the Hub client in your environment:

```bash
python -m pip install -U huggingface_hub
```

Authenticate interactively with a token from [your token settings](https://huggingface.co/settings/tokens). Give it only the write permissions needed for your repository. Never paste a token into a submitted notebook or commit it to Git.

```python
from huggingface_hub import login, HfApi

login()  # interactive; do not place the token in source code
api = HfApi()
repo_id = "YOUR_USERNAME/ie-group-03"  # replace with your own namespace

api.create_repo(repo_id=repo_id, repo_type="model", private=True, exist_ok=True)
api.upload_folder(
    repo_id=repo_id,
    repo_type="model",
    folder_path="hf_release",  # a reviewed folder, not your whole working directory
    commit_message="Add evaluated NER and NEL project",
)
print(f"https://huggingface.co/{repo_id}")
```

If the repository already exists, check its visibility in settings: `exist_ok=True` does not make an existing public repository private. Review your upload before making a private draft public through the website.

## 6. Verify that someone else can use it

Ask a teammate to download the release in a fresh environment and follow the README. For a custom pipeline, retrieve its files with:

```python
from huggingface_hub import snapshot_download

release_path = snapshot_download(repo_id="YOUR_USERNAME/ie-group-03")
print(release_path)
# Follow your release's documented loading command from this folder.
```

For a compatible Transformers NER model, test loading the tokenizer and `AutoModelForTokenClassification` from the repository ID. For NEL, document and test the actual architecture and candidate/KB dependencies instead of assuming token classification applies.

Record the repository commit revision used for the final results. Downloading is not enough: check a real input, its span offsets and its linked IDs. Public hosting does not itself validate the model or guarantee free inference.

## 7. Add the release to your project submission

Include the Hub URL, release revision and loading example in your project README and final presentation. Share the link with the instructor so the work can be highlighted through L3i++.

If release permissions, model licensing or access prevent publishing, submit the same reproducible package locally and explain why. Publication is encouraged when feasible; it does not replace the required evaluation and error analysis.

## Official references

- [L3i++ organization](https://huggingface.co/l3ipp)
- [Uploading models](https://huggingface.co/docs/hub/models-uploading)
- [Python upload guide](https://huggingface.co/docs/huggingface_hub/guides/upload)
- [Writing model cards](https://huggingface.co/docs/hub/model-cards)
- [Organization membership](https://huggingface.co/docs/hub/organizations-managing)

[⬅ Group project](./group_project_ie_ai.md) · [Course homepage](../index.md)
