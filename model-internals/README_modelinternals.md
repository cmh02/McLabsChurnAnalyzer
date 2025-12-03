# MCLabs Churn Analyzer: Model Internals

This directory contains the internal model states for our pipelines:

| File Name                                                       | Model Name          | Description                                                                                                  |
| --------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------ |
| [MCA_LabelEncoder.pkl](MCA_LabelEncoder.pkl)                       | Label Encoder       | The label encoder used in the pipeline for the target variable (since we re-class to drop inactive samples). |
| [MCA_Pipeline_LogReg.pkl](MCA_Pipeline_LogReg.pkl)                 | Logistic Regression | Basic Logistic Regression model in sci-kit learn.                                                            |
| [MCA_Pipeline_GridSearch_XGB.pkl](MCA_Pipeline_GridSearch_XGB.pkl) | XGBoost             | XGBoost model that uses GridSearchCV for hyperparameter tuning.                                              |

### Using Saved Model Internals

To use a saved version of a model, simply load it using it [JobLib](https://joblib.readthedocs.io/en/stable/):

`loaded_pipeline = load("path_to_pipeline_save")`
