'''
MCA DataPrepare Module
Author: @cmh02

This module will provide a pipeline for per-timestamp data preparation tasks:
- Data Anonymization and Cleaning
- Feature Engineering
- Active Variable Creation
'''

'''
ENUM DEFINITIONS
'''
from enum import Enum

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