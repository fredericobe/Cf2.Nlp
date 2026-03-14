# Cf2.Nlp

Cf2.Nlp is a Python natural language matching library focused on **intent detection**, **entity extraction**, and **context-aware conversation flow** for Portuguese-language text.

The repository contains:

- A core NLP engine (`Nlp/`) that models intents, training phrases, entities, and runtime matching.
- A REST API layer (`NlpApi/`) with MongoDB persistence helpers.
- Automated tests for both the core and API layers (`NlpTests/`, `NlpApiTests/`).
- A legacy implementation (`v0/`) kept for historical reference.

---

## What this library does

At a high level, the library lets you:

1. Define a **Memory** with Intents and Entities.
2. Train a **Brain** with example phrases (`Brain.Learn()`).
3. Send user input and retrieve the **most probable intent** (`Brain.GetMostProbableIntent(...)`).
4. Fill mandatory parameters/entities and generate responses.
5. Restrict intent matching using input/output conversational contexts.

The main matching pipeline is:

- Tokenization (including special handling for URL/email/date patterns).
- Stemming (RSLP stemmer, Portuguese-oriented).
- Stopword/special-char removal.
- Conversion into a sentence corpus (terms + matched entities).
- Intent scoring by corpus overlap.

---

## Core concepts (domain model)

### Brain

`Brain` is the orchestrator. It receives a `WordProcess` instance and a `Memory` instance, learns intent corpora, and performs intent selection at runtime.

Important responsibilities:

- Learning all intents via `Learn()`.
- Context handling (`addCurrentContext`, `clearContexts`, `getCurrentContexts`).
- Intent ranking via `GetMostProbableIntent(sentence)`.
- Accuracy threshold control via `AccuracyFactor`.

### Memory

`Memory` stores:

- Intents (`GetIntents`, `AddIntent`)
- Entities (`GetEntities`, `AddEntity`)

It also resolves runtime entities with `FindEntity(word)`.

### Intent

An `Intent` contains:

- Training phrases.
- Responses.
- Optional input/output contexts.
- Extracted parameters (`Parameters`) and completion state (`Completed`).

During learning, each phrase is resolved and merged into an intent-level corpus. During matching, the intent computes a score and tries to resolve mandatory parameters.

### Phrase and parameters

Training phrases can include entity placeholders like:

```text
quero comprar uma pizza de {entity:{name:pizza}}
```

The phrase parser rewrites placeholders to internal tokens (e.g., `__pizza_1__`) and builds parameter metadata. During runtime, matched entities populate `actualValue` and `resolvedValue`.

### Entities and synonyms

Entity resolution supports two strategies:

- `Entity` + `Synonym` collections (semantic groups with stemming-based matching).
- `RegExpEntity` for regex-based dynamic entities.

### Sentence

`Sentence` represents user input transformed into a normalized corpus. It resolves each token into either:

- `type="term"` (stemmed lexical term), or
- `type="entity"` (when `Memory.FindEntity` matches an entity).

---

## Repository structure

### `Nlp/` (main library)

Main modules:

- `brain.py`: learning and intent selection engine.
- `intent.py`: intent model, corpus scoring, parameter completion, response selection.
- `phrase.py`: phrase parsing, entity markers, corpus generation.
- `sentence.py`: runtime user-input normalization and entity lookup.
- `memory.py`: in-memory repository for intents/entities.
- `entities.py`, `synonym.py`, `regExpEntity.py`: entity modeling and resolution.
- `wordProcess.py`: tokenization, stemming, stopword/special-char removal.
- `jsonConvert.py`: custom object <-> JSON mapper.

### `NlpTests/` (unit tests for the core)

Covers:

- Brain learning and scoring behavior.
- Context-driven intent filtering.
- Parameter fulfillment flows.
- Phrase entity parsing.
- Word processing/tokenization rules.
- JSON conversion behavior.

These tests are also the best practical examples of how to instantiate and use the engine.

### `NlpApi/` (REST + persistence layer)

Contains:

- Flask-RESTful API resources (`brainApi.py`).
- MongoDB repository (`brainRepository.py`).
- Mongo-backed memory implementation (`mongoMemory.py`).
- Additional API stubs (`entityApi.py`, `intentApi.py`, `match.py`, `nlpservice.py`) that are partially implemented.

### `NlpApiTests/` (API/persistence tests)

Includes:

- API resource tests with mocked repositories.
- Mongo-backed CRUD and memory lifecycle tests.

### `v0/` (legacy version)

Historical version of the library with older architecture and tests (`v0/Cf2.Nlp`, `v0/Cf2.Nlp.Tests`). Useful for archaeology/comparison, but not the primary implementation path.

### Solution/project files

- `Nlp.sln`: Visual Studio solution grouping all projects.
- `*.pyproj`: Python Tools for Visual Studio project metadata.

---

## Requirements

This codebase is Python-based and depends on a few runtime libraries:

- `nltk`
- `flask`
- `flask-restful`
- `pymongo`
- `mongoengine`
- `bson` (provided by `pymongo`)

Suggested installation:

```bash
pip install nltk flask flask-restful pymongo mongoengine
```

NLTK resources required by the tokenizer/stemmer/stopwords pipeline:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('rslp')"
```

If these corpora are missing, tests and runtime preprocessing may fail.

---

## Quick start (library usage)

Below is a minimal example based on repository test patterns.

```python
import sys
sys.path.append('Nlp')

from brain import Brain
from wordProcess import WordProcess
from memory import Memory
from intent import Intent
from entities import Entity
from synonym import Synonym

# 1) Build memory
memory = Memory()
word = WordProcess()

# 2) Define an entity
pizza = Entity()
pizza.Name = "pizza"

s1 = Synonym(word)
s1.setPrincipal("calabreza")
pizza.Synonymous.append(s1)

s2 = Synonym(word)
s2.setPrincipal("mussarela")
pizza.Synonymous.append(s2)

memory.AddEntity(pizza)

# 3) Define an intent
intent = Intent()
intent.Name = "intent_pizza"
intent.addTrainingPhrase("quero comprar uma pizza de {entity:{name:pizza}}")
intent.addTrainingPhrase("quero comprar uma pizza")
intent.addResponse("Sua pizza será entregue")
memory.AddIntent(intent)

# 4) Train and match
brain = Brain(word, memory)
brain.Learn()

result = brain.GetMostProbableIntent("quero comprar uma pizza de calabreza")
if result["intent"]:
    print(result["intent"].Name)
    print(result["score"])
    print(result["intent"].getResponse())
```

`GetMostProbableIntent(...)` returns a dictionary with at least:

- `intent`: selected intent object (or `None`)
- `score`: score in [0, 1] in current implementation
- `phrase`: selected phrase-scoring metadata

---

## Context-driven conversations

The engine supports context gates:

- Intents with empty `InputContexts` are considered when there is no active context.
- Intents with non-empty `InputContexts` are considered when context exists.
- On successful match, selected intent `OutputContexts` are appended to current context list.

This is useful for multi-turn flows like:

1. User asks to buy something (`comprar`) -> sets context `compra`.
2. Follow-up intent (`compra_fim`) only becomes reachable with `InputContext = compra`.

See `NlpTests/brain_context_test.py` for a complete scenario.

---

## Running tests

From repository root, examples:

```bash
python -m unittest NlpTests.wordProcess_test
python -m unittest NlpTests.brain_context_test
python -m unittest NlpApiTests.apiTest
```

For Mongo-backed tests, ensure MongoDB is running on `localhost:27017`.

---

## Current maturity notes

- Core matching components are implemented and covered by tests.
- Some API files in `NlpApi/` are placeholders or incomplete stubs.
- There is no packaging metadata (`setup.py`/`pyproject.toml`) yet, so usage is source-based (`sys.path` patterns are used throughout tests).
- The solution is strongly oriented to Portuguese preprocessing due to NLTK RSLP and Portuguese stopwords.

---

## Suggested next improvements

If you plan to evolve this repository, high-impact steps include:

1. Add modern Python packaging (`pyproject.toml`) and installable modules.
2. Replace ad-hoc `sys.path` usage with package imports.
3. Finish/clean API endpoints for intent/entity/match operations.
4. Add CI pipeline scripts and dependency lock files.
5. Expand docs with end-to-end API examples and data schemas.

