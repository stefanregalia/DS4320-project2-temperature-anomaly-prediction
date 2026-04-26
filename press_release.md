# Machine Learning Model Predicts Country-Level Temperature Anomalies Across the Globe

## Hook

Every year, temperatures around the world continue to rise, but not equally. Some countries experience gradual increases while others are experiencing warming at an alarming rate, impacting survival methods for billions of people and wildlife.

## Problem Statement

Global surface temperatures have been rising at exponential rates over the last 250 years. The rates of warming vary across regions, however, making certain regions more susceptible to its consequences than others. For example, coastal areas are beginning to deal with increased sea levels and rising tides, whereas dry regions are subject to droughts and famine. By being informed ahead of time about potential years of temperature anomalies, policymakers and the general public can take preventative measures to reduce the consequences of global warming. To start the spread of this information, we analyzed historical temperature anomaly records for 10 countries across 6 continents to predict how annual temperatures will continue to deviate from historical norms.

## Solution Description

Using over 250 years of historical temperature data collected from weather stations across the globe, we built a machine learning model that predicts annual temperature anomalies compared to the 1951-1980 historical baseline for 10 countries across 6 continents, consisting of the United States and Canada (North America), Brazil (South America), Germany and Russia (Europe), Nigeria and Egypt (Africa), India and China (Asia), and Australia (Oceania). The visualization below shows the model's predicted temperature anomalies plotted against the actual recorded values — points that fall along the dashed line represent perfect predictions. The tight clustering of points along this line demonstrates that the model accurately captures warming trends across all 10 countries. The model uses these historical trends to predict future anomalies, giving policymakers, humanitarian organizations, and everyday citizens an accessible tool to understand regional warming and plan accordingly. We urge governments and international organizations to use these findings to prioritize climate adaptation funding for the regions warming fastest.

## Chart

![Actual vs Predicted Annual Temperature Anomalies](visualizations/actual_vs_predicted.png)