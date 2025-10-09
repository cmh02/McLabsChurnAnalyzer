'''
MCA DataCombine Module
Author: @cmh02

This module will provide a Target Variable Creation pipeline for cross-timestamp data preparation tasks:

For the target variable, we observe the following classes:
- Inactive (0): Player has not been active for either timestamp
- Recovered (1): Player was inactive in t1, but active in t2
- Churned (2): Player was active in t1, but inactive in t2
- Active (3): Player has been active in both timestamps
'''

'''
MODULE/PACKAGE IMPORTS
'''

# Data
import pandas as pd

'''
CLASS DEFINITION
'''

class McaTargetPipeline:
	'''
	MCA Target Variable Creation Class
	'''

	@staticmethod
	def buildTarget(currentDf: pd.DataFrame, futureDf: pd.DataFrame, onlyReturnTarget: bool) -> pd.DataFrame:
		'''
		Build the target variable based on player activity between two timestamps.

		Parameters:
		- currentDf: DataFrame for timestamp 1
		- futureDf: DataFrame for timestamp 2 (the most up-to-date data timestamp)
		'''

		# Merge the two dataframes on 'UUID' column to get activity status at both timestamps
		df = currentDf.merge(futureDf[['UUID', 'active']], on='UUID', how='outer', suffixes=('_t2', '_t3'))

		# Fill missing activity values with 0 (indicating inactivity)
		df['active_t2'] = df['active_t2'].fillna(0)
		df['active_t3'] = df['active_t3'].fillna(0)

		# Derive target variables based on t2 and t3 active status (binary addition)
		df['churn'] = df["active_t2"] * 2 + df["active_t3"]

		# If only the target variable is requested, return that
		if onlyReturnTarget:
			return df[['UUID', 'churn']]

		# Drop activity columns
		df.drop(columns=['active_t2', 'active_t3'], inplace=True)

		# Rename all columns with _t2 suffix to remove the suffix
		df.rename(columns=lambda x: x.replace('_t2', ''), inplace=True)

		# Return the full current dataframe with the target variable
		return df