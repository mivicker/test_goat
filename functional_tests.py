from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		#Edith has heard about her boy mikes to-do app and is ready to check it out,

		self.browser.get('http://localhost:8000')

		#she glances over and does not notice that the title says to-do, but it just feels right.

		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test')

		#She is prompted to enter a to do item, to give her that little pang of stress from our application
		#allways pushing our customers to be better, be more alpha.

		#She enters 'revise resume' because that's what us in this capitalist hell hole have no excuse
		#not to be doing aside from sheer sloth 

		#When she hits enter, the page updates and displays her knew item urgently

		#This leads to another item 'email resume to someone who doesn't care' which is 
		#both a task and the admittion of failure.

		#The page updates, showing both, and edith wonders if this is worth it at all
		#Will she keep this pointless habit?

if __name__ == '__main__':
	unittest.main()