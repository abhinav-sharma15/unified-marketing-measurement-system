## Week 1 Completion Update

### Status

Completed

### What I Learned

- Attribution explains customer journeys but does not prove causality.
- Attribution cannot answer whether a conversion would have happened without the campaign or channel.
- Incrementality testing adds causal evidence by comparing treatment outcomes against a counterfactual.
- Geo Lift is useful when user-level randomization is not possible.
- MMM supports budget planning by estimating contribution, ROI, marginal ROI, expected returns, and diminishing returns.
- Lead quality and LTV are important because lead volume alone does not represent business value.
- AI should act as a copilot for interpretation, summarization, test design, and decision support, but it should not replace causal analysis.

### Files Created or Updated

- README.md
- ROADMAP.md
- PROGRESS_LOG.md
- DECISION_LOG.md
- LEARNING_CHECKLIST.md
- docs/00_measurement_philosophy.md
- docs/01_market_landscape.md
- docs/02_ai_measurement_copilot.md

### Confidence Level

Medium

### Work Relevance

High

### Reflection

The key learning from Week 1 is that modern marketing measurement should not rely on one method. Attribution is useful for journey diagnostics, but decision-ready measurement requires causal evidence, budget planning models, value-based lead/customer scoring, and clear governance. The role of AI should be to make this system easier to understand, explain, and use, not to create unsupported causal claims.

### Next Week Focus

Week 2: Design the core marketing data model.

## Week 2

### Phase

Marketing Data Architecture

### Learning Objective

Design the core data model required to support attribution, incrementality testing, Geo Lift, MMM, LTV prediction, and AI-assisted decision-making.

### Build Objective

Create the first version of the marketing measurement data architecture.

### Planned Deliverables

- [ ] docs/01_data_architecture.md
- [ ] Core dimension table list
- [ ] Core fact table list
- [ ] Measurement use case mapping
- [ ] Week 2 reflection

### Key Questions

- Which tables are needed for each measurement method?
- What is the grain of each table?
- Which fields are required?
- Which tables would be hardest to build in a real business?
- What data quality issues could break the system?


Which table is most important for attribution? 2. Which table is most important for Geo Lift? 3. Which table is most important for MMM? 4. Which table is most important for LTV prediction? 5. Which tables would be hardest to build in a real company? 6. What data quality issues could break this measurement system? 7. How would this architecture apply to your current reporting setup?

## Week 2 Reflection

1. The most important table for attribution is `fct_customer_journey` because it captures the ordered sequence of customer touchpoints and enables first-touch, last-touch, assisted, and multi-touch analysis.

2. The most important table for Geo Lift is `fct_geo_market_weekly` because it provides weekly geography-level data needed to compare treatment and control markets.

3. The most important tables for MMM are `fct_ad_spend` and `fct_revenue`, supported by `fct_geo_market_weekly` for geo-level models. MMM needs historical time-series data linking marketing inputs to business outcomes.

4. The most important table for LTV prediction is `fct_revenue`, supported by `fct_leads`, `fct_opportunities`, and `dim_customer`, because LTV requires linking acquisition source to downstream customer value.

5. The hardest tables to build in a real company would be `fct_customer_journey`, `fct_experiment_results`, `fct_ltv_predictions`, and `fct_mmm_outputs` because they require stitching together fragmented systems, identities, experiments, and model outputs.

6. Key data quality risks include inconsistent channel naming, missing campaign IDs, broken UTMs, duplicate leads, unmatched customer IDs, incomplete CRM fields, missing geo data, and revenue not linked back to marketing activity.

7. This architecture could help turn the current reporting setup into a decision-ready measurement system by connecting spend, traffic, leads, pipeline, revenue, experiments, MMM, LTV, and AI-generated recommendations into one governed framework.
### Confidence Level

Not started

### Work Relevance

High

### Next Week Focus

Generate mock marketing datasets.
