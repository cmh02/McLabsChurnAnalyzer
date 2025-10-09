'''
MCA DataPrepare Module
Author: @cmh02

This module will provide a pipeline for per-timestamp data preparation tasks:
- Data Anonymization and Cleaning
- Feature Engineering
- Active Variable Creation
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

# Custom
from mcalib import McaHashMode

class McaDataUtils:

	@staticmethod
	def analyzeDataFrame(df: pd.DataFrame):
		'''
		Analyze the given DataFrame and print summary statistics.
		'''
		print(f"{df.drop(columns=['UUID']).describe().T.map(lambda x: f"{x:.4f}")}")

	@staticmethod
	def clearUUIDs(df: pd.DataFrame) -> pd.DataFrame:
		'''
		Clear UUIDs from the DataFrame.
		'''
		# Check if UUID column exists
		if 'UUID' not in df.columns:
			raise ValueError("DataFrame does not contain 'UUID' column.")

		# Drop and return the DataFrame without UUIDs
		df.drop(columns=["UUID"], inplace=True)
		return df

	@staticmethod
	def hashUUIDs(df: pd.DataFrame, hashMode: McaHashMode) -> pd.DataFrame:
		'''
		Hash UUIDs in the DataFrame using the specified hash mode.
		'''

		# Check if UUID column exists
		if 'UUID' not in df.columns:
			raise ValueError("DataFrame does not contain 'UUID' column.")

		# Hash the UUIDs based on the specified hash mode and return
		if hashMode == McaHashMode.SHA256:
			df["UUID"] = df["UUID"].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
		elif hashMode == McaHashMode.MD5:
			df["UUID"] = df["UUID"].apply(lambda x: hashlib.md5(x.encode()).hexdigest())
		else:
			raise ValueError(f"Unsupported MCA hash mode: {hashMode}")
		return df
