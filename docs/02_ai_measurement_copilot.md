# AI Measurement Copilot

## Purpose

The AI Measurement Copilot is the intelligence and usability layer on top of the Unified Marketing Measurement System.

It does not replace attribution, incrementality testing, MMM, or LTV models.

It helps users interpret results, ask questions, generate summaries, design tests, and make better decisions.

## Core AI Use Cases

### 1. Natural Language Measurement Q&A

Example questions:

- Why did Paid Social revenue increase last month?
- Is Meta actually incremental?
- Why does attribution disagree with MMM?
- Which channel should receive more budget?
- Which campaigns generate low-quality leads?

### 2. Evidence Triangulation

The copilot compares signals from:

- Attribution
- Incrementality testing
- Geo Lift
- MMM
- Lead quality
- LTV

Example output:

Paid Social has strong attribution performance, but incrementality evidence is weak and marginal ROI is declining. Recommendation: hold budget and run a follow-up Geo Lift test.

### 3. Experiment Design Assistant

The copilot can help design:

- A/B tests
- Geo Lift tests
- Holdout tests
- Difference-in-differences analyses
- Synthetic control tests

It should generate:

- Hypothesis
- Primary metric
- Secondary metrics
- Treatment group
- Control group
- Required pre-period
- Test duration
- Risks
- Readout template

### 4. MMM Interpretation Assistant

The copilot explains:

- Adstock
- Saturation
- Response curves
- Contribution
- ROI
- Marginal ROI
- Budget optimization results

Example:

Paid Search has high average ROI but low marginal ROI, which suggests it may be close to saturation. YouTube has lower current ROI but higher marginal ROI, which suggests it may have more room to scale.

### 5. Decision Recommendation Agent

The copilot recommends:

- Increase
- Hold
- Reduce
- Test further
- Investigate data quality
- Improve targeting

Recommendations must include:

- Evidence used
- Confidence level
- Reasoning
- Risk flags
- Suggested next action

### 6. Automated Documentation

The copilot helps create:

- Experiment readouts
- Decision logs
- Executive summaries
- Monthly measurement review notes
- Model interpretation notes
- Assumption logs

## Guardrails

The AI copilot must follow these rules:

- Do not claim causality from attribution alone.
- Do not recommend major budget increases without causal or MMM evidence.
- Clearly distinguish attribution, incrementality, MMM, and LTV evidence.
- Flag weak or conflicting evidence.
- Show assumptions.
- Recommend testing when evidence is insufficient.
- Always include confidence level and next best action.

## Final Vision

The AI Measurement Copilot should help convert technical measurement outputs into business-ready decisions.

It should answer:

- What happened?
- What likely caused it?
- Which evidence is strongest?
- What should we do next?
- What should we test?
- What should we not over-interpret?
