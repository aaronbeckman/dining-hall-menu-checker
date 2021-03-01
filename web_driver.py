import datetime
import json
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Web_Driver:
    def __init__(self, dest, path):
        with open('constants.json') as f:
            xpaths = json.load(f)

        self.date_xpath = xpaths["date_xpath"]
        self.months = xpaths["months"]
        self.next_day_xpath = xpaths["next_day_xpath"]
        self.previous_day_xpath = xpaths["previous_day_xpath"]

        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
            # options.add_argument('headless') # SOOOOOON
            self.site = webdriver.Chrome(options=options, executable_path=path)
            self.site.get(dest)  # Read from main site
        except Exception as e:
            logging.error('[web_driver.Web_Driver.__init__] {}'.format(e))

    def close(self):
        self.site.quit()

    def retrieve_site_day(self):
        """ Returns the current day selected on the webpage in datetime.date format """

        retrieved_date = self.site.find_element_by_xpath(self.date_xpath).text.split(
            ', ')  # ['dayofweek', 'month dayofmonth', 'year']

        date = datetime.date(int(retrieved_date[2]), self.months.get(
            retrieved_date[1].split(' ')[0]), int(retrieved_date[1].split(' ')[1]))

        return date

    def select_location(self, xpath):
        """
        Selects the specific dining hall to search

        Parameters:
        xpath (str): xpath of the dining hall location (retrieved from constants.json)
        """
        self.site.find_element_by_xpath(xpath).click()

    def time_travel(self, delta):
        """
        Goes [delta] days from the current day

        Keep in mind there are limits, so the returned date value should be used to get the displayed date,
        rather than incrementing a counter unlinked to this, as a max/min may be reached causing this function
        to do nothing. Range seems to be (today) to (today + 7) for a total of 8 days

        Parameters:
        xpath (str): xpath of the button to press (either next or previous day, retrieved from constants.json)

        Returns:
        (datetieme.date): The current date displayed
        """
        xpath = self.next_day_xpath if delta > 0 else self.previous_day_xpath
        delta = abs(delta)

        for i in range(delta):
            self.site.find_element_by_xpath(xpath).click()

        return self.retrieve_site_day()

    def select_day(self, day):
        """
        Goes to the selected day, if possible (within standard 8 day range)

        Parameters:
        day (datetime.date): day to go to

        Returns:
        (datetieme.date): The current date displayed
        """
        current_day = datetime.date.today()

        current_time_delta = (day - current_day).days
        site_time_delta = (day - self.retrieve_site_day()).days

        if current_time_delta < 8 and current_time_delta > 0:
            return self.time_travel(site_time_delta)

    def select_meal(self, xpath):
        """
        Selects the meal (as in, related to the time of day)

        Parameters:
        xpath (str): xpath of the meal button (retrieved from constants.json)

        Returns:
        (str): the selected meal (Breakfast, Lunch, Dinner, or Late Night)
        """
        meal = self.site.find_element_by_xpath(xpath)
        meal.click()

        return meal.text
