"""
ml_workflow.py
No-code ML pipeline: upload CSV → auto-clean → train → evaluate → export.
No manual coding required from the user.
"""

import os
import tempfile
from typing import Optional

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

router = APIRouter(prefix="/ml", tags=["No-Code ML Workflow"])

# In-memory pipeline state (per-process; swap for Redis/DB in production)
_pipeline_state: dict = {
    "step": "idle",
    "uploaded_file": None,
    "cleaned_file": None,
    "target_column": None,
    "results": None,
}

_TEMP_DIR = tempfile.gettempdir()


def _temp_path(filename: str) -> str:
    return os.path.join(_TEMP_DIR, filename)


@router.post("/upload", summary="Upload a CSV dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Accept a CSV file upload. Returns basic statistics:
    row/column counts, column names, and null counts per column.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    contents = await file.read()
    save_path = _temp_path(file.filename)
    with open(save_path, "wb") as f:
        f.write(contents)

    df = pd.read_csv(save_path)

    _pipeline_state["step"] = "uploaded"
    _pipeline_state["uploaded_file"] = file.filename
    _pipeline_state["cleaned_file"] = None
    _pipeline_state["results"] = None

    return {
        "status": "uploaded",
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "null_counts": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "preview": df.head(5).to_dict(orient="records"),
    }


@router.post("/clean", summary="Auto-clean the uploaded dataset")
def clean_dataset(filename: str = Form(...)):
    """
    Auto-clean the specified CSV:
    - Drop columns with > 50% null values
    - Fill numeric nulls with column median
    - Fill categorical nulls with column mode
    Returns cleaned statistics.
    """
    path = _temp_path(filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found. Upload it first via /ml/upload.")

    df = pd.read_csv(path)
    original_shape = df.shape

    # Drop high-null columns
    threshold = 0.5
    null_ratios = df.isnull().mean()
    dropped_cols = null_ratios[null_ratios > threshold].index.tolist()
    df.drop(columns=dropped_cols, inplace=True)

    # Fill remaining nulls
    for col in df.columns:
        if df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col].fillna(df[col].median(), inplace=True)
            else:
                mode_val = df[col].mode()
                df[col].fillna(mode_val[0] if not mode_val.empty else "unknown", inplace=True)

    cleaned_filename = f"cleaned_{filename}"
    cleaned_path = _temp_path(cleaned_filename)
    df.to_csv(cleaned_path, index=False)

    _pipeline_state["step"] = "cleaned"
    _pipeline_state["cleaned_file"] = cleaned_filename

    return {
        "status": "cleaned",
        "original_shape": {"rows": original_shape[0], "columns": original_shape[1]},
        "cleaned_shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "dropped_columns": dropped_cols,
        "remaining_columns": df.columns.tolist(),
        "remaining_nulls": int(df.isnull().sum().sum()),
        "cleaned_filename": cleaned_filename,
    }


@router.post("/train", summary="Train a model on cleaned data")
def train_model(filename: str = Form(...), target_column: str = Form(...)):
    """
    Train a RandomForest model on the cleaned CSV.
    Automatically selects Classifier or Regressor based on target column type.
    Returns accuracy (classifier) or R² score (regressor) and feature importances.
    """
    path = _temp_path(filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

    df = pd.read_csv(path)

    if target_column not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Target column '{target_column}' not found. Available: {df.columns.tolist()}",
        )

    # Encode categorical features
    df_encoded = df.copy()
    label_encoders: dict = {}
    for col in df_encoded.select_dtypes(include="object").columns:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        label_encoders[col] = le

    X = df_encoded.drop(columns=[target_column])
    y = df_encoded[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Choose model type
    unique_ratio = y.nunique() / len(y)
    is_classification = (y.nunique() <= 20) or (unique_ratio < 0.05)

    if is_classification:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        score = round(accuracy_score(y_test, preds) * 100, 2)
        metric_name = "accuracy_percent"
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        score = round(r2_score(y_test, preds), 4)
        metric_name = "r2_score"

    importances = dict(
        sorted(
            zip(X.columns.tolist(), [round(float(i), 4) for i in model.feature_importances_]),
            key=lambda x: x[1],
            reverse=True,
        )
    )

    _pipeline_state["step"] = "trained"
    _pipeline_state["target_column"] = target_column
    _pipeline_state["results"] = {
        "model_type": "RandomForestClassifier" if is_classification else "RandomForestRegressor",
        metric_name: score,
        "feature_importances": importances,
    }

    return {
        "status": "trained",
        "model_type": "RandomForestClassifier" if is_classification else "RandomForestRegressor",
        "target_column": target_column,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        metric_name: score,
        "feature_importances": importances,
    }


@router.get("/status", summary="Current pipeline step and results")
def get_status():
    """Return the current ML pipeline state and any stored results."""
    return {
        "pipeline_step": _pipeline_state["step"],
        "uploaded_file": _pipeline_state["uploaded_file"],
        "cleaned_file": _pipeline_state["cleaned_file"],
        "target_column": _pipeline_state["target_column"],
        "results": _pipeline_state["results"],
    }
