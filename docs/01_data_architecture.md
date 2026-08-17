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

## Dimension Tables


## dim_date

Creates a consistent calendar layer for daily, weekly, monthly, quarterly, and yearly analysis.

date_id
date
week_start_date
month
quarter
year
day_of_week
is_weekend
is_holiday
fiscal_week
fiscal_month
fiscal_quarter
fiscal_year

## dim_channel
Standardizes channel naming across platforms and reporting systems.

channel_id
channel_name
channel_group
channel_type
is_paid
is_owned
is_earned
is_offline
is_brand
is_performance
default_measurement_method

## dim_campaign
Stores campaign metadata and connects spend, traffic, leads, and revenue.

campaign_id
campaign_name
platform_campaign_id
channel_id
campaign_type
objective
region
country
start_date
end_date
target_audience
funnel_stage
product_focus
budget_owner

## dim_customer
Represents known leads, accounts, customers, or users.

customer_id
account_id
lead_id
email_hash
created_date
country
region
industry
company_size_band
customer_type
acquisition_channel
first_campaign_id
is_customer
customer_start_date

## dim_geo
Provides geography hierarchy for Geo Lift, MMM, regional reporting, and market-level analysis.

geo_id
country
region
market
city
dma_or_area
timezone
population_band
sales_region
is_test_eligible

## dim_product
Connects marketing activity to product lines or product families.

product_id
product_name
product_family
product_type
subscription_flag
average_order_value
gross_margin_band

## dim_experiment
Stores metadata for experiments and causal tests.

experiment_id
experiment_name
test_type
channel_id
campaign_id
hypothesis
primary_metric
secondary_metric
start_date
end_date
owner
status
confidence_threshold
decision_rule

## Fact tables

## fct_ad_spend
Stores daily media spend and delivery metrics.
One row per date, campaign, channel, geo, and platform.

date
campaign_id
channel_id
geo_id
platform
spend
impressions
clicks
video_views
reach
frequency
currency

## fct_web_sessions
Stores website sessions and traffic source information.
One row per website session.

session_id
customer_id
anonymous_user_id
date
timestamp
channel_id
campaign_id
source
medium
landing_page
device_type
country
geo_id
is_new_visitor
session_duration_seconds
page_views
converted_flag

## fct_leads
Stores lead creation and lead source information.
One row per lead.

lead_id
customer_id
created_date
channel_id
campaign_id
source
medium
geo_id
industry
company_size_band
lead_score_initial
lead_status
mql_flag
sql_flag
sales_owner

## fct_opportunities
Stores sales opportunity creation and pipeline progression.
One row per opportunity.

opportunity_id
lead_id
customer_id
created_date
close_date
stage
pipeline_value
expected_value
closed_won_flag
closed_lost_flag
loss_reason
sales_cycle_days
product_id

## fct_revenue
Stores orders, subscriptions, closed-won revenue, or transactions.
One row per revenue transaction or closed-won booking.

revenue_id
customer_id
opportunity_id
date
product_id
geo_id
revenue_amount
gross_margin
currency
new_or_existing_customer
subscription_flag
billing_period

## fct_customer_journey
Stores ordered customer journey touchpoints.
One row per customer touchpoint.

journey_event_id
customer_id
session_id
event_timestamp
event_date
touchpoint_sequence
channel_id
campaign_id
source
medium
event_type
landing_page
conversion_flag
revenue_id

## fct_geo_market_weekly
Aggregates weekly performance by geography.
One row per geo and week.

week_start_date
geo_id
channel_id
spend
impressions
clicks
sessions
leads
orders
revenue
baseline_revenue
promotion_flag
seasonality_index
competitor_event_flag

## fct_experiment_results
Stores results from A/B tests, Geo Lift tests, holdouts, and other causal analyses.
One row per experiment result.

experiment_id
test_type
channel_id
campaign_id
geo_id
start_date
end_date
primary_metric
baseline_value
treatment_value
control_value
absolute_lift
relative_lift_pct
incremental_conversions
incremental_revenue
incremental_ltv
spend
incremental_roi
confidence_level
p_value
credible_interval_lower
credible_interval_upper
result_summary
decision

## fct_mmm_outputs
Stores MMM outputs by channel, time period, and model version.
One row per channel, time period, and model version.

model_version
period_start_date
period_end_date
channel_id
contribution_revenue
contribution_pct
roi
marginal_roi
saturation_level
recommended_spend
current_spend
spend_change_recommendation
confidence_lower
confidence_upper
model_notes

## fct_ltv_predictions
Stores predicted lead quality, expected revenue, and expected LTV.
One row per lead, customer, or account prediction.

prediction_id
lead_id
customer_id
prediction_date
model_version
lead_quality_score
probability_mql
probability_sql
probability_closed_won
expected_revenue
expected_ltv
ltv_band
top_positive_drivers
top_negative_drivers

## fct_decision_recommendations
Stores final measurement recommendations generated by the decision engine or AI copilot.
One row per channel, campaign, or decision event.

recommendation_id
recommendation_date
channel_id
campaign_id
decision_scope
attribution_signal
incrementality_signal
mmm_signal
ltv_signal
overall_confidence
recommended_action
reasoning_summary
risk_flags
next_best_action
owner
status


## Measurement Use Case Mapping

### Attribution

Required tables:

- fct_web_sessions
- fct_customer_journey
- fct_leads
- fct_revenue
- dim_channel
- dim_campaign
- dim_customer

Main outputs:

- First-touch attribution
- Last-touch attribution
- Assisted conversions
- Journey paths
- Channel credit allocation

### Incrementality Testing

Required tables:

- dim_experiment
- fct_experiment_results
- fct_ad_spend
- fct_revenue
- fct_leads
- dim_channel
- dim_campaign

Main outputs:

- Incremental conversions
- Incremental revenue
- Lift percentage
- Confidence level
- Test decision

### Geo Lift

Required tables:

- dim_geo
- fct_geo_market_weekly
- dim_experiment
- fct_experiment_results

Main outputs:

- Treatment/control comparison
- Difference-in-differences estimate
- Geo-level incremental revenue
- Geo test recommendation

### MMM

Required tables:

- fct_ad_spend
- fct_revenue
- fct_geo_market_weekly
- dim_channel
- dim_campaign
- fct_experiment_results
- fct_mmm_outputs

Main outputs:

- Channel contribution
- ROI
- Marginal ROI
- Saturation
- Recommended spend

### Lead Quality and LTV

Required tables:

- fct_leads
- fct_opportunities
- fct_revenue
- dim_customer
- dim_campaign
- dim_channel
- fct_ltv_predictions

Main outputs:

- Lead quality score
- Expected revenue
- Expected LTV
- Channel quality comparison

### AI Measurement Copilot

Required tables:

- fct_experiment_results
- fct_mmm_outputs
- fct_ltv_predictions
- fct_decision_recommendations
- fct_ad_spend
- fct_revenue
- fct_customer_journey

Main outputs:

- Evidence summaries
- Decision explanations
- Experiment design suggestions
- Risk flags
- Next best action

## Conceptual Architecture

```text
Raw Data Sources
     |
     v
Staging Layer
     |
     v
Intermediate Models
     |
     v
Marketing Measurement Marts
     |
     v
Measurement Methods
     |
     v
Decision Engine
     |
     v
AI Measurement Copilot
