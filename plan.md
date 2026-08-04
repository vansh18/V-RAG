# Build plan: adversarial verification RAG pipeline

**Timeline:** ~14 days, part-time
**Goal:** A working demo + eval numbers you can put on a resume and defend in an interview

---

## Day 1-2: Domain, data, and baseline setup

**Tasks**
- Pick your domain (medical guidelines, legal precedent, or financial reports — pick one with genuine contradiction over time)
- Collect 15-30 source documents. Deliberately include documents that disagree or supersede each other (e.g. an old guideline + its 2022 update)
- Set up your project repo structure: `/ingest`, `/agents`, `/eval`, `/app`
- Chunk documents (500-800 tokens, with overlap) and embed them into a vector store (Chroma or Qdrant — both are free and local)
- Tag each chunk with metadata: source name, publish date. **Date metadata is important** — your prosecutor will need it later to prefer newer evidence

**Deliverable:** A vector store you can query and get back real chunks with source + date.

---

## Day 3-4: Baseline RAG (get this working end-to-end first)

**Tasks**
- Build a plain retrieve → generate pipeline: query → top-k chunks → LLM answers with citations
- No agents yet. Just confirm the fundamentals work.
- Write 10 test questions by hand and sanity-check the answers

**Deliverable:** A working baseline you can compare everything else against. This is also your fallback demo if the agentic version breaks near the deadline.

---

## Day 5-6: Responder agent

**Tasks**
- Formalize the responder as its own function/class: takes `(query, chunks, objections=None)` → returns `(answer, cited_claims)`
- Prompt it to output structured claims alongside the answer (a list of the specific factual assertions it made) — the prosecutor needs these to attack individually
- Add the revision path: if `objections` is passed in, the prompt must explicitly instruct it to address each one

**Deliverable:** Responder agent that can both draft and revise.

---

## Day 7-8: Prosecutor agent (the core differentiator — spend real time here)

**Tasks**
- Take the claims list from the responder
- For each claim, generate an adversarial retrieval query (e.g. "evidence contradicting: aspirin recommended for primary prevention in adults 50+")
- Run these against your vector store — this is a *separate* retrieval call from the responder's original one
- Prompt the prosecutor to compare the new chunks against the claim and output structured objections: `{claim, contradicting_chunk, explanation}`
- Filter weak objections — an LLM will sometimes flag irrelevant nitpicks, so add a step where the prosecutor rates its own objection's severity (this will matter for your judge)

**Deliverable:** Prosecutor agent that reliably surfaces real contradictions on your test set, and mostly stays quiet when there's nothing to contest (test this — an over-eager prosecutor is a known failure mode you should be able to describe).

---

## Day 9: Judge agent + orchestration loop

**Tasks**
- Judge takes `(draft_answer, objections)` → outputs `verdict: accept/revise` + `confidence score`
- Write the orchestration loop: responder → prosecutor → judge → (if revise) responder again, capped at 3 rounds
- Log every round: what changed, what objection triggered it, how long it took

**Deliverable:** The full loop running end-to-end on a handful of queries, with visible round-by-round logs.

---

## Day 10-11: Evaluation harness

**Tasks**
- Build ~30 test questions in two buckets:
  - **Trap questions** — where the "obvious" answer from older/single-source retrieval is actually outdated or wrong
  - **Clean questions** — where the naive answer is already correct (tests false-positive revision rate)
- For each, hand-label the correct answer
- Run both baseline RAG and your full pipeline against all 30, score accuracy
- Record: accuracy (baseline vs. pipeline), average rounds to convergence, latency, % of trap questions caught, % of clean questions wrongly revised

**Deliverable:** A results table. This is the single most important artifact for your resume — it turns "I built an agent" into "I built an agent and proved it works."

---

## Day 12-13: Demo UI

**Tasks**
- Simple Streamlit or Gradio app (don't overbuild this)
- Show: the question box, then a live trace of each round (draft → objection → verdict), then the final answer with citations
- This trace view is what makes the project memorable in an interview — reviewers remember demos, not READMEs

**Deliverable:** A working, presentable demo.

---

## Day 14: Documentation and polish

**Tasks**
- README with: architecture diagram, the eval results table, and a "failure modes I found" section (e.g. the over-eager prosecutor issue)
- Push to GitHub with a clean commit history
- Write your resume bullet using the real numbers from your eval, e.g.:
  *"Built a multi-agent RAG verification pipeline where an adversarial agent retrieves contradicting evidence against draft answers; reduced factual error rate by X% over baseline RAG on a 30-question eval, at a Yx latency cost."*

---

## Stack recommendation
- **LLM:** Claude or GPT-4 class model via API
- **Vector store:** Chroma (simplest) or Qdrant (more production-like)
- **Orchestration:** Hand-rolled Python loop (more impressive than a framework) or LangGraph if you want the visual graph
- **Demo:** Streamlit
- **Eval:** Plain Python script + a results CSV — no need for a fancy eval framework at this scale

## The one thing not to skip
The eval harness (days 10-11). Without before/after numbers, this is "an agent that talks to itself" in an interview. With numbers, it's evidence you can design and measure an ML system — which is the actual skill being hired for.