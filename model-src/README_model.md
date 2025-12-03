
# MCLabs Churn Analyzer: Model Source

This document will outline the structure of the codebase for this project. Note that each source code file contains it's own developer documentation, and that this file simply outlines the codebase.

## Interactive Notebooks

There are two notebooks provided in this version of the project:

| Notebook Name  | Notebook Location                                | Notebook Description                                                                                                                                                                                                                            |
| -------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Data Pipeline  | [MCA_DataPipeline.ipynb]()                          | This notebook is used for transforming the raw data files into the final master dataset. This includes all data cleaning, feature engineering, and target derivation steps.                                                                     |
| Model Creation | [ MCA_ModelCreation.ipynb](MCA_ModelCreation.ipynb) | This notebook is used for creating the machine learning model pipelines. It creates two pipelines, one for logistic regression and one for XGBoost. It then evaluates the models, presents the results, and saves the pipelines for future use. |

## Code Submodules


| Submodule Name   | Submodule Location                                   | Submodule Description                                                       |
| ---------------- | ---------------------------------------------------- | --------------------------------------------------------------------------- |
| Data Preparation | [MCA_DataPrepare.py](mcalib/MCA_DataPrepare.py)         | Handles all data preparation steps such as data cleaning and preprocessing. |
| Data Utilities   | [MCA_DataUtils.py](mcalib/MCA_DataUtils.py)             | Provides common utilities for working with data in this project.            |
| Enumerations     | [MCA_Enum.py](mcalib/MCA_Enum.py)                       | Central location for all enums used in this project.                        |
| Feature Pipeline | [MCA_FeaturePipeline.py](mcalib/MCA_FeaturePipeline.py) | Defines the feature pipeline for creating features across two datasets.     |
| Target Pipeline  | [MCA_TargetPipeline.py](mcalib/MCA_TargetPipeline.py)   | Defines the target pipeline for deriving the target across two datasets.    |
