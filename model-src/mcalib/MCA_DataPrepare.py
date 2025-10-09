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
import re
from datetime import datetime, timedelta

# Data
import numpy as np
import pandas as pd


class McaDataPrepare:
	'''
	MCA Data Preparation Class
	'''

	@staticmethod
	def prepareData(df: pd.DataFrame, dfTimestamp: float) -> pd.DataFrame:
		'''
		General data preparation for a given playerdata timestamp.
		'''

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
		df["plan_player_lastseen"] = df["plan_player_lastseen"].apply(lambda x: McaDataPrepare._planDateToSecondsSince(planDateString=x, untilUnixTimeStamp=dfTimestamp))

		# Remove any extra text from balance column
		df["balance"] = df["balance"].replace({"dollars": "", "dollar": "", "money": "", "Dollars": "", "Dollar": "", "Money": ""}, regex=True)

		# Derived Feature: Relative playtime between total and month (how much of the playtime was this month)
		df["plan_player_relativePlaytime_totalmonth"] = df["plan_player_time_total_raw"].astype(float) / df["plan_player_time_month_raw"].astype(float)

		# Derived Feature: Relative playtime between week and month (how much of the month was this week)
		df["plan_player_relativePlaytime_weekmonth"] = df["plan_player_time_week_raw"].astype(float) / df["plan_player_time_month_raw"].astype(float)

		# Derived Feature: Relative playtime between day and week (how much of the week was this day)
		df["plan_player_relativePlaytime_dayweek"] = df["plan_player_time_day_raw"].astype(float) / df["plan_player_time_week_raw"].astype(float)

		# Fix missing / infinities
		df.replace([np.inf, -np.inf], np.nan, inplace=True)
		df.fillna(0, inplace=True)

		# Create "active" variable (1 if last seen within 14 days, else 0)
		df["active"] = df["plan_player_lastseen"].apply(lambda x: 0 if x >= 1209600 else 1)

		# Return the prepared dataframe
		return df

	@staticmethod
	def _planDateToSecondsSince(planDateString: str, untilUnixTimeStamp: float) -> int:
		'''
		Convert a plan date string into seconds since that date from a given unix timestamp.
		'''

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