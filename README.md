# DS 4320 Project 2: Predicting Country-Level Temperature Anomalies

## Executive Summary

This repository contains the full implementation of a machine learning pipeline to predict annual surface temperature anomalies for 10 countries across 6 continents using historical climate data from Berkeley Earth. The data was ingested from Berkeley Earth's publicly available Amazon S3 storage, parsed, and stored in a MongoDB Atlas document database containing 23,267 documents. An XGBoost regression model was trained on features including year, month, monthly temperature anomaly, measurement uncertainty, and country, achieving a test R² of 0.74 and a mean absolute error of 0.24°C. The repository includes the data ingestion script, MongoDB sanity checks, the full analysis pipeline, a press release, and complete metadata documentation.

**Name:** Stefan Regalia

**NetID:** xtm9px

**DOI:** [10.5281/zenodo.19798275](https://doi.org/10.5281/zenodo.19798275)

**Press Release:** [press_release.md](press_release.md)

**Pipeline:** [pipeline.ipynb](code/pipeline.ipynb)

**License:** [MIT LICENSE](LICENSE)

## Repository Structure

DS4320-project2-temperature-anomaly-prediction/
├── code/
│   ├── ingestion.py          # Data ingestion script
│   ├── mongosh_sanity-check.js  # MongoDB sanity checks
│   ├── pipeline.ipynb        # Analysis and modeling pipeline
│   └── pipeline.md           # Pipeline saved as markdown
├── visualizations/
│   └── actual_vs_predicted.png  # Visualization
├── press_release.md          # Project press release
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
└── .gitignore                # Git ignore rules


## Problem Definition

**Initial General Problem**: As human greenhouse gas emissions have increased over the years, global temperatures have risen, leading to unpredictable natural disasters, loss of habitat for wildlife, droughts, famine, and many more consequences. Forecasting these temperature changes is critical for preparing vulnerable regions for the effects of global warming.

**Refined Specific Problem**: Using historical monthly surface temperature anomaly records from 1750 to 2020 for 10 countries across 6 continents, can we predict the annual temperature anomaly (deviation from the 1951–1980 baseline in degrees Celsius) using year, month, monthly temperature anomalies (how much one month deviated from the 1951-1980 average), and monthly anomaly uncertainty (the 95% confidence interval on the identified anomalies).

The motivation behind this project is to predict annual temperature anomalies for a range of countries so that countries in all areas of the world can mitigate major consequences as a result of global warming. By predicting temperature anomalies for 10 countries across 6 different continents, we can identify the most vulnerable regions, as each region has a diverse climate and global warming trends vary across regions. Therefore, policymakers, humanitarian organizations, and infrastructure planners can further understand how to allocate resources and design strategies for adaptation for the most vulnerable regions. By building a regression model on historical surface temperature anomaly records, this project aims to make country-level global warming trends quantifiable and comparable.

The general problem of forecasting global climate change was refined to focus on predicting annual temperature anomalies for 10 countries across 6 different continents. Specifically, the 10 countries, United States, Canada, Russia, Germany, Brazil, Nigeria, Egypt, India, China, and Australia were selected to represent North America, Europe, Asia, South America, Africa, and Oceania. There are many dimensions of climate change to focus on, such as carbon emissions, sea level rise, and increases in wildfire rates, but temperature anomalies were chosen as the target because rising temperatures are the underlying driver of many of these consequences. The 10 countries were selected to represent diverse climates and geographic regions, allowing for meaningful comparison of warming trends across the globe. Year and month were chosen as features because they capture the long-term warming trend and seasonal patterns, respectively. Monthly temperature anomaly was included because it captures how much temperatures in a given month deviated from historical trends, providing a direct measure of short-term warming. Monthly anomaly uncertainty was included because it reflects how reliably that deviation was measured, as earlier records have higher uncertainty due to sparse weather station coverage and modern records are more precise, allowing the model to account for varying data quality across time.

[Machine Learning Model Predicts Country-Level Temperature Anomalies Across the Globe](press_release.md)

## Domain Exposition

| Term | Description |
|---|---|
| Annual Temperature Anomaly (Target) | The deviation of a country's annual surface temperature from the 1951–1980 baseline average, measured in degrees Celsius |
| Year (Predictor) | Calendar year of the observation, captures the long-term warming trend |
| Month (Predictor) | Calendar month of the observation (1–12), captures seasonal patterns |
| Monthly Temperature Anomaly (Predictor) | How much a given month's temperature deviated from the 1951–1980 average for that same month, in degrees Celsius |
| Monthly Anomaly Uncertainty (Predictor) | The 95% confidence interval on the monthly anomaly measurement, in degrees Celsius |
| Country (Predictor) | The country for which the temperature anomaly is recorded |
| Baseline Period  | The 1951–1980 reference window used to compute all anomalies |
| GMST | Global Mean Surface Temperature, the average of all land and ocean surface temperatures worldwide |
| Radiative Forcing | The change in energy flux in the atmosphere caused by greenhouse gases, measured in W/m² |
| IPCC | Intergovernmental Panel on Climate Change, the UN body that synthesizes global climate science |
| Regression | A machine learning task that predicts a continuous numerical value |
| R² Score (KPI) | Measures how well the model explains variance in the target variable, ranges from 0 to 1 |
| RMSE (KPI) | Root Mean Squared Error, measures average prediction error in degrees Celsius |
| MAE (KPI) | Mean Absolute Error, measures average absolute prediction error in degrees Celsius |

This project lives at the intersection of the environmental science and data science domains. Environmental science is the study of the Earth's natural systems and how human activity impacts them. Climate change, often caused by human greenhouse gas emissions, is one of the most common consequences of this human impact, and temperature anomalies are a popular metric used by institutions such as NASA, NOAA, and Berkeley Earth to measure and track global warming over time. The domain of data science contributes the machine learning techniques, regression analysis in this instance, to identify patterns in historical temperature records and predict future trends. Together, these domains allow us to move from simply observing climate change to quantifying and forecasting it at the country level.

[Link to OneDrive Folder with Background Readings](https://myuva-my.sharepoint.com/:f:/g/personal/xtm9px_virginia_edu/IgBnQlPYhRMyTqUWdBzYjEF_AfB0bYVMzNCpYq6PGUmdtmc?e=TlEmHN)

| Title | Description | Link |
|---|---|---|
| Summary of Findings (Berkeley Earth) | Overview of Berkeley Earth's methodology and key findings on global land surface temperature trends over 250 years | [Link to reading](https://myuva-my.sharepoint.com/personal/xtm9px_virginia_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings%2FSummary%20of%20Findings%20%2D%20Berkeley%20Earth%2Epdf&parent=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings&ga=1) |
| Climate Change: Global Temperature (NOAA) | Explains how temperature anomalies are measured, why warming is uneven across regions, and future temperature projections | [Link to reading](https://myuva-my.sharepoint.com/personal/xtm9px_virginia_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings%2FClimate%20change%5F%20global%20temperature%20%5F%20NOAA%20Climate%2Egov%2Epdf&parent=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings&ga=1) |
| Global Temperature Report for 2025 (Berkeley Earth) | Most recent annual temperature analysis including country-level trends and the accelerating rate of warming | [Link to reading](https://myuva-my.sharepoint.com/personal/xtm9px_virginia_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings%2FGlobal%20Temperature%20Report%20for%202025%20%2D%20Berkeley%20Earth%2Epdf&parent=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings&ga=1) |
| Temperature Change Statistics 1961–2024 (FAO) | Country-level warming statistics for 198 countries, including the 10 countries in this project | [Link to reading](https://myuva-my.sharepoint.com/personal/xtm9px_virginia_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings%2FTemperature%20change%20statistics%201961%E2%80%932024%2E%20Global%2C%20regional%20and%20country%20trends%2Epdf&parent=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings&ga=1) |
| Global Warming of 1.5°C (IPCC) | A report on regional climate change impacts, warming thresholds, and consequences for vulnerable regions | [Link to reading](https://myuva-my.sharepoint.com/personal/xtm9px_virginia_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings%2FGlobal%20Warming%20of%201%2E5%20%C2%BAC%20%E2%80%94%2Epdf&parent=%2Fpersonal%2Fxtm9px%5Fvirginia%5Fedu%2FDocuments%2FDesign%20Project%202%20Readings&ga=1) |

## Data Creation

The data used in this project was accessed from Berkeley Earth, a non-profit organization that provides historical temperature data from over 39,000 weather station records across different continents. Berkeley Earth processes raw station observations, adjusts records to account for station relocations and equipment changes, and then computes regional temperature anomalies relative to the 1951–1980 baseline period. The data used in this project was accessed programmatically from Berkeley Earth's publicly available Amazon S3 storage, where temperature trend files for every country are hosted in plain-text format. Each file contains monthly temperature anomaly records for a single country, spanning from 1750 to 2020, along with uncertainty estimates representing the 95% confidence interval for each measurement.

For this project, data was collected for 10 countries. These countries are the United States, Canada, Russia, Germany, Brazil, Nigeria, Egypt, India, China, and Australia. These countries were selected to represent 6 continents and diverse climate regions. A Python script fetched each country's file using an HTTP request, parsed the whitespace-delimited records, converted NaN values to null, and inserted the resulting documents into a MongoDB Atlas collection. Each document represents one monthly observation for one country, resulting in a total of 23,267 documents in the database.

| File | Description | Link |
|---|---|---|
| `ingestion.py` | Fetches monthly temperature anomaly data for 10 countries from Berkeley Earth, parses each file into structured documents, and inserts them into MongoDB Atlas | [Data ingestion file](https://github.com/stefanregalia/DS4320-project2-temperature-anomaly-prediction/blob/main/code/ingestion.py) |

Several sources of bias are present in this dataset. First, geographic and
socioeconomic bias exists because Berkeley Earth computes temperature anomalies by aggregating weather station records. This means that wealthier, more developed nations with denser station networks have lower uncertainty and more reliable records. Countries with sparse station coverage, particularly in Africa and parts of Asia, may have higher uncertainty values and may underrepresent true warming trends in these regions. Second, temporal bias is introduced by earlier years in the dataset, where station coverage was extremely limited worldwide. Records from the 1700s and early 1800s are based on only a handful of stations, making anomaly estimates for those periods far less reliable than modern records. This means the model may learn different relationships from early records versus modern ones due to the differences in data quality across time. Lastly, sampling bias is introduced by the selection of only 10 countries, which do not fully represent all climate regions, warming projections, and geographic contexts worldwide, potentially limiting the generalizability of the model's predictions.

Several strategies can be used to handle the biases mentioned above. Geographic and socioeconomic bias can be mitigated by including monthly anomaly uncertainty as a feature in the model, allowing it to down-weight observations from regions and time periods with high uncertainty. This also mitigates temporal bias, as it will down-weight observations from older time periods, as they tend to have more uncertainty. Sampling bias from the 10-country selection can be acknowledged as a limitation of the project scope. The 10 countries were  selected to represent 6 continents and diverse climate regions, which partially mitigates this bias, but conclusions drawn from the model should not be generalized beyond the countries included in the dataset.

Several critical decisions were made during the data acquisition process that introduce or mitigate uncertainty. First, the choice to use Berkeley Earth as the sole data source was made because it provides the most comprehensive historical temperature records available, spanning over 250 years and incorporating over 39,000 weather stations. However, relying on a single source means that any systematic biases in Berkeley Earth's methodology are carried through to the model. Second, the decision to include all records regardless of year, including early records from the 1700s and 1800s with high uncertainty, was made to maximize the historical depth of the dataset. This introduces uncertainty in early records but allows the model to learn long-term warming trends. Third, NaN values in the dataset were converted to null on ingestion and stored as such in MongoDB. During model training, any row containing a null value in any column will be dropped, ensuring the model only trains on complete, reliable observations. This reduces the risk of introducing artificial values through imputation, but also reduces the amount of training data available, particularly for earlier records where smoothed anomaly columns are more likely to be null. Finally, the 0.2 second delay between HTTP requests was included to avoid overloading Berkeley Earth's servers.

## Metadata

The following guidelines define the expected structure for documents in the `temperature_anomalies` collection in MongoDB.

- Every document must contain the fields `country`, `year`, `month`,
  `monthly_anomaly_c`, and `monthly_anomaly_unc_c` as these are always
  present in the source data and are required for model training.
- `annual_anomaly_c` and `annual_anomaly_unc_c` should be present but may
  be null for early records where insufficient data exists.
- `five_year_anomaly_c`, `five_year_unc_c`, `ten_year_anomaly_c`,
  `ten_year_unc_c`, `twenty_year_anomaly_c`, and `twenty_year_unc_c` are
  expected to be null for most early records and should be stored as null
  rather than omitted.
- `country` must be a lowercase hyphenated string matching the Berkeley
  Earth file naming convention (e.g. `"united-states"`, not `"United States"`).
- `year` and `month` must be integers. `month` must be between 1 and 12.
- All anomaly and uncertainty values must be stored as floats in degrees
  Celsius, or null if not available.
- `baseline`, `source`, and `source_url` must be present in every document
  for provenance tracking.
- No two documents may share the same `country`, `year`, and `month`
  combination, enforced by a unique index on these three fields.
- Not all fields are used as features in the model. The fields
  used for training are `country`, `year`, `month`, `monthly_anomaly_c`,
  and `monthly_anomaly_unc_c`, with `annual_anomaly_c` as the target
  variable. All other fields are retained in the database for completeness
  and potential future use.

  | Collection | Stored In | Documents | Countries | Year Range | Features | Description |
|---|---|---|---|---|---|---|
| temperature_anomalies | MongoDB Atlas | 23,267 | 10 | 1750–2020 | 15 | Monthly surface temperature anomaly records for 10 countries across 6 continents, sourced from Berkeley Earth. Each document represents one monthly observation for one country, including anomaly values at monthly, annual, 5-year, 10-year, and 20-year smoothing levels along with uncertainty estimates for each. |

| Feature | Data Type | Description | Example |
|---|---|---|---|
| `country` | String | Lowercase hyphenated country name matching Berkeley Earth file naming convention | `"united-states"` |
| `year` | Integer | Calendar year of the observation | `2020` |
| `month` | Integer | Calendar month of the observation (1–12) | `6` |
| `monthly_anomaly_c` | Float | Deviation of the monthly surface temperature from the 1951–1980 average for that same month, in degrees Celsius | `1.186` |
| `monthly_anomaly_unc_c` | Float | 95% confidence interval on the monthly anomaly measurement, in degrees Celsius | `0.243` |
| `annual_anomaly_c` | Float | 12-month smoothed average anomaly centered on the given month, in degrees Celsius. Target variable for the regression model. | `1.021` |
| `annual_anomaly_unc_c` | Float | 95% confidence interval on the annual anomaly, in degrees Celsius | `0.212` |
| `five_year_anomaly_c` | Float | 5-year smoothed average anomaly, in degrees Celsius | `0.981` |
| `five_year_unc_c` | Float | 95% confidence interval on the 5-year anomaly, in degrees Celsius | `0.189` |
| `ten_year_anomaly_c` | Float | 10-year smoothed average anomaly, in degrees Celsius | `0.950` |
| `ten_year_unc_c` | Float | 95% confidence interval on the 10-year anomaly, in degrees Celsius | `0.174` |
| `twenty_year_anomaly_c` | Float | 20-year smoothed average anomaly, in degrees Celsius | `0.912` |
| `twenty_year_unc_c` | Float | 95% confidence interval on the 20-year anomaly, in degrees Celsius | `0.163` |
| `baseline` | String | Reference period used to compute all anomalies | `"1951-1980"` |
| `source` | String | Organization that produced the data | `"Berkeley Earth"` |
| `source_url` | String | Direct URL to the source file for this country | `"https://berkeley-earth-temperature.s3..."` |

| Feature | Min | Max | Mean | Std Dev | Null Count | Uncertainty Source |
|---|---|---|---|---|---|---|
| `monthly_anomaly_c` | -9.599 | 7.578 | -0.029 | 1.250 | 1,602 | Sparse station coverage, especially in early records |
| `monthly_anomaly_unc_c` | 0.039 | 12.169 | 0.726 | 0.925 | 1,602 | Higher in early records (1700s–1800s) due to few weather stations |
| `annual_anomaly_c` | -2.566 | 3.756 | -0.027 | 0.669 | 1,872 | Null for early records lacking sufficient monthly data for smoothing |
| `annual_anomaly_unc_c` | 0.019 | 4.507 | 0.314 | 0.366 | 1,872 | Higher in early records due to sparse station coverage |
| `five_year_anomaly_c` | -1.499 | 2.489 | -0.032 | 0.512 | 2,498 | Null when insufficient preceding months exist |
| `ten_year_anomaly_c` | -1.254 | 2.119 | -0.048 | 0.463 | 2,899 | Null when insufficient preceding months exist |
| `twenty_year_anomaly_c` | -0.927 | 1.731 | -0.070 | 0.402 | 3,875 | Null when insufficient preceding months exist |