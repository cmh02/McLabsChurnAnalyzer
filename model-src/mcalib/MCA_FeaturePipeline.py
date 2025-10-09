'''
MCA DataCombine Module
Author: @cmh02

This module will provide a Feature Engineering pipeline for cross-timestamp data preparation tasks:
'''

'''
MODULE/PACKAGE IMPORTS
'''

# Data
import numpy as np
import pandas as pd

'''
CLASS DEFINITION
'''

class McaFeaturePipeline:
	'''
	MCA Feature Engineering Class
	'''

	@staticmethod
	def combineData(currentDf: pd.DataFrame, previousDf: pd.DataFrame) -> pd.DataFrame:
		'''
		Combine two dataframes from different timestamps into one dataframe with engineered features.

		Parameters:
		- currentDf: DataFrame for timestamp 2 (the most up-to-date data timestamp)
		- previousDf: DataFrame for timestamp 1
		'''

		# Merge the two dataframes on 'UUID' column
		df = currentDf.merge(previousDf, on='UUID', how='outer', suffixes=('_t2', '_t1'))

		# Get change in balance
		df['balance_change'] = np.abs(df['balance_t2'] - df['balance_t1'])

		# Get change in lw metrics
		df['lw_rev_total_change'] = np.abs(df['lw_rev_total_t2'] - df['lw_rev_total_t1'])
		df['lw_rev_phase_change'] = np.abs(df['lw_rev_phase_t2'] - df['lw_rev_phase_t1'])

		# Get change in leaderboard metrics
		df['leaderboard_position_chems_all_change'] = np.abs(df['leaderboard_position_chems_all_t2'] - df['leaderboard_position_chems_all_t1'])
		df['leaderboard_position_chems_week_change'] = np.abs(df['leaderboard_position_chems_week_t2'] - df['leaderboard_position_chems_week_t1'])
		df['leaderboard_position_police_all_change'] = np.abs(df['leaderboard_position_police_all_t2'] - df['leaderboard_position_police_all_t1'])
		df['leaderboard_position_police_week_change'] = np.abs(df['leaderboard_position_police_week_t2'] - df['leaderboard_position_police_week_t1'])

		# Get change in rank metrics
		df['chemrank_change'] = np.abs(df['chemrank_t2'] - df['chemrank_t1'])
		df['policerank_change'] = np.abs(df['policerank_t2'] - df['policerank_t1'])
		df['donorrank_change'] = np.abs(df['donorrank_t2'] - df['donorrank_t1'])
		df['goldrank_change'] = np.abs(df['goldrank_t2'] - df['goldrank_t1'])

		# Drop unneeded columns
		df.drop(columns=['active_t1', 'active_t2'], inplace=True)

		# Drop all columns with _t1 suffix
		t1Cols = [col for col in df.columns if col.endswith('_t1')]
		df.drop(columns=t1Cols, inplace=True)

		# Rename all columns with _t2 suffix to remove the suffix
		df.rename(columns=lambda x: x.replace('_t2', ''), inplace=True)

		# Return the combined dataframe
		return df