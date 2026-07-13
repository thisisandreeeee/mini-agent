# RAG fixtures

A synthetic document corpus for testing the retrieval-augmented generation (RAG)
tool (see `TODO.md` §5).

## Design goal

Every fact in `docs/` is **fictional and unique** — it describes an invented company,
"Kestrel Analytics", with invented products, codenames, people, dates, and numbers.
None of it exists in the model's training data, so the agent **cannot answer the
evaluation questions from prior knowledge**. A correct answer is only possible if
retrieval actually surfaces the relevant chunk. This makes the fixtures a clean test
of whether RAG is working, rather than of what the base model already knows.

## Contents

- `docs/` — the corpus to ingest, chunk, and embed. Ten interlinked Markdown
  documents about Kestrel Analytics and its Tidepool platform. Facts cross-reference
  each other (e.g. the postmortem relies on a limit defined in the product spec),
  which enables multi-hop retrieval tests.
- `eval.jsonl` — questions with expected answers and the source document(s) that
  contain the evidence. **Do not ingest this file** into the vector store; it is the
  answer key. Fields:
  - `id` — stable question id.
  - `question` — the user query.
  - `expected_answer` — the ground-truth answer.
  - `sources` — the doc(s) that must be retrieved (empty for unanswerable questions).
  - `type` — `single-hop`, `multi-hop`, or `unanswerable`.

## Unanswerable questions

`q13` and `q14` have no supporting evidence in the corpus. They test the "Done"
criterion from `TODO.md`: the agent should decline and cite insufficient evidence
rather than hallucinate an answer.

## Regenerating / extending

Keep new facts unique and internally consistent with the existing docs. Use the
codenames in `docs/glossary.md` so cross-document references stay coherent.
