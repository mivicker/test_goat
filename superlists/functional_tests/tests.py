from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
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

		self.wait_for_row_in_list_table('1. revise resume')
		
		#This leads to another item 'email resume to someone who doesn't care' which is 
		#both a task and the admittion of failure.

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("email resume to someone who doesn't care")
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table("2. email resume to someone who doesn't care")
		self.wait_for_row_in_list_table("1. revise resume")

		#The page updates, showing both, and edith wonders if this is worth it at all
		#Will she keep this pointless habit?

	def test_layout_and_styling(self):
		#Edith goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		#She notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta = 10
			)

		#She sees that new list is also nicely centered
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1. testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta = 10
			)		

	def test_multiple_users_can_start_lists_at_different_urls(self):
		#Edith starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("revise resume")
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table("1. revise resume")

		#Edith notices that her list has a unique url
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		self.browser.quit()
		self.browser = webdriver.Firefox()

		#Check that nothing from edith's list is coming through on the new list.

		self.browser.get(self.live_server_url)
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