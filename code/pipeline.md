# Problem Solution Pipeline


```python
import os
import pandas as pd
from pymongo import MongoClient, errors
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment. Check your .env file.")

# Connecting to MongoDB Atlas
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["climate_db"]
    col = db["temperature_anomalies"]
    client.admin.command("ping")
    print("Connected to MongoDB Atlas successfully.")
    print(f"Total documents in collection: {col.count_documents({})}")
except errors.ServerSelectionTimeoutError as e:
    print(f"Could not connect to MongoDB: {e}")
```

    Connected to MongoDB Atlas successfully.
    Total documents in collection: 23267



```python
# Querying MongoDB and loading into a dataframe
cursor = col.find({}, {"_id": 0, "country": 1, "year": 1, "month": 1,
                        "monthly_anomaly_c": 1, "monthly_anomaly_unc_c": 1,
                        "annual_anomaly_c": 1})

df = pd.DataFrame(list(cursor))
print(f"Raw dataframe shape: {df.shape}")
df.head()
```

    Raw dataframe shape: (23267, 6)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country</th>
      <th>year</th>
      <th>month</th>
      <th>annual_anomaly_c</th>
      <th>monthly_anomaly_c</th>
      <th>monthly_anomaly_unc_c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>united-states</td>
      <td>1768</td>
      <td>9</td>
      <td>NaN</td>
      <td>-1.186</td>
      <td>2.432</td>
    </tr>
    <tr>
      <th>1</th>
      <td>united-states</td>
      <td>1768</td>
      <td>10</td>
      <td>NaN</td>
      <td>-1.818</td>
      <td>2.829</td>
    </tr>
    <tr>
      <th>2</th>
      <td>united-states</td>
      <td>1768</td>
      <td>11</td>
      <td>-0.663</td>
      <td>-1.590</td>
      <td>3.599</td>
    </tr>
    <tr>
      <th>3</th>
      <td>united-states</td>
      <td>1768</td>
      <td>12</td>
      <td>-0.429</td>
      <td>-0.978</td>
      <td>4.940</td>
    </tr>
    <tr>
      <th>4</th>
      <td>united-states</td>
      <td>1769</td>
      <td>1</td>
      <td>-0.378</td>
      <td>-0.150</td>
      <td>5.222</td>
    </tr>
  </tbody>
</table>
</div>



## EDA


```python
# Checking for null values
print("Null counts per column:")
print(df.isnull().sum())
print(f"\nTotal rows with at least one null: {df.isnull().any(axis=1).sum()}")
```

    Null counts per column:
    country                     0
    year                        0
    month                       0
    annual_anomaly_c         1872
    monthly_anomaly_c        1602
    monthly_anomaly_unc_c    1602
    dtype: int64
    
    Total rows with at least one null: 1911



```python
# Dropping rows with null values
df_clean = df.dropna()
print(f"Shape after dropping nulls: {df_clean.shape}")
```

    Shape after dropping nulls: (21356, 6)


We drop rows with null values for better analysis performing. We do this instead of imputing the null values so that we do not bias the analysis, as we have sufficient data when dropping all these rows.


```python
# Basic statistics for numerical features
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>month</th>
      <th>annual_anomaly_c</th>
      <th>monthly_anomaly_c</th>
      <th>monthly_anomaly_unc_c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>23267.000000</td>
      <td>23267.000000</td>
      <td>21395.000000</td>
      <td>21665.000000</td>
      <td>21665.00000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1919.074784</td>
      <td>6.503073</td>
      <td>-0.027365</td>
      <td>-0.028934</td>
      <td>0.72646</td>
    </tr>
    <tr>
      <th>std</th>
      <td>62.972203</td>
      <td>3.452024</td>
      <td>0.668628</td>
      <td>1.249675</td>
      <td>0.92533</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1750.000000</td>
      <td>1.000000</td>
      <td>-2.566000</td>
      <td>-9.599000</td>
      <td>0.03900</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1875.000000</td>
      <td>4.000000</td>
      <td>-0.452000</td>
      <td>-0.665000</td>
      <td>0.21100</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1923.000000</td>
      <td>7.000000</td>
      <td>-0.090000</td>
      <td>-0.042000</td>
      <td>0.35300</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1972.000000</td>
      <td>10.000000</td>
      <td>0.330000</td>
      <td>0.621000</td>
      <td>0.90500</td>
    </tr>
    <tr>
      <th>max</th>
      <td>2020.000000</td>
      <td>12.000000</td>
      <td>3.756000</td>
      <td>7.578000</td>
      <td>12.16900</td>
    </tr>
  </tbody>
</table>
</div>




```python
import matplotlib.pyplot as plt
import seaborn as sns

# Distribution of target variable
plt.figure(figsize=(10, 5))
sns.histplot(df["annual_anomaly_c"].dropna(), bins=50, color="steelblue", edgecolor="black")
plt.title("Distribution of Annual Temperature Anomaly (°C)", fontsize=14, fontweight="bold")
plt.xlabel("Annual Temperature Anomaly (°C)", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.axvline(0, color="black", linestyle="--", linewidth=1, label="1951-1980 Baseline")
plt.legend()
plt.tight_layout()
plt.show()
```


    
![png](pipeline_files/pipeline_8_0.png)
    



```python
# Correlation heatmap of features and target
plt.figure(figsize=(8, 6))
sns.heatmap(df_clean[["year", "month", "monthly_anomaly_c", "monthly_anomaly_unc_c", "annual_anomaly_c"]].corr(),
            annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
```


    
![png](pipeline_files/pipeline_9_0.png)
    


We plot the correlation heatmap to identify which variables we expect to best predict our target variable, annual_anomaly _c. This also helps us identify any multicollinearity.

## Data Preprocessing


```python
# One-hot encoding country
df_model = pd.get_dummies(df_clean, columns=["country"], drop_first=True)

# Defining features and target
feature_cols = ["year", "month", "monthly_anomaly_c", "monthly_anomaly_unc_c"] + \
               [col for col in df_model.columns if col.startswith("country_")]

X = df_model[feature_cols]
y = df_model["annual_anomaly_c"]

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"\nFeature columns: {list(X.columns)}")
```

    Features shape: (21356, 13)
    Target shape: (21356,)
    
    Feature columns: ['year', 'month', 'monthly_anomaly_c', 'monthly_anomaly_unc_c', 'country_brazil', 'country_canada', 'country_china', 'country_egypt', 'country_germany', 'country_india', 'country_nigeria', 'country_russia', 'country_united-states']


We one hot encode the only categorical variable, which is country, as the model can only understand numeric values.


```python
# Updated correlation heatmap with one-hot encoded features
plt.figure(figsize=(12, 10))
sns.heatmap(
    df_model[feature_cols + ["annual_anomaly_c"]].corr(),
    annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 8}
)
plt.title("Correlation Heatmap - All Features", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
```


    
![png](pipeline_files/pipeline_14_0.png)
    


We plot a new correlation heatmap since the one-hot encoding process led to the creation of new variables representing country

## Modeling


```python
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Building XGBoost pipeline
xgb_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", XGBRegressor(random_state=42, n_jobs=-1, verbosity=0))
])

# Hyperparameter grid
xgb_param_grid = {
    "model__n_estimators": [100, 200],
    "model__max_depth": [3, 5, 10],
    "model__learning_rate": [0.01, 0.1, 0.3],
    "model__min_child_weight": [1, 5, 10]
}

# Grid search with 5-fold cross validation
xgb_grid_search = GridSearchCV(
    xgb_pipeline,
    xgb_param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1,
    verbose=3
)

xgb_grid_search.fit(X_train, y_train)

print(f"\nBest parameters: {xgb_grid_search.best_params_}")
print(f"Best cross-validation R²: {xgb_grid_search.best_score_:.4f}")
```

    Fitting 5 folds for each of 54 candidates, totalling 270 fits
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.496 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.490 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.496 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.511 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.580 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.490 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.583 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.589 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.496 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.490 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.584 total time=   0.3s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.601 total time=   0.3s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.496 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.490 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.511 total time=   0.3s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.580 total time=   0.4s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.496 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.496 total time=   0.3s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.583 total time=   0.4s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.589 total time=   0.4s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.584 total time=   0.4s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.490 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.601 total time=   0.4s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.490 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.511 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.583 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.601 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.580 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.589 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.529 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.525 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.584 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.528 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.524 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.539 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.614 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.613 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.525 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.529 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.618 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.528 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.616 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.524 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.625 total time=   0.3s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.539 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.529 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.615 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.616 total time=   0.3s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.613 total time=   0.3s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.618 total time=   0.3s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.525 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.528 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.539 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.522 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.612 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.618 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.615 total time=   0.3s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.625 total time=   0.5s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.615 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.625 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.563 total time=   1.3s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.568 total time=   1.5s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.569 total time=   1.4s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.573 total time=   1.4s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.565 total time=   1.5s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.570 total time=   1.1s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.565 total time=   1.1s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.563 total time=   1.3s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.660 total time=   3.0s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.659 total time=   2.9s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.655 total time=   3.0s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.571 total time=   0.7s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.571 total time=   0.8s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.663 total time=   2.4s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.666 total time=   2.5s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.568 total time=   0.6s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.660 total time=   1.4s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.657 total time=   1.3s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.562 total time=   0.7s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.660 total time=   1.4s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.665 total time=   1.4s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.563 total time=   0.6s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.568 total time=   0.7s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.664 total time=   1.5s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.641 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.640 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.652 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.647 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.653 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.569 total time=   0.7s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.661 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.659 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.672 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.640 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.667 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.668 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.641 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.652 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.658 total time=   1.4s
    [CV 4/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.661 total time=   1.6s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.647 total time=   0.6s
    [CV 2/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.653 total time=   1.8s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.654 total time=   0.7s
    [CV 5/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.659 total time=   1.8s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.656 total time=   0.4s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.659 total time=   0.4s
    [CV 3/5] END model__learning_rate=0.01, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.657 total time=   1.9s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.671 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.669 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.640 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.640 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.670 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.652 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.647 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.652 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.658 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.672 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.666 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.660 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.669 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.679 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.686 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.676 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.690 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.681 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.678 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.688 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.695 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.708 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.675 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.696 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.700 total time=   0.3s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.689 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.697 total time=   0.3s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.681 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.692 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.702 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.696 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.680 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.707 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.679 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.684 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.697 total time=   0.3s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.687 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.684 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.698 total time=   0.3s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.700 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.695 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.704 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.692 total time=   0.4s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.724 total time=   0.7s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.713 total time=   0.6s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.719 total time=   0.7s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.726 total time=   0.7s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.720 total time=   0.7s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.718 total time=   0.3s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.711 total time=   0.5s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.711 total time=   0.5s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.712 total time=   1.3s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.725 total time=   1.3s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.720 total time=   1.4s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.725 total time=   1.1s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.718 total time=   1.0s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.721 total time=   1.6s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.730 total time=   1.7s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.723 total time=   1.2s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.716 total time=   0.4s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.703 total time=   0.4s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.710 total time=   0.4s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.710 total time=   1.2s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.710 total time=   1.4s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.715 total time=   0.4s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.726 total time=   1.2s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.667 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.712 total time=   0.4s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.717 total time=   0.8s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.674 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.676 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.680 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=100;, score=0.677 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.681 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.712 total time=   0.6s
    [CV 1/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.721 total time=   0.7s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.687 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.706 total time=   0.7s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.695 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.671 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.687 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.678 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.669 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.717 total time=   0.8s
    [CV 5/5] END model__learning_rate=0.1, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.712 total time=   0.8s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=1, model__n_estimators=200;, score=0.691 total time=   0.3s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.677 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=100;, score=0.679 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.682 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.689 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.684 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.669 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.691 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.669 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=5, model__n_estimators=200;, score=0.694 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.680 total time=   0.1s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.678 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=100;, score=0.675 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.695 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.693 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.689 total time=   0.1s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.681 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.682 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=3, model__min_child_weight=10, model__n_estimators=200;, score=0.688 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.704 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.705 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.713 total time=   0.1s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=100;, score=0.704 total time=   0.1s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.705 total time=   0.3s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.693 total time=   0.2s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.713 total time=   0.3s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.701 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.717 total time=   0.3s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.708 total time=   0.3s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=1, model__n_estimators=200;, score=0.725 total time=   0.4s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.715 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.699 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=100;, score=0.705 total time=   0.4s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.706 total time=   0.3s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.697 total time=   0.2s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.723 total time=   0.3s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.708 total time=   0.3s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.697 total time=   0.2s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.708 total time=   0.4s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.702 total time=   0.1s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.708 total time=   0.2s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=5, model__n_estimators=200;, score=0.708 total time=   0.4s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=100;, score=0.707 total time=   0.2s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.712 total time=   0.6s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.708 total time=   0.6s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.705 total time=   0.7s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.714 total time=   0.6s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=5, model__min_child_weight=10, model__n_estimators=200;, score=0.714 total time=   0.6s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.710 total time=   1.0s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.689 total time=   1.1s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.697 total time=   1.2s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.707 total time=   0.9s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=100;, score=0.716 total time=   1.0s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.706 total time=   0.6s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.699 total time=   0.5s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.694 total time=   0.6s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.709 total time=   1.7s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.697 total time=   1.6s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.686 total time=   1.7s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.712 total time=   0.5s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=100;, score=0.696 total time=   0.6s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.714 total time=   1.7s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=1, model__n_estimators=200;, score=0.709 total time=   1.8s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.702 total time=   0.6s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.689 total time=   0.3s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.703 total time=   1.0s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.702 total time=   0.3s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.690 total time=   1.0s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.690 total time=   1.0s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.697 total time=   1.1s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=5, model__n_estimators=200;, score=0.710 total time=   1.0s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.709 total time=   0.3s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=100;, score=0.697 total time=   0.3s
    [CV 2/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.686 total time=   0.4s
    [CV 1/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.697 total time=   0.5s
    [CV 3/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.694 total time=   0.4s
    [CV 4/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.705 total time=   0.4s
    [CV 5/5] END model__learning_rate=0.3, model__max_depth=10, model__min_child_weight=10, model__n_estimators=200;, score=0.694 total time=   0.4s
    
    Best parameters: {'model__learning_rate': 0.1, 'model__max_depth': 10, 'model__min_child_weight': 1, 'model__n_estimators': 200}
    Best cross-validation R²: 0.7213



```python
# Evaluating best model on test set
best_xgb = xgb_grid_search.best_estimator_
y_pred_xgb = best_xgb.predict(X_test)

mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
rmse_xgb = np.sqrt(mean_squared_error(y_test, y_pred_xgb))
r2_xgb = r2_score(y_test, y_pred_xgb)

print(f"\n=== XGBoost Model Performance ===")
print(f"R²:   {r2_xgb:.4f}")
print(f"MAE:  {mae_xgb:.4f} °C")
print(f"RMSE: {rmse_xgb:.4f} °C")
```

    
    === XGBoost Model Performance ===
    R²:   0.7375
    MAE:  0.2405 °C
    RMSE: 0.3398 °C


### Analysis Rationale

The dataset was split 80/20 into training and test sets using a random split with a fixed random state of 42 for reproducibility. The feature set X consists of year, month, monthly_anomaly_c, and monthly_anomaly_unc_c, along with one-hot encoded country columns to represent each country as an independent binary feature without implying a false numeric ordering. The target variable y is annual_anomaly_c, representing the 12-month smoothed temperature anomaly in degrees Celsius relative to the 1951–1980 baseline. XGBoost was selected as the model because it handles non-linear relationships and feature interactions well, which is important for climate data where warming trends vary significantly across countries and time periods. A scikit-learn pipeline was used to chain StandardScaler and XGBoost into a single object to prevent data leakage by ensuring scaling parameters are learned only from the training data. Hyperparameters were tuned via GridSearchCV across 54 combinations with 5-fold cross-validation to find the optimal balance between model complexity and generalization, yielding best parameters of learning_rate = 0.1, max_depth = 10, min_child_weight = 1, and n_estimators = 200.

The final XGBoost model achieved a test R² of approximately 0.74, MAE of 0.24°C, and RMSE of 0.34°C, with a cross-validation R² of 0.72 confirming strong generalization. The remaining 26% of unexplained variance is likely attributable to missing climate drivers not present in this dataset, such as CO₂ concentration.

## Visualization


```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(y_test, y_pred_xgb, alpha=0.3, s=10, color="steelblue")

# Perfect prediction line
min_val = min(y_test.min(), y_pred_xgb.min())
max_val = max(y_test.max(), y_pred_xgb.max())
ax.plot([min_val, max_val], [min_val, max_val], color="black",
        linewidth=1.5, linestyle="--", label="Perfect Prediction")

# R² annotation
ax.annotate(f"R² = {r2_xgb:.4f}",
            xy=(0.05, 0.92), xycoords="axes fraction",
            fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray"))

# Explanation of R² for a non-technical audience
ax.annotate("R² measures how accurately the model predicts\ntemperature anomalies. A value of 1.0 indicates\na perfect prediction, 0.0 indicates no predictive power.",
            xy=(0.05, 0.78), xycoords="axes fraction",
            fontsize=9, color="gray",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="lightgray"))

ax.set_xlabel("Actual Annual Temperature Anomaly (°C)", fontsize=13)
ax.set_ylabel("Predicted Annual Temperature Anomaly (°C)", fontsize=13)
ax.set_title("Actual vs Predicted Annual Temperature Anomalies",
             fontsize=15, fontweight="bold")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
fig.text(0.99, 0.01, "Source: Berkeley Earth (berkeleyearth.org)",
         ha="right", fontsize=9, color="gray")
plt.tight_layout()
plt.savefig("../visualizations/actual_vs_predicted.png", dpi=300, bbox_inches="tight")
plt.show()
```


    
![png](pipeline_files/pipeline_21_0.png)
    


### Visualization Rationale

An actual vs predicted scatter plot was chosen because it directly and intuitively communicates how well the model performs to both technical and non-technical audiences. Each point represents one monthly observation, with its actual temperature anomaly on the x-axis and the model's predicted value on the y-axis. Points that fall along the dashed perfect prediction line indicate accurate predictions, while points further away represent larger errors. The tight clustering of points along this line confirms that the model is capturing the underlying warming trends well across all 10 countries. The R² annotation was included with a simple explanation to make the model's accuracy immediately interpretable without requiring statistical knowledge.
