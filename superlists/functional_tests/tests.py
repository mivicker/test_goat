from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		try:
			table = self.browser.find_element_by_id('id_list_table')
			rows = table.find_elements_by_tag_name('tr')
			self.assertIn(row_text, [row.text for row in rows])
			return
		except (AssertionError, WebDriverException) as e:
			if time.time() - start_time > MAX_WAIT:
				raise e
			time.sleep(0.5)

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

		self.wait_for_row_in_list_table('1. revise resume')
		
		#This leads to another item 'email resume to someone who doesn't care' which is 
		#both a task and the admittion of failure.

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("email resume to someone who doesn't care")
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		self.wait_for_row_in_list_table("1. revise resume")
		self.wait_for_row_in_list_table("2. email resume to someone who doesn't care")

		#The page updates, showing both, and edith wonders if this is worth it at all
		#Will she keep this pointless habit?

	def test_multiple_users_can_start_lists_at_different_urls(self):
		#Edith starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("revise resume")
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table("revise resume")

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("email resume to someone who doesn't care")
		inputbox.send_keys(Keys.ENTER)
		
		self.wait_for_row_in_list_table("1. revise resume")
		self.wait_for_row_in_list_table("2. email resume to someone who doesn't care")

		#Edith notices that her list has a unique url
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		self.browser.quit()
		self.browser = webdriver.Firefox()

		#Check that nothing from edith's list is coming through on the new list.

		self.brower.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('revise resume', page_text)
		self.assertNotIn("email resume to someone who doesn't care", page_text)

		#Test adding a new item.

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1. buy milk')

		#Francis notices her url is fresh, not ediths.

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#Check again that nothing from edith's list is showing up and that the new items are availble

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertIn('1. buy milk', page_text)
		self.assertNotIn('1. revise resume', page_text)

if __name__ == '__main__':
	unittest.main()
