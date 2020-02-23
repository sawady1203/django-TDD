# Djangoでテスト駆動開発 その5

これはDjangoでテスト駆動開発(Test Driven Development, 以下:TDD)を理解するための学習用メモです。

参考文献は[**Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript (English Edition) 2nd Edition**](https://www.amazon.co.jp/dp/B074HXXXLS/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)を元に学習を進めていきます。

本書ではDjango1.1系とFireFoxを使って機能テスト等を実施していますが、今回はDjagno3系とGoogle Chromeで機能テストを実施していきます。また一部、個人的な改造を行っていますが(Project名をConfigに変えるなど、、)、大きな変更はありません。

⇒⇒[その1 - Chapter1](https://qiita.com/komedaoic/items/dd7abd24961250208c7c)はこちら
⇒⇒[その2 - Chapter2](https://qiita.com/komedaoic/items/58dc509e8f681da73199)はこちら
⇒⇒[その3 - Chapter3](https://qiita.com/komedaoic/items/0057b55c8ba763bda6ca)はこちら
⇒⇒[その4 - Chapter4](https://qiita.com/komedaoic/items/148b42f070be478f6e23)はこちら
⇒⇒[その5 - Chapter5](https://qiita.com/komedaoic/items/f431c13531ced5b3d2f3)はこちら

## Part1. The Basics of TDD and Django

### Chapter6. Improving Functional Testss: Ensuring Isolation and Removing Voodoo Sleeps

Chapter5ではPOSTされたデータが保存されているか、それを問題なくresponseに返せているのか、を確認しました。
単体テストではDjangoのテスト用DBを作成しているため、テスト実行時とともにテスト用のデータは削除されますが、
機能テストでは(現在の設定では)本番用のDB(db.sqlite3)を使用してしまい、テスト時のデータも保存されてしまうという問題がありました。
今回はこれらの問題に対する`best practice`を実践していきます。

#### Ensuring Test Isolation in Functional Tests

テスト用のデータが残るとテスト間での分離ができないため、「テスト用のデータが保存されているために成功するはずのテストが失敗する」
ようなトラブルが発生します。これを避けるためにテスト間を分離することを意識することが大切です。

機能テストでも単体テストのようにテスト用のデータベースを自動で作成して、テストが終われば削除できるような仕組みを
Djagnoでは`LiveServerTestCase`クラスを使用することで実装することができます。

`LiveServerTestCase`はDjangoのテストランナーを使ってテストを行うことを想定しています。
Djangoのテストランナーが走ると全てのフォルダ内の`test`から始まるファイルを実行します。

したがって、Djangoのアプリケーションのように機能テスト用のフォルダを作成しましょう。

```sh
# フォルダの作成
$ mkdir functional_tests
# DjangoにPythonパッケージとして認識させるため
$ type nul > functional_tests/__init__.py
# 既存の機能テストを名前を変えて移動
$ git mv functional_tests.py functional_tests/tests.py
# 確認
$ git status
```

これで`python manage.py functional_tests.py`で機能テストを実行していたのが、
`python manage.py test functional_tests`で実行できるようになりました。

それでは機能テストを書き換えましょう。

```python
# django-tdd/functional_tests/tests.py

from django.test import LiveServerTestCase  # 追加
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):  # 変更

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # のび太は新しいto-doアプリがあると聞いてそのホームページにアクセスした。
        self.browser.get(self.live_server_url)  # 変更

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
        time.sleep(3)  # ページ更新を待つ。
        self.check_for_row_in_list_table('1: Buy dorayaki')

        # テキストボックスは引続きアイテムを記入することができるので、
        # 「どら焼きのお金を請求すること」を記入した(彼はお金にはきっちりしている)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Demand payment for the dorayaki")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        # ページは再び更新され、新しいアイテムが追加されていることが確認できた
        self.check_for_row_in_list_table('2: Demand payment for the dorayaki')

        # のび太はこのto-doアプリが自分のアイテムをきちんと記録されているのかどうかが気になり、
        # URLを確認すると、URLはのび太のために特定のURLであるらしいことがわかった
        self.fail("Finish the test!")

        # のび太は一度確認した特定のURLにアクセスしてみたところ、

        # アイテムが保存されていたので満足して眠りについた。

```

機能テストを`unittest`モジュールから`LiveServerTestCase`を継承した形に変更しました。
Djangoのテストランナーを使用して機能テストを実行できるようになったので、`if __name == '__main__'`以下は削除しました。

それでは実際に機能テストを実行してみましょう。

```sh
$ python manage.py test functional_tests

Creating test database for alias 'default'...
System check identified no issues (0 silenced).

======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\masayoshi\Documents\03.study\17. Portfolio\django-TDD\functional_tests\tests.py", line 59, in test_can_start_a_list_and_retrieve_it_later
    self.fail("Finish the test!")
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 1 test in 28.702s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

機能テストは`self.fail`で終了し、`LiveServerTestCase`を適用する前と同じ結果が得られました。
また、機能テスト用のデータベースが作成され、テストが終了すると同時に削除されていることも確認できました。

ここでコミットしておきましょう。

```sh
$ git status
$ git add functional_tests
$ git commit -m "make functional_tests an app, use LiveSeverTestCase"
```
