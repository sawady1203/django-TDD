# Djangoでテスト駆動開発 その2

これはDjangoでテスト駆動開発(Test Driven Development, 以下:TDD)を理解するための学習用メモです。

参考文献は[**Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript (English Edition) 2nd Edition**](https://www.amazon.co.jp/dp/B074HXXXLS/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)を元に学習を進めていきます。

本書ではDjango1.1系とFireFoxを使って機能テスト等を実施していますが、今回はDjagno3系とGoogle Chromeで機能テストを実施していきます。また一部、個人的な改造を行っていますが(Project名をConfigに変えるなど、、)、大きな変更はありません。

⇒⇒[その1](https://qiita.com/komedaoic/items/dd7abd24961250208c7c)はこちら

## Part1. The Basics of TDD and Django

### Chapter2 Extending Our Functional Test Usinng the unittest Module

Chapter1では環境構築から初めての機能テストを記述し、DjangoのDefaultページが機能しているかどうかを機能テストを通して確認することができました。
今回はToDoアプリケーションを作成しながらこれを実際のフロントページに適用していきたいと思います。

ChromeのWebドライバーとSeleniumをつかったテストはユーザー視点でアプリケーションが**どう機能するのか**を確認することができるため、**機能テスト**と呼ばれています。
これはユーザーがアプリケーションを使用するときの *ユーザーストーリー* をなぞるものであり、ユーザーがアプリケーションをどう利用して、それに対してアプリケーションがどうレスポンスを返すのかを決定づけるものと言えます。

#### Functional Test == Acceptance Test == End-To-End Test

今回参考にしている[**Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript (English Edition) 2nd Edition**](https://www.amazon.co.jp/dp/B074HXXXLS/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)ではアプリケーションの機能(*function*)をテストすることを*functional tests*と呼んでいるため、本記事では機能テストと呼んでいます。これは *acceptance tests(受け入れテスト)* 、*End-To-End tests(E2Eテスト、インテグレーションテスト)* と呼ばれたりもします。このテストを行うのは外から見てアプリケーション全体がどう機能するのかを確認するためです。

そこで実際のユーザーストーリー想定しながら、機能テストにコメントとして記述していきます。

```python
# django-tdd/functional_tests.py

from selenium import webdriver

browser = webdriver.Chrome()

# のび太は新しいto-doアプリがあると聞いてそのホームページにアクセスした。
browser.get('http://localhost:8000')

# のび太はページのタイトルがとヘッダーがto-doアプリであることを示唆していることを確認した。
assert 'To-Do' in browser.title

# のび太はto-doアイテムを記入するように促され、


# のび太は「どら焼きを買うこと」とテキストボックスに記入した(彼の親友はどら焼きが大好き)


# のび太がエンターを押すと、ページは更新され、
# "1: どら焼きを買うこと"がto-doリストにアイテムとして追加されていることがわかった


# テキストボックスは引続きアイテムを記入することができるので、
# 「どら焼きのお金を請求すること」を記入した(彼はお金に関してはきっちりしている)


# ページは再び更新され、新しいアイテムが追加されていることが確認できた


# のび太はこのto-doアプリが自分のアイテムをきちんと記録されているのかどうかが気になり、
# URLを確認すると、URLはのび太のために特定のURLであるらしいことがわかった


# のび太は一度確認した特定のURLにアクセスしてみたところ、


# アイテムが保存されていたので満足して眠りについた。


browser.quit()

```

Titleに関するassertを"Django"から"To-Do"に変更しました。このままでは機能テストが失敗することが予想されます。
ということで機能テストを実行してみます。

```sh
# ローカルサーバーの起動
$ python manage.py runserver

# 別のコマンドラインを立ち上げて
# 機能テストの実行
$ python functional_tests.py

Traceback (most recent call last):
  File "functional_tests.py", line 11, in <module>
    assert 'To-Do' in browser.title
AssertionError
```

テストは予想していた通り失敗しました。
したがって、このテストが成功できるように開発を進めて行けばいいことがわかります。

#### unittest Moduleを使用する

先ほど実行した機能テストでは

- AssertioErrorが親切でない(browser titleが実際に何だったのか知れると嬉しい)

- Seleniumで起動させたブラウザが消されず残っている

という煩わしさがありました。これらはPythonの標準モジュールであるunittestモジュールを使うと解決することができます。

機能テストを下記のように書き換えてみます。

```python
# django-tdd/functional_tests.py

from selenium import webdriver
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
        self.fail('Finish the test!')

        # のび太はto-doアイテムを記入するように促され、

        # のび太は「どら焼きを買うこと」とテキストボックスに記入した(彼の親友はどら焼きが大好き)

        # のび太がエンターを押すと、ページは更新され、
        # "1: どら焼きを買うこと"がto-doリストにアイテムとして追加されていることがわかった

        # テキストボックスは引続きアイテムを記入することができるので、
        # 「どら焼きのお金を請求すること」を記入した(彼はお金にはきっちりしている)

        # ページは再び更新され、新しいアイテムが追加されていることが確認できた

        # のび太はこのto-doアプリが自分のアイテムをきちんと記録されているのかどうかが気になり、
        # URLを確認すると、URLはのび太のために特定のURLであるらしいことがわかった

        # のび太は一度確認した特定のURLにアクセスしてみたところ、

        # アイテムが保存されていたので満足して眠りについた。


if __name__ == '__main__':
    unittest.main(warnings='ignore')

```

機能テストはunittest.TestCaseを継承して書くことができます。
今回のポイントを整理してみます。

- 実行させたいテスト関数は *test_* から始めることでテストランナーが自動でテストを走らせる。
- *setUp* と *tearDown* はテストが走る前後で実行される特別な関数。
- *tearDown* はテストエラーでも実行される。
- self.fail()は何がなんでもテストは失敗し、エラーが吐き出される。
- unittest.main()でテストが実行され、自動的にテストケースとそのメソッドが実行される。
- warnings='ignore'のオプションを追加すると過剰なResoureWarningなどを無視することができる。

それでは実行してみましょう。

```sh
$ python functional_tests.py
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 20, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('To-Do', self.browser.title)
AssertionError: 'To-Do' not found in 'Django: 納期を逃さない完璧主義者のためのWebフレームワーク'

----------------------------------------------------------------------
Ran 1 test in 7.956s

FAILED (failures=1)

```

unittestモジュールを使うことで *AssertionError* の中身がより理解しやすくなりました。

ここで *self.assertIn('To-Do', self.brower.title)* を *self.assertIn('Django', self.brower.title)* としたらテストがクリアできるはずです。これを確認してみます。

```python
# django-tdd/functional_tests.py

~~~
    def test_can_start_a_list_and_retrieve_it_later(self):
        # のび太は新しいto-doアプリがあると聞いてそのホームページにアクセスした。
        self.browser.get('http://localhost:8000')

        # のび太はページのタイトルがとヘッダーがto-doアプリであることを示唆していることを確認した。
        self.assertIn('Django', self.browser.title)  # 変更
        self.fail('Finish the test!')
~~~
```

```sh
$ python functinal_tests.py
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 21, in test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 1 test in 6.081s

FAILED (failures=1)
```

実行した結果、テストは成功するはずですが、テストはFAILとされてしましました。
*AssertionError* を確認すると、*self.fail('Finish the test')* で設定したメッセージが反映されました。
これは *self.fail('message')* はエラーが無くても必ず設定したエラーメッセージを吐き出す機能を持っているためです。
ここではテストが終わったことがわかるようにリマインダーとして設定されています。

ということで今度は *self.fail('Finish the test!')* をコメントアウトして実行してみます。

```python
# django-tdd/functional_tests.py
~~~
    def test_can_start_a_list_and_retrieve_it_later(self):
        # のび太は新しいto-doアプリがあると聞いてそのホームページにアクセスした。
        self.browser.get('http://localhost:8000')

        # のび太はページのタイトルがとヘッダーがto-doアプリであることを示唆していることを確認した。
        self.assertIn('Django', self.browser.title)
        # self.fail('Finish the test!')  # コメントアウト
~~~
```

```sh
$ python functinal_tests.py

.
----------------------------------------------------------------------
Ran 1 test in 7.698s

OK
```

確かにエラーは無くテストが成功したことが確認できました。最終的な機能テストの出力はこのような形になるはずです。
*functional_tests.py* の 変更した箇所を元に戻しておきましょう。

```python
# django-tdd/functional_tests.py
~~~
    def test_can_start_a_list_and_retrieve_it_later(self):
        # のび太は新しいto-doアプリがあると聞いてそのホームページにアクセスした。
        self.browser.get('http://localhost:8000')

        # のび太はページのタイトルがとヘッダーがto-doアプリであることを示唆していることを確認した。
        self.assertIn('To-do', self.browser.title)
        self.fail('Finish the test!')
~~~
```

#### Commit

ユーザーストーリーをコメントで追加しながら作成することで、to-doアプリケーションの機能テストを作成して実行することができました。ここでコミットしておきましょう。**git status**をすると変更したファイルを確認することができました。

**git diff**をすると最後のコミットとの差分を確認することができます。
これを実行するとfunctional_tests.pyが大きく変更されていることがわかります。

それではコミットしておきます。

```sh
$ git add .
$ git commit -m "First FT specced out in comments, and now users unittest"
```

#### Chapter2まとめ

機能テストをDjangoのプロジェクトの立ち上げを確認するレベルから、To-Doアプリケーションを使用するユーザーストーリに基づいたものに変更することができました。更にunittestを使用することでエラーメッセージをよりうまく活用することができることがわかりました。

