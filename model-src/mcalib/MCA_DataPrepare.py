'''
MCA DataPrepare Module
Author: @cmh02

This module will provide a pipeline for data preparation tasks:
- Data Anonymization and Cleaning
- Feature Engineering
- Target Variable Creation
'''


'''
MODULE/PACKAGE IMPORTS
'''

# System
import os
import re
import hashlib
from glob import glob
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Data
import numpy as np
import pandas as pd

# Output/Display
from enum import Enum
from tqdm import tqdm

'''
ENUM DEFINITIONS
'''

class McaOutputMode(Enum):
	NONE = "none"
	PUBLIC = "public"
	PRIVATE = "private"
	FINAL = "final"
	ALL = "all"

class McaStorageMode(Enum):
	NONE = "none"
	INSTANCE = "instance"

class McaHashMode(Enum):
	NONE = "none"
	SHA256 = "sha256"

'''
CLASS DEFINITION
'''

class McaDataPrepare:
	def __init__(self, inputFolderPath: str, outputMode: McaOutputMode=McaOutputMode.ALL, storageMode: McaStorageMode=McaStorageMode.NONE):

		# Save instance configuration
		self.inputFolderPath = inputFolderPath
		self.dataFolderPath = os.path.dirname(os.path.dirname(inputFolderPath))
		self.outputMode = outputMode
		self.storageMode = storageMode

		# Load environment file using python-dotenv
		load_dotenv(dotenv_path="../env/.env")

		# Load environmental variables
		self.MCA_PEPPERKEY = os.getenv("MCA_PEPPERKEY")
		if not self.MCA_PEPPERKEY:
			raise ValueError("Missing required environment variable: MCA_PEPPERKEY")
		
		# If configured, create base dictionary for storing dataframes
		if self.storageMode == McaStorageMode.INSTANCE:
			self.dfdict = {}
		
		# Print our initial configuration
		print(f"A New MCA Data Preparer has been created!")
		print(f"-> Input Folder Path: {self.inputFolderPath}")
		print(f"-> Data Directory Path: {self.dataFolderPath}")
		print(f"-> Output Mode: {self.outputMode}")
		print(f"-> Storage Mode: {self.storageMode}")

	def prepareData(self):

		# Set up intermediate output paths depending on output type
		if self.outputMode in (McaOutputMode.PUBLIC, McaOutputMode.ALL):
			self.anonymizedFolderPath_public = os.path.join(self.dataFolderPath, "anonymized/public/")
			os.makedirs(self.anonymizedFolderPath_public, exist_ok=True)

			self.cleanedFolderPath_public = os.path.join(self.dataFolderPath, "cleaned/public/")
			os.makedirs(self.cleanedFolderPath_public, exist_ok=True)

			self.featurizedFolderPath_public = os.path.join(self.dataFolderPath, "featurized/public/")
			os.makedirs(self.featurizedFolderPath_public, exist_ok=True)
		if self.outputMode in (McaOutputMode.PRIVATE, McaOutputMode.ALL):
			self.anonymizedFolderPath_private = os.path.join(self.dataFolderPath, "anonymized/private/")
			os.makedirs(self.anonymizedFolderPath_private, exist_ok=True)

			self.cleanedFolderPath_private = os.path.join(self.dataFolderPath, "cleaned/private/")
			os.makedirs(self.cleanedFolderPath_private, exist_ok=True)

			self.featurizedFolderPath_private = os.path.join(self.dataFolderPath, "featurized/private/")
			os.makedirs(self.featurizedFolderPath_private, exist_ok=True)

		# Set up output folder path (output folder always gets made)
		self.outputFolderPath_public = os.path.join(self.dataFolderPath, "prepared/public/")
		os.makedirs(self.outputFolderPath_public, exist_ok=True)

		self.outputFolderPath_private = os.path.join(self.dataFolderPath, "prepared/private/")
		os.makedirs(self.outputFolderPath_private, exist_ok=True)

		# Get the names of all input files using glob
		inputDataFiles = glob(os.path.join(self.inputFolderPath, "**", "*.csv"), recursive=True)

		# Iterate through the files
		for filePath in tqdm(iterable=inputDataFiles, desc="Preparing Data Files", unit="file"):

			# Get relative path for input file location
			dataRelativeFilePath = os.path.relpath(filePath, self.inputFolderPath)

			# Read the input CSV file
			df = pd.read_csv(filePath)

			# Anonymize the UUID column (UUID -> hash(PEPPER + UUID))
			df['UUID'] = [hashlib.sha256(f"{self.MCA_PEPPERKEY}:{uuid}".encode()).hexdigest() for uuid in df['UUID']]

			# If configured, create private output path and save dataframe to path
			if self.outputMode in (McaOutputMode.PRIVATE, McaOutputMode.ALL):
				outputFilePath = os.path.join(self.anonymizedFolderPath_private, dataRelativeFilePath)
				os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)
				df.to_csv(outputFilePath, index=False)

			# If configured, create public output path and save dataframe without UUID's to path
			if self.outputMode in (McaOutputMode.PUBLIC, McaOutputMode.ALL):
				outputFilePath = os.path.join(self.anonymizedFolderPath_public, dataRelativeFilePath)
				os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)
				df.drop(columns=['UUID']).to_csv(outputFilePath, index=False)

			# Replace <none> with NULL
			df.replace("<none>", pd.NA, inplace=True)
			df.replace(" <none>", pd.NA, inplace=True)

			# Replace "-" with NULL
			df.replace("-", pd.NA, inplace=True)

			# Fill missing values for other features
			df.fillna({
				"mcmmo_power_level": 0,
				"mcmmo_skill_ACROBATICS": 0,
				"mcmmo_skill_ALCHEMY": 0,
				"mcmmo_skill_ARCHERY": 0,
				"mcmmo_skill_AXES": 0,
				"mcmmo_skill_CROSSBOWS": 0,
				"mcmmo_skill_EXCAVATION": 0,
				"mcmmo_skill_FISHING": 0,
				"mcmmo_skill_HERBALISM": 0,
				"mcmmo_skill_MACES": 0,
				"mcmmo_skill_MINING": 0,
				"mcmmo_skill_REPAIR": 0,
				"mcmmo_skill_SALVAGE": 0,
				"mcmmo_skill_SMELTING": 0,
				"mcmmo_skill_SWORDS": 0,
				"mcmmo_skill_TAMING": 0,
				"mcmmo_skill_TRIDENTS": 0,
				"mcmmo_skill_UNARMED": 0,
				"mcmmo_skill_WOODCUTTING": 0,
				"lw_rev_total": 0,
				"lw_rev_phase": 0,
				"chemrank": 0,
				"policerank": 0,
				"donorrank": 0,
				"goldrank": 0,
				"current_month_votes": 0,
				"plan_player_time_total_raw": 0,
				"plan_player_time_month_raw": 0,
				"plan_player_time_week_raw": 0,
				"plan_player_time_day_raw": 0,
				"plan_player_time_afk_raw": 0,
				"plan_player_latest_session_length_raw": 0,
				"plan_player_favorite_server": "Spawn",
				"plan_player_sessions_count": 1,
				"leaderboard_position_chems_all": 0,
				"leaderboard_position_chems_week": 0,
				"leaderboard_position_police_all": 0,
				"leaderboard_position_police_week": 0,
				"balance": 0
			}, inplace=True)
			
			# Drop players missing a last-seen date
			df.dropna(subset=["plan_player_lastseen"], inplace=True)

			# Convert last seen times into seconds since last seen
			recordingTimestamp = float(os.path.basename(os.path.dirname(filePath)))
			df["plan_player_lastseen"] = df["plan_player_lastseen"].apply(lambda x: self._planDateToSecondsSince(planDateString=x, untilUnixTimeStamp=recordingTimestamp))

			# Remove any extra text from balance column
			df["balance"] = df["balance"].replace({"dollars": "", "dollar": "", "money": "", "Dollars": "", "Dollar": "", "Money": ""}, regex=True)

			# If configured, create private output path and save dataframe to path
			if self.outputMode in (McaOutputMode.PRIVATE, McaOutputMode.ALL):
				outputFilePath = os.path.join(self.cleanedFolderPath_private, dataRelativeFilePath)
				os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)
				df.to_csv(outputFilePath, index=False)

			# If configured, create public output path and save dataframe without UUID's to path
			if self.outputMode in (McaOutputMode.PUBLIC, McaOutputMode.ALL):
				outputFilePath = os.path.join(self.cleanedFolderPath_public, dataRelativeFilePath)
				os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)
				df.drop(columns=['UUID']).to_csv(outputFilePath, index=False)

			# Derived Feature: Relative playtime between total and month (how much of the playtime was this month)
			df["plan_player_relativePlaytime_totalmonth"] = df["plan_player_time_total_raw"].astype(float) / df["plan_player_time_month_raw"].astype(float)

			# Derived Feature: Relative playtime between week and month (how much of the month was this week)
			df["plan_player_relativePlaytime_weekmonth"] = df["plan_player_time_week_raw"].astype(float) / df["plan_player_time_month_raw"].astype(float)

			# Derived Feature: Relative playtime between day and week (how much of the week was this day)
			df["plan_player_relativePlaytime_dayweek"] = df["plan_player_time_day_raw"].astype(float) / df["plan_player_time_week_raw"].astype(float)

			# Fix missing / infinities
			df.replace([np.inf, -np.inf], np.nan, inplace=True)
			df.fillna(0, inplace=True)

			# If configured, create private output path and save dataframe to path
			if self.outputMode in (McaOutputMode.PRIVATE, McaOutputMode.ALL):
				outputFilePath = os.path.join(self.featurizedFolderPath_private, dataRelativeFilePath)
				os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)
				df.to_csv(outputFilePath, index=False)

			# If configured, create public output path and save dataframe without UUID's to path
			if self.outputMode in (McaOutputMode.PUBLIC, McaOutputMode.ALL):
				outputFilePath = os.path.join(self.featurizedFolderPath_public, dataRelativeFilePath)
				os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)
				df.drop(columns=['UUID']).to_csv(outputFilePath, index=False)

			# Create the target variable
			df["churn"] = df["plan_player_lastseen"].apply(lambda x: 1 if x >= 1209600 else 0)

			# If configured, create private output path and save dataframe to path
			if self.outputMode in (McaOutputMode.PRIVATE, McaOutputMode.FINAL, McaOutputMode.ALL):
				outputFilePath = os.path.join(self.outputFolderPath_private, dataRelativeFilePath)
				os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)
				df.to_csv(outputFilePath, index=False)

			# If configured, create public output path and save dataframe without UUID's to path
			if self.outputMode in (McaOutputMode.PUBLIC, McaOutputMode.FINAL, McaOutputMode.ALL):
				outputFilePath = os.path.join(self.outputFolderPath_public, dataRelativeFilePath)
				os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)
				df.drop(columns=['UUID']).to_csv(outputFilePath, index=False)

			# If configured, save the dataframe
			if self.storageMode == McaStorageMode.INSTANCE:
				self.dfdict[recordingTimestamp] = df

	def analyzeData(self, timestamp: int):
		# Check that we have instance storage
		if self.storageMode != McaStorageMode.INSTANCE:
			print(f"Data Analysis is not possible in {self.storageMode} mode.")
		
		# Check that the timestamp exists
		if timestamp not in self.dfdict.keys():
			print(f"No data found for timestamp {timestamp}. Available timestamps: {list(self.dfdict.keys())}")

		# Print analysis for dataframe
		print(f"{self.dfdict[timestamp].drop(columns=['UUID']).describe().T.map(lambda x: f"{x:.4f}")}")

	def _planDateToSecondsSince(self, planDateString: str, untilUnixTimeStamp: int) -> int:
		# Convert the unix timestamp into a datetime object
		untilDateTime = datetime.fromtimestamp(untilUnixTimeStamp)

		# Check if the plan date is in weekday formatting or date formatting
		if re.match(r"^\S+ \S+ \S+ \S+:\S+$", planDateString):
			
			# If we already have date formatting, just parse the string
			planDateTime = datetime.strptime(planDateString, "%b %d %Y %H:%M")

		else:

			# If we have relative day-of-week formatting, then we need to figure out which day it is
			planDateStringSplit = planDateString.split(" ")
			planDayOfWeek = planDateStringSplit[0]
			planTimeOfDay = planDateStringSplit[1]

			# If the day is "Today", then it is really the day before recording
			if planDayOfWeek == "Today":
				planDateTime = untilDateTime - timedelta(days=1)
			
			# If the day is "Yesterday", then it is 2 days before
			elif planDayOfWeek == "Yesterday":
				planDateTime = untilDateTime - timedelta(days=2)

			# If the day is shown as a day-of-the-week, then calc difference + 1
			elif planDayOfWeek in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:

				# Get week of the day as datetime
				planDateTime = datetime.strptime(planDayOfWeek, "%A")

				# Calculate difference in days then add 1 for offset
				relativeDaysPassed = (untilDateTime.weekday() - planDateTime.weekday()) % 7
				planDateTime = untilDateTime - timedelta(days=relativeDaysPassed + 1)

			# Detect incorrect formatting
			else:
				raise ValueError(f"Unrecognized plan date format: {planDateString}")

			# Set the time
			planDateTime = planDateTime.replace(hour=int(planTimeOfDay.split(":")[0]), minute=int(planTimeOfDay.split(":")[1]))

		# Return difference of the two dates in seconds
		return abs(int((planDateTime - untilDateTime).total_seconds()))