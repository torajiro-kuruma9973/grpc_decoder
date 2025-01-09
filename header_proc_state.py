from enum import Enum

class state(Enum):
	IDEL = 0
	DETERMINE_TYPE = 1
	DIRECT_GET = 2                 # name and val can be obtained directly from static tbl
	INSERT_TBL_NEED_NAME_VAL = 4   # name or/and val needs/need to be retrive from the following data
	GET_LEN = 5
	GET_DATA = 6
	CLEAN = 7