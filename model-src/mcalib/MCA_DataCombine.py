'''
MCA DataCombine Module
Author: @cmh02

This module will provide a pipeline for cross-timestamp data preparation tasks:
- Feature Engineering
- Churn Variable Creation

For the target variable, we observe the following classes:
- Inactive (0): Player has not been active for either timestamp
- Active (1): Player has been active in both timestamps
- Recovered (2): Player was inactive in t1, but active in t2
- Churned (3): Player was active in t1, but inactive in t2
- Active (3): Player has been active in both timestamps
'''

'''
MODULE/PACKAGE IMPORTS
'''

# System
import os
import re
import hashlib
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Data
import numpy as np
import pandas as pd

# Output/Display
from enum import Enum

# Custom
from mcalib import McaOutputMode, McaStorageMode

'''
CLASS DEFINITION
'''

class McaDataCombine:
	def __init__(self, inputFilePath1: str, inputFilePath2: str, autoCombine: bool=True, outputMode: McaOutputMode=McaOutputMode.ALL, storageMode: McaStorageMode=McaStorageMode.NONE):

		# Perform checks on input parameters
		if outputMode not in [McaOutputMode.FINAL, McaOutputMode.NONE]:
			raise ValueError(f"Invalid outputMode '{outputMode}' specified. Valid options are: 'final', 'none'.")
		if storageMode not in [McaStorageMode.NONE, McaStorageMode.INSTANCE]:
			raise ValueError(f"Invalid storageMode '{storageMode}' specified. Valid options are: 'none', 'instance'.")

		# Save instance configuration
		self.inputFilePath1 = inputFilePath1
		self.inputFilePath2 = inputFilePath2
		self.outputMode = outputMode
		self.storageMode = storageMode
		self.autoCombine = autoCombine

		# Create directory paths
		self.timestampFolderPath1 = os.path.dirname(self.inputFilePath1)
		self.timestampFolderPath2 = os.path.dirname(self.inputFilePath2)
		self.preparedPrivateFolderPath = os.path.dirname(self.timestampFolderPath1)
		self.preparedFolderPath = os.path.dirname(self.preparedPrivateFolderPath)
		self.dataFolderPath = os.path.dirname(self.preparedFolderPath)
		self.outputFolderPath = os.path.join(self.dataFolderPath, "combined")
		self.outputFolderPathPublic = os.path.join(self.outputFolderPath, "public")
		self.outputFolderPathPrivate = os.path.join(self.outputFolderPath, "private")

		# Create output directories if they do not exist
		os.makedirs(self.outputFolderPathPublic, exist_ok=True)
		os.makedirs(self.outputFolderPathPrivate, exist_ok=True)

		# Print our initial configuration
		print(f"A New MCA Data Combiner has been created!")
		print(f"-> AutoCombine Mode: {autoCombine}")
		print(f"-> Output Mode: {self.outputMode}")
		print(f"-> Storage Mode: {self.storageMode}")
		print(f"-> Input File Path 1: {self.inputFilePath1}")
		print(f"-> Input File Path 2: {self.inputFilePath2}")
		print(f"-> Output Folder Path: {self.outputFolderPath}")
		print(f"-> Public Output Folder Path: {self.outputFolderPathPublic}")
		print(f"-> Private Output Folder Path: {self.outputFolderPathPrivate}")

		# If autoCombine is enabled, run the combineData method
		if self.autoCombine:
			self.combineData()

	def combineData(self):

		# Load the data from the input file paths
		df1 = pd.read_csv(self.inputFilePath1)
		df2 = pd.read_csv(self.inputFilePath2)

		# Merge the two dataframes on 'UUID' column
		self.df = pd.merge(df1, df2, on='UUID', suffixes=('_t1', '_t2'))

		# Get change in balance
		self.df['balance_change'] = np.abs(self.df['balance_t2'] - self.df['balance_t1'])

		# Get change in lw metrics
		self.df['lw_rev_total_change'] = np.abs(self.df['lw_rev_total_t2'] - self.df['lw_rev_total_t1'])
		self.df['lw_rev_phase_change'] = np.abs(self.df['lw_rev_phase_t2'] - self.df['lw_rev_phase_t1'])

		# Get change in leaderboard metrics
		self.df['leaderboard_position_chems_all_change'] = np.abs(self.df['leaderboard_position_chems_all_t2'] - self.df['leaderboard_position_chems_all_t1'])
		self.df['leaderboard_position_chems_week_change'] = np.abs(self.df['leaderboard_position_chems_week_t2'] - self.df['leaderboard_position_chems_week_t1'])
		self.df['leaderboard_position_police_all_change'] = np.abs(self.df['leaderboard_position_police_all_t2'] - self.df['leaderboard_position_police_all_t1'])
		self.df['leaderboard_position_police_week_change'] = np.abs(self.df['leaderboard_position_police_week_t2'] - self.df['leaderboard_position_police_week_t1'])

		# Get change in rank metrics
		self.df['chemrank_change'] = np.abs(self.df['chemrank_t2'] - self.df['chemrank_t1'])
		self.df['policerank_change'] = np.abs(self.df['policerank_t2'] - self.df['policerank_t1'])
		self.df['donorrank_change'] = np.abs(self.df['donorrank_t2'] - self.df['donorrank_t1'])
		self.df['goldrank_change'] = np.abs(self.df['goldrank_t2'] - self.df['goldrank_t1'])

		# Derive target variables based on t1 and t2 active status (binary addition)
		self.df['churn'] = self.df["active_t1"] * 2 + self.df["active_t2"]

		# Drop unneeded columns
		self.df.drop(columns=['active_t1', 'active_t2'], inplace=True)

		# Make public and private output
		if self.outputMode in [McaOutputMode.FINAL, McaOutputMode.ALL]:

			# Create the output file path
			outputFilePathPublic = os.path.join(self.outputFolderPathPublic, "CombinedData.csv")
			outputFilePathPrivate = os.path.join(self.outputFolderPathPrivate, "CombinedData.csv")

			# Save the dataframe to the private output path
			self.df.to_csv(outputFilePathPrivate, index=False)

			# Save the dataframe to the public output path without UUID column
			self.df.drop(columns=['UUID']).to_csv(outputFilePathPublic, index=False)

	def analyzeData(self):
		# Check that we have instance storage
		if self.storageMode != McaStorageMode.INSTANCE:
			print(f"Data Analysis is not possible in {self.storageMode} mode.")

		# Print analysis for dataframe
		print(f"{self.df.drop(columns=['UUID']).describe().T.map(lambda x: f"{x:.4f}")}")
