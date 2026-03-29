# ---------------- IMPORT LIBRARIES ----------------
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import joblib


# ---------------- LOAD DATASET ----------------
df = pd.read_csv("fetal_bw_m1.csv")

print("Dataset Loaded Successfully")
print(df.head())


# ---------------- SPLIT FEATURES ----------------
X = df.drop("BWEIGHT", axis=1)
y = df["BWEIGHT"]


# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ---------------- RANDOM FOREST MODEL ----------------
rf = RandomForestRegressor()
rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)
rf_score = r2_score(y_test, rf_pred)

print("Accuracy of Random Forest:", round(rf_score * 100, 2), "%")


# ---------------- LINEAR REGRESSION ----------------
lr = LinearRegression()
lr.fit(X_train, y_train)

lr_pred = lr.predict(X_test)
lr_score = r2_score(y_test, lr_pred)

print("Accuracy of Linear Regression:", round(lr_score * 100, 2), "%")


# ---------------- SAVE BEST MODEL ----------------
joblib.dump(rf, "final_pickle_model.pk1")

print("Model Saved Successfully as final_pickle_model.pk1")
