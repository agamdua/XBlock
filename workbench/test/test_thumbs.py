"""Tests for the thumbs module"""

from workbench import scenarios
from workbench.test.selenium_test import SeleniumTest


class ThreeThumbsTest(SeleniumTest):
    """Test the functionalities of the three thumbs test XBlock."""

    def setUp(self):
        super(ThreeThumbsTest, self).setUp()

        scenarios.add_xml_scenario(
            "test_three_thumbs", "three thumbs test",
            """<vertical><thumbs/><thumbs/><thumbs/></vertical>"""
        )
        self.addCleanup(scenarios.remove_scenario, "test_three_thumbs")

        # Suzy opens the browser to visit the workbench
        self.browser.get(self.live_server_url)

        # She knows it's the site by the header
        header1 = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header1.text, 'XBlock scenarios')

    def test_three_thumbs_initial_state(self):
        # She clicks on the three thumbs at once scenario
        link = self.browser.find_element_by_link_text('three thumbs test')
        link.click()

        # The header reflects the XBlock
        header1 = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header1.text, 'XBlock: three thumbs test')

        # She sees that there are 3 sets of thumbs
        vertical_css = 'div.student_view > div.xblock > div.vertical'

        # The following will give a NoSuchElementException error
        # if it is not there
        vertical = self.browser.find_element_by_css_selector(vertical_css)

        # Make sure there are three thumbs blocks
        thumb_css = 'div.xblock[data-block-type="thumbs"]'
        thumbs = vertical.find_elements_by_css_selector(thumb_css)
        self.assertEqual(3, len(thumbs))

        # Make sure they all have 0 for upvote and downvote counts
        up_count_css = 'span.upvote span.count'
        down_count_css = 'span.downvote span.count'

        for thumb in thumbs:
            up_count = thumb.find_element_by_css_selector(up_count_css)
            down_count = thumb.find_element_by_css_selector(down_count_css)
            self.assertEqual('0', up_count.text)
            self.assertEqual('0', down_count.text)

    def test_three_upvoting(self):
        # She clicks on the three thumbs at once scenario
        link = self.browser.find_element_by_link_text('three thumbs test')
        link.click()

        # The vertical that contains the thumbs
        vertical_css = 'div.student_view > div.xblock > div.vertical'
        vertical = self.browser.find_element_by_css_selector(vertical_css)

        # The three thumbs blocks
        thumb_css = 'div.xblock[data-block-type="thumbs"]'
        thumbs = vertical.find_elements_by_css_selector(thumb_css)

        # Up and down counts
        up_count_css = 'span.upvote span.count'
        down_count_css = 'span.downvote span.count'

        # Up vote for the first thumb
        thumbs[0].find_element_by_css_selector('span.upvote').click()

        # Only the first thumb's upcount should increase
        self.assertEqual('1', thumbs[0].find_element_by_css_selector(up_count_css).text)
        self.assertEqual('0', thumbs[1].find_element_by_css_selector(up_count_css).text)
        self.assertEqual('0', thumbs[2].find_element_by_css_selector(up_count_css).text)

        # Down counts should all still be zero
        for thumb in thumbs:
            down_count = thumb.find_element_by_css_selector(down_count_css)
            self.assertEqual('0', down_count.text)

    def test_three_downvoting(self):
        # She clicks on the three thumbs at once scenario
        link = self.browser.find_element_by_link_text('three thumbs test')
        link.click()

        # The vertical that contains the thumbs
        vertical_css = 'div.student_view > div.xblock > div.vertical'
        vertical = self.browser.find_element_by_css_selector(vertical_css)

        # The three thumbs blocks
        thumb_css = 'div.xblock[data-block-type="thumbs"]'
        thumbs = vertical.find_elements_by_css_selector(thumb_css)

        # Up and down counts
        up_count_css = 'span.upvote span.count'
        down_count_css = 'span.downvote span.count'

        # Up vote for the first thumb
        thumbs[0].find_element_by_css_selector('span.downvote').click()

        # Only the first thumb's downcount should increase
        self.assertEqual('1', thumbs[0].find_element_by_css_selector(down_count_css).text)
        self.assertEqual('0', thumbs[1].find_element_by_css_selector(down_count_css).text)
        self.assertEqual('0', thumbs[2].find_element_by_css_selector(down_count_css).text)

        # Up counts should all still be zero
        for thumb in thumbs:
            down_count = thumb.find_element_by_css_selector(up_count_css)
            self.assertEqual('0', down_count.text)
