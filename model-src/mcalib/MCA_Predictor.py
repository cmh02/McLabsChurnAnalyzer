'''
MCA Predictor Module
Author: @cmh02

This module will provide a pipeline for making predictions on new data using a trained model.
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
from mcalib import McaOutputMode, McaStorageMode, McaHashMode

'''
CLASS DEFINITION
'''

class McaPredictor:
	def __init__(self):
		pass
