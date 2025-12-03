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
import hashlib
from dotenv import load_dotenv

# Data
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
		
		# Get hash pepper from env
		load_dotenv()
		hashPepper = os.getenv("MCA_PEPPERKEY", "")
		if hashPepper is None or hashPepper == "":
			raise ValueError("MCA_PEPPERKEY environment variable is not set.")

		# Hash the UUIDs based on the specified hash mode and return
		if hashMode == McaHashMode.SHA256:
			df["UUID"] = df["UUID"].apply(lambda x: hashlib.sha256((x + hashPepper).encode()).hexdigest())
		elif hashMode == McaHashMode.MD5:
			df["UUID"] = df["UUID"].apply(lambda x: hashlib.md5((x + hashPepper).encode()).hexdigest())
		else:
			raise ValueError(f"Unsupported MCA hash mode: {hashMode}")
		return df
	
	@staticmethod
	def getDfForTimestamp(timestamp: float, dataDir: str=f"../data/gatheringoutput") -> pd.DataFrame:
		'''
		Load and return the DataFrame for a given playerdata timestamp.
		'''

		# Construct file path
		filePath = os.path.join(dataDir, f"{timestamp}/PlayerData.csv")

		# Check if file exists
		if not os.path.exists(filePath):
			raise FileNotFoundError(f"Playerdata file not found at path: {filePath}")

		# Load and return the DataFrame
		df = pd.read_csv(filePath)
		return df
