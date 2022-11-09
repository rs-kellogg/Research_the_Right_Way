
import unittest
import harvest_helpers
import time

class harvest_helpers(unittest.TestCase):

	def error_kill_switch1(self):
		self.assertEqual('yes', harvest_helpers.error_kill_switch(page_error_counter=0, storage_error_counter=0, content_error_counter=0))
		
	def error_kill_switch2(self):
		self.assertEqual('yes', harvest_helpers.error_kill_switch(page_error_counter=3, storage_error_counter=3, content_error_counter=3))
	
	def error_kill_switch3(self):
		self.assertEqual('no', harvest_helpers.error_kill_switch(page_error_counter=4, storage_error_counter=0, content_error_counter=0))
		
if __name__ == '__main__':
  unittest.main() 
