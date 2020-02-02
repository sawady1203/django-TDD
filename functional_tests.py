# django-tdd/functional_tests.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # のび太は新しいto-doアプリがあると聞いてそのホームページにアクセスした。
        self.browser.get('http://localhost:8000')

        # のび太はページのタイトルがとヘッダーがto-doアプリであることを示唆していることを確認した。
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # のび太はto-doアイテムを記入するように促され、
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # のび太は「どら焼きを買うこと」とテキストボックスに記入した(彼の親友はどら焼きが大好き)
        inputbox.send_keys('Buy dorayaki')

        # のび太がエンターを押すと、ページは更新され、
        # "1: どら焼きを買うこと"がto-doリストにアイテムとして追加されていることがわかった
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  # ページ更新を待つ。

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == "1: Buy dorayaki" for row in rows)
        )

        # テキストボックスは引続きアイテムを記入することができるので、
        # 「どら焼きのお金を請求すること」を記入した(彼はお金にはきっちりしている)

        self.fail("Finish the test!")

        # ページは再び更新され、新しいアイテムが追加されていることが確認できた

        # のび太はこのto-doアプリが自分のアイテムをきちんと記録されているのかどうかが気になり、
        # URLを確認すると、URLはのび太のために特定のURLであるらしいことがわかった

        # のび太は一度確認した特定のURLにアクセスしてみたところ、

        # アイテムが保存されていたので満足して眠りについた。


if __name__ == '__main__':
    unittest.main(warnings='ignore')
