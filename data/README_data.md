# MCLabs Churn Analyzer: Data Storage

In this directory, there are several different data folders. Each stores the data at a specific point in the project.

| Data Directory                  | Description                                                                                             | Notes                                                   |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [gatheringoutput](gatheringoutput) | Raw output data from gathering skripts.                                                                 | Data files are not published to protect player privacy. |
| [anonoutput](anonoutput)           | All of the data from [gatheringoutput](gatheringoutput) but anynomized (UUID's converted to placeholders). |                                                         |
| [combined](combined/)              | All of the data from [anonoutput](anonoutput) combined into a single CSV file.                             |                                                         |
| [cleaned](cleaned/)                | The data after being passed through several cleaning steps.                                             |                                                         |
| [featurized](featurized/)          | The data after feature derivation (engineering).                                                        |                                                         |
| [targetized](targetized/)          | The data after churn derivation.                                                                        |                                                         |
