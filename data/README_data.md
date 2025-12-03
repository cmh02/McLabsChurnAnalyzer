# MCLabs Churn Analyzer: Data Storage

In the current version of the project, the data directory only contains subdirectories:

| Data Directory                  | Description                                       | Notes                                                                                                                                                                                                                     |
| ------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [gatheringoutput](gatheringoutput) | Raw output data from gathering skripts.           | Data files are not published to protect player privacy.                                                                                                                                                                   |
| [master](master/)                  | The data after anonymization and concatenization. | Master dataset containing all of the data from[gatheringoutput](gatheringoutput) after cleaning, feature engineering, target derivation, and concatenization. All data is anonymized by removing the UUID for each sample.  |
