# Djangoでテスト駆動開発 その3

これはDjangoでテスト駆動開発(Test Driven Development, 以下:TDD)を理解するための学習用メモです。

参考文献は[**Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript (English Edition) 2nd Edition**](https://www.amazon.co.jp/dp/B074HXXXLS/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)を元に学習を進めていきます。

本書ではDjango1.1系とFireFoxを使って機能テスト等を実施していますが、今回はDjagno3系とGoogle Chromeで機能テストを実施していきます。また一部、個人的な改造を行っていますが(Project名をConfigに変えるなど、、)、大きな変更はありません。

⇒⇒[その1 - Chapter1](https://qiita.com/komedaoic/items/dd7abd24961250208c7c)はこちら
⇒⇒[その2 - Chapter2](https://qiita.com/komedaoic/items/58dc509e8f681da73199)はこちら
⇒⇒[その2 - Chapter3](https://qiita.com/komedaoic/items/0057b55c8ba763bda6ca)はこちら

## Part1. The Basics of TDD and Django

### Chapter4. What Are We Doing with All These Tests? (And, Refactoring)

Chapter3までTDDの流れを抑えましたが少々細かすぎて退屈でした(とくに`home_page = None`のくだりなど)
正直そこまで細かく単体テストの結果をみながらコードを書いていく必要はあるのでしょうか？

#### Programming is Like Pulling a Bucket of Water Up from a Well

TDDはいくらか退屈で面倒くさいものですが、プログラマの開発を守る歯止めでもあります。
TDDで開発を進めるのはとても疲れる作業ですが、長期的にみるとありがたみがある開発手法です。
なるべく小さなテストを元に開発を進めるのがコツです。

#### Using Selenium to Test User Interactions

前回、単体テストからhome_pageビューを作成したので、今回は機能テストを拡張していきましょう。

```python
# django-tdd/functional_tests.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 追加
import time  # 追加

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
```

機能テストを拡張しました。実際にテストをしてみます。

```sh
# 開発用サーバーを立ち上げる
$ python manage.py runserver

# 別のcmdを起動して機能テストを実行
$ python functional_tests.py

DevTools listening on ws://127.0.0.1:51636/devtools/browser/9aa225f9-c6e8-4119-ac2a-360d76473962
E
======================================================================
ERROR: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 24, in test_can_start_a_list_and_retrieve_it_later
    header_text = self.browser.find_element_by_tag_name('h1').text
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 530, in find_element_by_tag_name
    return self.find_element(by=By.TAG_NAME, value=name)
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 978, in find_element
    'value': value})['value']
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"h1"}
  (Session info: chrome=79.0.3945.130)


----------------------------------------------------------------------
Ran 1 test in 7.004s

FAILED (errors=1)
```

テスト結果は`<h1>`要素がみつからないとのことでした。これを解決するためにできることはなんでしょうか？
まずは機能テストを拡張したのでコミットしておきましょう。

```sh
$ git add .
$ git commit -m "Functional test now checks we can input a to-do item"
```


