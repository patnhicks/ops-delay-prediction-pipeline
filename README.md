# ops-delay-prediction-pipeline
## Late Delivery Prediction 

### Overview
This project focuses on predicting delivery delays using large-scale, real-world trasnportation data taken from 
the US Dept of Transportation (DOT) Bureau of Transportation Statistics.  

The goal of the Delay Delivery Prediction project is a decision-support model that identifies operations drivers 
of delay and supports proactive and effective mitigation strategies.  

### Business Problem

Unit of analysis: Individual flight

Target variable: Arrival delay > 15 minutes(?).  This is my initial binary variable and this is a variable included in initial data. 
As I get deeper in EDA, the criteria of this may be updated.

Prediction timing: Prior to take-off

### Data Source
Dataset: https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp

Time Frame: Jan-Jun 2019

### Data Scope: 

Exclusions: These condition will be excluded from analysis. They are typically non-systemic and inherently unpredictable. They will be analyzed during EDA to 
understand their frequencies and impact to determine whether further analysis is warranted.  
- Emergencies, security incidents, extreme (non-seasonal) weather extremes
- Cancellations/diversions

This analysis is focused on operational issues, like traffic congestion, route path and characteristics, carrier behavioras, and origin and destination (OD)
airport patterns.

### Approach

### Project Structure
notebooks/   → EDA and modeling analysis

src/         → reusable functions

reports/     → plots and summaries

data/        → raw and processed datasets

### Insights

### Current Status

