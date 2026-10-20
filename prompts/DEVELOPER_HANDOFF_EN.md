# Reuse the foundation — developer prompt

```text
Continue the existing project at Darrenchih/hvac122-learning-foundation, at the repository root.
Do not rebuild the application or replace its architecture by default.

Read README.md, FOUNDATION.md, AI_HANDOFF.md, CONTRIBUTING.md, and the content-pack schema.
Inspect the actual files and current tests before changing code.

Task: [specific change]
Constraints: offline browser runtime; no accounts, paid APIs, or runtime-generated answers;
Traditional Chinese UI, English questions with optional Chinese translations;
backward-compatible learning records and stable content identifiers.

For content work, modify content packs or authored data sources only.
For behavior changes, make the smallest coherent implementation and add meaningful regression coverage.
Never rewrite a published question under the same ID when its grading-relevant content changes.
Never clear localStorage/IndexedDB, remove user material, alter unrelated projects, or change system security settings.
Do not publish private course documents, answer sheets, credentials, browser profiles, or learning backups.
MIT covers project-authored software/content; it does not grant rights to third-party material.

Run python scripts/run_tests.py and relevant browser checks if supported.
Distinguish PASS, FAIL, BLOCKED, and NOT RUN. Do not claim real-browser or Windows testing from a VM harness.
Provide changed files, rationale, actual test results, compatibility impact, and remaining limitations.
```
