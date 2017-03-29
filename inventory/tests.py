from django.test import TestCase

import views

# Create your tests here.

class MoveTests(unittest.TestCase):
	def test_five_plus_five(self):
		assert 5 + 5 == 10

	def test_one_plus_one(self):
		assert not 1 + 1 == 3



# # class ViewTests(unittest.TestCase):
# # 	def test_url(self, Index):
# # 		assert 'https://api-snacks.nerderylabs.com/v1/snacks?ApiKey=' + api_key


# if __name__ == '__main__':  # if you run file directly, it runs unit test here
# 	unittest.main()