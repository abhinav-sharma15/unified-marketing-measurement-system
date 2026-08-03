# Roadmap: Unified Marketing Measurement System

## Project Goal

Build a practical, GitHub-managed learning and product prototype that helps move marketing measurement from attribution-led reporting to causal, decision-ready measurement.

## Phase 0: Foundation

### Week 1: Measurement Philosophy and GitHub Setup

Deliverables:

- GitHub repository
- README
- Roadmap
- Progress log
- Measurement philosophy document
- Initial market landscape note
- AI measurement copilot concept

## Phase 1: Marketing Data Architecture

### Week 2: Core Marketing Data Model

Define the entities, tables, and relationships needed for marketing measurement.

### Week 3: Generate Mock Marketing Data

Create realistic mock datasets for spend, sessions, leads, revenue, geo sales, and customer LTV.

### Week 4: SQL Staging Models

Build staging models to clean and standardize source data.

### Week 5: Marketing Mart Design

Create reusable marketing marts for daily spend, customer journeys, funnels, geo markets, and campaign performance.

## Phase 2: Attribution Analysis

### Week 6: First-Touch and Last-Touch Attribution

Build basic attribution models and compare channel credit allocation.

### Week 7: Multi-Touch Attribution

Implement linear, U-shaped, and time-decay attribution.

### Week 8: Markov Attribution

Build a simple Markov chain attribution model and channel removal effect analysis.

### Week 9: Attribution Limitation Case Study

Demonstrate why attribution is useful for diagnostics but not sufficient for budget decisions.

## Phase 3: Incrementality Testing

### Week 10: A/B Testing Foundation

Build a simple randomized experiment analysis.

### Week 11: Power, Sample Size, and MDE

Create an experiment planning calculator.

### Week 12: Difference-in-Differences

Analyze mock treatment and control data.

### Week 13: Geo Lift Testing

Build a practical geo incrementality workflow.

### Week 14: Incrementality Repository

Create a reusable evidence base for experiment results.

## Phase 4: Marketing Mix Modeling

### Week 15: MMM Conceptual Foundation

Document adstock, saturation, response curves, base sales, ROI, and marginal ROI.

### Week 16: Simple MMM From Scratch

Build a basic regression-based MMM using mock weekly data.

### Week 17: Adstock and Saturation

Implement adstock and saturation functions.

### Week 18: Open-Source MMM Tooling Review

Compare Meridian, Robyn, and other MMM approaches.

### Week 19: MMM Calibration With Experiments

Connect incrementality evidence to MMM interpretation.

## Phase 5: Lead Quality and LTV Prediction

### Week 20: Lead Quality Framework

Define lead quality, funnel outcomes, and value-based marketing measurement.

### Week 21: Lead Scoring Model

Build a simple model predicting lead-to-opportunity or opportunity-to-win.

### Week 22: LTV Prediction

Estimate expected revenue or expected customer lifetime value.

## Phase 6: Unified Decision Engine

### Week 23: Measurement Decision Framework

Define which measurement method should be used for which business question.

### Week 24: Budget Decision Engine Prototype

Create a prototype that recommends increase, hold, reduce, or test further.

## Phase 7: AI Measurement Copilot

### Week 25: AI Product Design

Define AI use cases, users, data access, and guardrails.

### Week 26: Prompt Library

Create prompts for attribution interpretation, experiment design, MMM explanation, and budget recommendations.

### Week 27: Measurement Retrieval Prototype

Create a simple retrieval layer across docs, experiment history, and model outputs.

### Week 28: AI Decision Summary Generator

Generate executive summaries from measurement results.

### Week 29: AI Experiment Design Assistant

Generate test plans, hypotheses, metrics, and risk checks.

### Week 30: AI Governance and Guardrails

Document AI limitations, evidence requirements, and decision governance.
