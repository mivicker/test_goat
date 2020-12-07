from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		#Edith has heard about her boy mikes to-do app and is ready to check it out,

		self.browser.get(self.live_server_url)

		#she glances over and does not notice that the title says to-do, but it just feels right.

		self.assertIn('To-do', self.browser.title)
		
		#Maybe she reads the headline for once
		header_text = self.browser.find_element_by_tag_name('h1').text
		self. assertIn('To-do', header_text)

		#She is prompted to enter a to do item, to give her that little pang of stress from our application
		#allways pushing our customers to be better, be more alpha.

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
			)

		#She enters 'revise resume' because that's what us in this capitalist hell hole have no excuse
		#not to be doing aside from sheer sloth 

		inputbox.send_keys('revise resume')

		#When she hits enter, the page updates and displays her knew item urgently

		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		self.check_for_row_in_list_table('1. revise resume')
		
		#This leads to another item 'email resume to someone who doesn't care' which is 
		#both a task and the admittion of failure.

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("email resume to someone who doesn't care")
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		self.check_for_row_in_list_table("1. revise resume")
		self.check_for_row_in_list_table("2. email resume to someone who doesn't care")

		#The page updates, showing both, and edith wonders if this is worth it at all
		#Will she keep this pointless habit?

		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main()
