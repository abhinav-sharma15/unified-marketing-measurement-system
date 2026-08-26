# Mock Data Dictionary

All files are synthetic and generated with random seed 42. They are for learning and product prototyping only.

## mock_ad_spend_daily.csv
- Rows: 43,860
- Grain/fields: date, channel_id, channel_name, campaign_id, campaign_name, geo_id, market, platform, spend_gbp, impressions, clicks, reach, video_views, currency

## mock_customer_ltv.csv
- Rows: 239
- Grain/fields: customer_id, lead_id, acquisition_channel, acquisition_campaign, customer_start_date, initial_revenue_gbp, renewal_revenue_gbp, expansion_revenue_gbp, total_revenue_gbp, gross_margin_gbp, retention_months, churn_flag, actual_ltv_gbp

## mock_experiments.csv
- Rows: 1
- Grain/fields: experiment_id, experiment_name, test_type, channel_name, hypothesis, primary_metric, start_date, end_date, treatment_markets, control_markets, planned_mde_pct, confidence_threshold, status

## mock_geo_weekly.csv
- Rows: 6,300
- Grain/fields: week_start_date, geo_id, market, channel_id, channel_name, spend_gbp, impressions, clicks, sessions, leads, opportunities, orders, revenue_gbp, baseline_revenue_gbp, promotion_flag, product_launch_flag, seasonality_index, competitor_event_flag, geo_test_id, treatment_flag

## mock_leads.csv
- Rows: 3,989
- Grain/fields: lead_id, customer_id, created_date, first_touch_channel, last_touch_channel, campaign_id, market, industry, company_size_band, product_interest, engagement_score, lead_status, mql_flag, sql_flag

## mock_opportunities.csv
- Rows: 766
- Grain/fields: opportunity_id, lead_id, customer_id, created_date, close_date, product_id, opportunity_stage, pipeline_value_gbp, expected_value_gbp, closed_won_flag, closed_lost_flag, sales_cycle_days, loss_reason

## mock_revenue.csv
- Rows: 239
- Grain/fields: revenue_id, customer_id, opportunity_id, revenue_date, product_id, market, revenue_amount_gbp, gross_margin_gbp, new_existing_customer, billing_type

## mock_web_sessions.csv
- Rows: 66,405
- Grain/fields: session_id, anonymous_user_id, customer_id, session_timestamp, session_date, channel_id, channel_name, campaign_id, source, medium, landing_page, device_type, market, is_new_visitor, page_views, session_duration_seconds, lead_created_flag, conversion_flag
