from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess
from testagent import TA_error

def run_test_log(parser):
	"""
	test FTVMTA log feature
	"""
	preprocess.preprocess(parser)
	Assert.test(parser)
	