import logging

logger = logging
logger.basicConfig(filename="logs.txt", level=logging.INFO)

class GlobalConfig:
	config = { 'window_width': 150 }
	# def __init__():
		# self.config = { 'window_width': 150 }

	@staticmethod
	def get(option):
		return GlobalConfig.config[option] 

	@staticmethod
	def set(option):
		GlobalConfig.config[option['key']] = option['value']
