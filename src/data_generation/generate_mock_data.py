import os, json, zipfile
import numpy as np
import pandas as pd
from pathlib import Path

SEED=42
rng=np.random.default_rng(SEED)
out=Path('/mnt/data/umm_mock_data_tmp'); out.mkdir(exist_ok=True)

dates=pd.date_range('2024-01-01','2025-12-31',freq='D')
markets=['London','Manchester','Birmingham','Leeds','Bristol','Glasgow','Liverpool','Sheffield','Edinburgh','Cardiff']
market_factor=dict(zip(markets,[1.55,1.10,1.05,.88,.82,.74,.77,.69,.66,.61]))
channels=['Paid Search - Brand','Paid Search - Non-Brand','Paid Social','LinkedIn','YouTube','Display','Email','Organic Search','Direct','Partner','Events']
paid=channels[:6]
ch_id={c:f'CH{idx+1:02d}' for idx,c in enumerate(channels)}
geo_id={m:f'G{idx+1:02d}' for idx,m in enumerate(markets)}
platform={'Paid Search - Brand':'Google Ads','Paid Search - Non-Brand':'Google Ads','Paid Social':'Meta','LinkedIn':'LinkedIn Ads','YouTube':'Google Ads','Display':'DV360'}
base_spend={'Paid Search - Brand':90,'Paid Search - Non-Brand':190,'Paid Social':155,'LinkedIn':125,'YouTube':110,'Display':65}
cpm={'Paid Search - Brand':80,'Paid Search - Non-Brand':65,'Paid Social':10,'LinkedIn':35,'YouTube':12,'Display':5}
ctr={'Paid Search - Brand':.085,'Paid Search - Non-Brand':.045,'Paid Social':.012,'LinkedIn':.008,'YouTube':.006,'Display':.003}
rows=[]
for d in dates:
    season=1+0.12*np.sin(2*np.pi*(d.dayofyear/365.25))+(.12 if d.month in [9,10,11] else 0)-(.20 if d.month==12 else 0)+(.08 if d.month==1 else 0)
    weekday=.75 if d.weekday()>=5 else 1
    for m in markets:
        for c in paid:
            s=base_spend[c]*market_factor[m]*season*weekday*rng.lognormal(0,.18)
            if c=='YouTube' and m in ['Manchester','Leeds','Bristol'] and pd.Timestamp('2025-07-01')<=d<=pd.Timestamp('2025-07-28'): s*=2.5
            impressions=max(1,int(s/cpm[c]*1000*rng.normal(1,.05)))
            clicks=max(0,min(impressions,int(impressions*ctr[c]*rng.normal(1,.12))))
            reach=max(1,min(impressions,int(impressions*rng.uniform(.55,.85))))
            views=int(impressions*rng.uniform(.35,.75)) if c in ['YouTube','Paid Social','Display'] else 0
            rows.append([d,ch_id[c],c,f'CMP_{c[:3].upper().replace(" ","")}_{m[:3].upper()}',f'{c} Always-on {m}',geo_id[m],m,platform[c],round(s,2),impressions,clicks,reach,views,'GBP'])
ad=pd.DataFrame(rows,columns=['date','channel_id','channel_name','campaign_id','campaign_name','geo_id','market','platform','spend_gbp','impressions','clicks','reach','video_views','currency'])
ad.to_csv(out/'mock_ad_spend_daily.csv',index=False)

# sessions with channel-specific behavior
session_rows=[]; lead_rows=[]; opp_rows=[]; rev_rows=[]; ltv_rows=[]
sid=lid=oid=rid=cid=0
all_dates=np.array(dates)
source_medium={
'Paid Search - Brand':('google','cpc_brand'),'Paid Search - Non-Brand':('google','cpc_nonbrand'),'Paid Social':('meta','paid_social'),'LinkedIn':('linkedin','paid_social'),'YouTube':('youtube','video'),'Display':('dv360','display'),'Email':('crm','email'),'Organic Search':('google','organic'),'Direct':('(direct)','none'),'Partner':('partner','referral'),'Events':('event','offline')}
lead_prob={'Paid Search - Brand':.065,'Paid Search - Non-Brand':.041,'Paid Social':.028,'LinkedIn':.045,'YouTube':.015,'Display':.010,'Email':.055,'Organic Search':.047,'Direct':.052,'Partner':.060,'Events':.075}
channel_probs=np.array([.12,.15,.16,.08,.07,.05,.07,.10,.10,.05,.05]); channel_probs/=channel_probs.sum()
industries=['Technology','Professional Services','Manufacturing','Retail','Healthcare','Education']
company_sizes=['1-49','50-249','250-999','1000+']
products=['Remote Access','Remote Support','Enterprise Connectivity','Security Add-on']
for d in dates:
    daily_n=int(95*(.8 if d.weekday()>=5 else 1.0)*(1.12 if d.month in [9,10,11] else 1)*(0.83 if d.month==12 else 1))
    for _ in range(daily_n):
        sid+=1; anon=f'U{rng.integers(1,30000):06d}'; m=rng.choice(markets,p=np.array(list(market_factor.values()))/sum(market_factor.values()))
        c=rng.choice(channels,p=channel_probs); src,med=source_medium[c]
        returning=bool(rng.random()<.43); lp=rng.choice(['/pricing','/enterprise','/solutions','/resources'],p=[.33,.22,.28,.17])
        p_lead=lead_prob[c]*(1.45 if returning else 1)*(1.35 if lp=='/pricing' else 1)
        lead_flag=bool(rng.random()<p_lead); cust=''
        if lead_flag:
            lid+=1; cid+=1; lead_id=f'L{lid:06d}'; cust=f'CU{cid:06d}'
            # quality patterns
            if c=='LinkedIn': size_p=[.08,.22,.34,.36]; engagement=rng.normal(78,10)
            elif c=='Paid Social': size_p=[.42,.34,.17,.07]; engagement=rng.normal(51,14)
            else: size_p=[.24,.34,.25,.17]; engagement=rng.normal(64,13)
            size=rng.choice(company_sizes,p=size_p); engagement=float(np.clip(engagement,5,100))
            mql_p=np.clip(.20+engagement/200+(.12 if c=='LinkedIn' else 0)-(.08 if c=='Paid Social' else 0),.05,.9)
            mql=bool(rng.random()<mql_p); sql=bool(mql and rng.random()<(.55+(.12 if c=='LinkedIn' else 0)-(.10 if c=='Paid Social' else 0)))
            status='SQL' if sql else ('MQL' if mql else 'New')
            lead_rows.append([lead_id,cust,d.date(),c,c,f'CMP_{c[:3].upper().replace(" ","")}_{m[:3].upper()}',m,rng.choice(industries),size,rng.choice(products),round(engagement,1),status,int(mql),int(sql)])
            if sql and rng.random()<.72:
                oid+=1; opp=f'O{oid:06d}'; created=d+pd.Timedelta(days=int(rng.integers(1,15))); cycle=int(rng.integers(20,120)); close=created+pd.Timedelta(days=cycle)
                base_val={'1-49':6000,'50-249':14000,'250-999':30000,'1000+':65000}[size]
                pipe=base_val*rng.lognormal(0,.28)*(1.18 if c=='LinkedIn' else .82 if c=='Paid Social' else 1)
                win_p=.28+(.14 if c=='LinkedIn' else 0)-(.08 if c=='Paid Social' else 0)+(.06 if engagement>75 else 0)
                won=bool(rng.random()<win_p); lost=not won; stage='Closed Won' if won else 'Closed Lost'
                opp_rows.append([opp,lead_id,cust,created.date(),close.date(),rng.choice(products),stage,round(pipe,2),round(pipe*win_p,2),int(won),int(lost),cycle,'' if won else rng.choice(['Budget','No decision','Competitor','Timing'])])
                if won:
                    rid+=1; amount=pipe*rng.uniform(.86,1.08); margin=amount*rng.uniform(.68,.86)
                    rev_rows.append([f'R{rid:06d}',cust,opp,close.date(),rng.choice(products),m,round(amount,2),round(margin,2),'New','Annual'])
                    renewal=amount*rng.uniform(.55,1.25) if rng.random()<.72 else 0
                    expansion=amount*rng.uniform(.05,.4) if rng.random()<.3 else 0
                    total=amount+renewal+expansion; retention=int(rng.integers(8,37)); churn=int(renewal==0)
                    ltv_rows.append([cust,lead_id,c,f'CMP_{c[:3].upper().replace(" ","")}_{m[:3].upper()}',close.date(),round(amount,2),round(renewal,2),round(expansion,2),round(total,2),round(total*rng.uniform(.68,.86),2),retention,churn,round(total,2)])
        session_rows.append([f'S{sid:07d}',anon,cust,pd.Timestamp(d)+pd.Timedelta(minutes=int(rng.integers(0,1440))),d.date(),ch_id[c],c,f'CMP_{c[:3].upper().replace(" ","")}_{m[:3].upper()}',src,med,lp,rng.choice(['Desktop','Mobile','Tablet'],p=[.58,.37,.05]),m,int(returning),int(rng.integers(1,9)),int(rng.integers(20,900)),int(lead_flag),int(lead_flag)])

sessions=pd.DataFrame(session_rows,columns=['session_id','anonymous_user_id','customer_id','session_timestamp','session_date','channel_id','channel_name','campaign_id','source','medium','landing_page','device_type','market','is_new_visitor','page_views','session_duration_seconds','lead_created_flag','conversion_flag'])
# Correct semantic: is_new_visitor
sessions['is_new_visitor']=1-sessions['is_new_visitor']
sessions.to_csv(out/'mock_web_sessions.csv',index=False)
leads=pd.DataFrame(lead_rows,columns=['lead_id','customer_id','created_date','first_touch_channel','last_touch_channel','campaign_id','market','industry','company_size_band','product_interest','engagement_score','lead_status','mql_flag','sql_flag']); leads.to_csv(out/'mock_leads.csv',index=False)
opps=pd.DataFrame(opp_rows,columns=['opportunity_id','lead_id','customer_id','created_date','close_date','product_id','opportunity_stage','pipeline_value_gbp','expected_value_gbp','closed_won_flag','closed_lost_flag','sales_cycle_days','loss_reason']); opps.to_csv(out/'mock_opportunities.csv',index=False)
rev=pd.DataFrame(rev_rows,columns=['revenue_id','customer_id','opportunity_id','revenue_date','product_id','market','revenue_amount_gbp','gross_margin_gbp','new_existing_customer','billing_type']); rev.to_csv(out/'mock_revenue.csv',index=False)
ltv=pd.DataFrame(ltv_rows,columns=['customer_id','lead_id','acquisition_channel','acquisition_campaign','customer_start_date','initial_revenue_gbp','renewal_revenue_gbp','expansion_revenue_gbp','total_revenue_gbp','gross_margin_gbp','retention_months','churn_flag','actual_ltv_gbp']); ltv.to_csv(out/'mock_customer_ltv.csv',index=False)

# Weekly geo-channel aggregation; base revenue independent of marketing plus lagged YouTube and treatment lift
ad['date']=pd.to_datetime(ad['date']); ad['week_start_date']=ad['date']-pd.to_timedelta(ad['date'].dt.weekday,unit='D')
weekly=ad.groupby(['week_start_date','geo_id','market','channel_id','channel_name'],as_index=False).agg(spend_gbp=('spend_gbp','sum'),impressions=('impressions','sum'),clicks=('clicks','sum'))
weekly['sessions']=(weekly['clicks']*rng.uniform(1.0,1.25,len(weekly))).astype(int)
weekly['leads']=(weekly['sessions']*weekly['channel_name'].map(lead_prob)*rng.uniform(.8,1.2,len(weekly))).astype(int)
weekly['opportunities']=(weekly['leads']*rng.uniform(.18,.38,len(weekly))).astype(int)
weekly['orders']=(weekly['opportunities']*rng.uniform(.2,.45,len(weekly))).astype(int)
week_num=pd.to_datetime(weekly['week_start_date']).dt.isocalendar().week.astype(int)
weekly['seasonality_index']=1+.12*np.sin(2*np.pi*week_num/52)
weekly['promotion_flag']=((pd.to_datetime(weekly['week_start_date']).dt.month.isin([3,9])) & (week_num%4==0)).astype(int)
weekly['product_launch_flag']=((pd.to_datetime(weekly['week_start_date'])>=pd.Timestamp('2025-03-03')) & (pd.to_datetime(weekly['week_start_date'])<=pd.Timestamp('2025-03-31'))).astype(int)
weekly['competitor_event_flag']=(rng.random(len(weekly))<.025).astype(int)
weekly['baseline_revenue_gbp']=[18000*market_factor[m]*s*rng.lognormal(0,.07) for m,s in zip(weekly.market,weekly.seasonality_index)]
# channel contribution with saturation
coef={'Paid Search - Brand':8,'Paid Search - Non-Brand':11,'Paid Social':6,'LinkedIn':9,'YouTube':7,'Display':3}
weekly['media_contribution']=[coef[c]*np.sqrt(max(s,0)) for c,s in zip(weekly.channel_name,weekly.spend_gbp)]
weekly['treatment_flag']=((weekly.market.isin(['Manchester','Leeds','Bristol'])) & (weekly.channel_name=='YouTube') & (weekly.week_start_date>=pd.Timestamp('2025-06-30')) & (weekly.week_start_date<=pd.Timestamp('2025-07-28'))).astype(int)
weekly['geo_test_id']=np.where(weekly['treatment_flag']==1,'GEO_YT_001','')
weekly['revenue_gbp']=(weekly['baseline_revenue_gbp']+weekly['media_contribution']+weekly['promotion_flag']*1800+weekly['product_launch_flag']*2400-weekly['competitor_event_flag']*1200)
weekly.loc[weekly.treatment_flag==1,'revenue_gbp']*=1.08
weekly['revenue_gbp']*=rng.lognormal(0,.04,len(weekly))
weekly['revenue_gbp']=weekly['revenue_gbp'].round(2); weekly['baseline_revenue_gbp']=weekly['baseline_revenue_gbp'].round(2); weekly['spend_gbp']=weekly['spend_gbp'].round(2)
weekly[['week_start_date','geo_id','market','channel_id','channel_name','spend_gbp','impressions','clicks','sessions','leads','opportunities','orders','revenue_gbp','baseline_revenue_gbp','promotion_flag','product_launch_flag','seasonality_index','competitor_event_flag','geo_test_id','treatment_flag']].to_csv(out/'mock_geo_weekly.csv',index=False)

exp=pd.DataFrame([['GEO_YT_001','YouTube Regional Incrementality Test','Geo Lift','YouTube','Increasing YouTube investment creates incremental revenue','Weekly revenue','2025-07-01','2025-07-28','Manchester|Leeds|Bristol','Birmingham|Liverpool|Sheffield',7.5,.95,'Completed']],columns=['experiment_id','experiment_name','test_type','channel_name','hypothesis','primary_metric','start_date','end_date','treatment_markets','control_markets','planned_mde_pct','confidence_threshold','status'])
exp.to_csv(out/'mock_experiments.csv',index=False)

# data dictionary and manifest
manifest=[]
for f in sorted(out.glob('*.csv')):
    df=pd.read_csv(f); manifest.append({'file':f.name,'rows':len(df),'columns':len(df.columns),'fields':list(df.columns)})
md=['# Mock Data Dictionary','','All files are synthetic and generated with random seed 42. They are for learning and product prototyping only.','']
for x in manifest:
    md += [f"## {x['file']}",f"- Rows: {x['rows']:,}",f"- Grain/fields: {', '.join(x['fields'])}",'']
(out/'mock_data_dictionary.md').write_text('\n'.join(md))
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))

# assertions
assert (ad.spend_gbp>=0).all() and (ad.clicks<=ad.impressions).all()
assert set(opps.lead_id).issubset(set(leads.lead_id))
assert set(rev.opportunity_id).issubset(set(opps.opportunity_id))
assert set(ltv.customer_id).issubset(set(rev.customer_id))
assert weekly.loc[weekly.treatment_flag==1,'geo_test_id'].eq('GEO_YT_001').all()

zip_path=Path('/mnt/data/umm_week3_mock_datasets.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(out.iterdir()): z.write(f,arcname=f.name)
    z.write('/mnt/data/generate_mock_data.py',arcname='generate_mock_data.py')
print(json.dumps({'zip':str(zip_path),'manifest':manifest},indent=2))
