# Marketing Data Architecture

## Purpose

This document defines the core data model for the Unified Marketing Measurement System.

The purpose of the data architecture is to create a trusted foundation that supports:

- Attribution diagnostics
- Incrementality testing
- Geo Lift measurement
- Marketing Mix Modeling
- Lead quality scoring
- LTV prediction
- AI-assisted measurement interpretation
- Budget decision recommendations

## Core Design Principle

All measurement methods should connect back to a common set of trusted marketing, customer, revenue, and experiment tables.

The system should avoid having separate disconnected datasets for attribution, MMM, experiments, and reporting.

## Core Measurement Questions

The data model should help answer:

- What did we spend?
- Where did the traffic come from?
- Which campaigns generated sessions, leads, opportunities, and revenue?
- Which channels influenced the customer journey?
- Which geographies were exposed to marketing treatment?
- Which campaigns or channels were tested?
- What was the incremental impact?
- What is the MMM-estimated contribution and marginal ROI?
- Which leads or customers have higher expected value?
- What action should be recommended: increase, hold, reduce, or test further?
