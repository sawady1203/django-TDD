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

#### The "Don't Test Constants" Rule, and Templates to the Rescue

現在のlists/tests.pyを確認してみましょう。

```python
# lists/tests.py

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_current_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

```

これを見ると特定のHTMLの文字列が含まれているかどうかを確認していますが、これは効果的な方法ではありません。
一般的に単体テストでは定数をテストすることを避けるべきです。特にHTMLは定数(テキスト)の集まりのようなものです。

HTMLはテンプレートを使って作成し、それを想定した機能テストを進めるべきです。

##### Refactoring to Use a Template

lists/views.pyが特定のHTMLファイルを返すようにリファクタリングをします。TDDでのリファクタリングのお気持ちは*既存の機能を変化させずに改善する*ことにあります。リファクタリングはテストなしに進められません。まずは単体テストしてみましょう。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.009s

OK
Destroying test database for alias 'default'...
```

前回からの続きであれば問題なくテストはパスするはずです。
それではテンプレートを作成します。

```sh
$ mkdir templates
$ cd templates
$ mkdir lists
$ type nul > lists\home.html
$ cd ../ # manage.pyがあるディレクトリに戻る
```

```html
<!-- templates/lists/home.html -->

<html>
    <title>To-Do lists</title>
</html>
```

これを返すようにlists/views.pyを変更します。

```python
# lists/views.py

from django.shortcuts import render


def home_page(request):
    return render(request, 'lists/home.html')
```

単体テストしてみましょう。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
E.
======================================================================
ERROR: test_home_page_returns_current_html (lists.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\--your_path--\django-TDD\lists\tests.py", line 18, in test_home_page_returns_current_html
    response = home_page(request)
  File "C:\--your_path--\django-TDD\lists\views.py", line 7, in home_page
    return render(request, 'home.html')
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\django\shortcuts.py", line 19, in render
    content = loader.render_to_string(template_name, context, request, using=using)
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\django\template\loader.py", line 61, in render_to_string
    template = get_template(template_name, using=using)
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\django\template\loader.py", line 19, in get_template
    raise TemplateDoesNotExist(template_name, chain=chain)
django.template.exceptions.TemplateDoesNotExist: home.html

----------------------------------------------------------------------
Ran 2 tests in 0.019s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

テンプレートは確かに作成したはずにも関わらず,`django.template.exceptions.TemplateDoesNotExist: home.html`というメッセージが確認できます。
また、lists/views.pyの`return render(request, 'home.html')`で処理がうまく行っていないのも確認できます。

これはアプリケーションを作成した際にDjangoに登録していないのが原因です。
config/settings.pyの`INSTALLED_APPS`に追加しましょう。

```python
# config/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lists.apps.ListsConfig',  # 追加
]

```

これでテストしてみます。

```sh
$ python manage.py test

======================================================================
FAIL: test_home_page_returns_current_html (lists.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\--your_path--\django-TDD\lists\tests.py", line 22, in test_home_page_returns_current_html
    self.assertTrue(html.endswith('</html>'))
AssertionError: False is not true

----------------------------------------------------------------------

```

これを確認すると`self.assertTrue(html.endswith('</html>'))`でつまづいているのが分かりますが、lists/home.htmlは確かに`</html>`で終わっています。
lists/tests.pyのhtmlの一部に`print(repr(html))`を追加して実行してみると確認できますが、lists/home.htmlの文末には改行コードの`\n`が追加されています。
これをパスするために、テストを一部変更する必要があります。

```python
# lists/tests.py

#~~省略~~
    self.assertTrue(html.strip().endswith('</html>'))  # 変更

```

これで実行してみましょう。

```sh
$ python manage.py test

----------------------------------------------------------------------
Ran 2 tests in 0.032s

OK
```

単体テストはパスできました。これでlists/views.pyをテンプレートを返すように変更することができました。
続いてlists/tests.pyも正しいテンプレートがレンダリングされているのかどうかを判断するようにリファクタリングしてみます。

##### The Django Test Client

正しいテンプレートが返ってきているのかどうかをテストする方法はDjangoが用意している`.assertTemplteUsed`が効果的です。
テストの一部に追加してみましょう。

```python
# lists/tests.py

# ~~省略~~

def test_home_page_returns_current_html(self):
    response = self.client.get('/')  # 変更

    html = response.content.decode('utf8')
    # print(repr(html))
    self.assertTrue(html.startswith('<html>'))
    self.assertIn('<title>To-Do lists</title>', html)
    self.assertTrue(html.strip().endswith('</html>'))  # 変更

    self.assertTemplateUsed(response, 'lists/home.html')  # 追加

```

`.assertTemplateUsed`を使うためにHttpRequest()をつかったマニュアル的なrequestではなく、Djagno test Clientをつかったリクエストに変更した。

```sh
$ python manage.py test

----------------------------------------------------------------------
Ran 2 tests in 0.040s

OK
```

このDjango test Clientと`.assertTemplateUsed`を使うと、URLのマッピングができているかどうか、指定したテンプレートが返ってくのかどうかを一緒に確認することができる。したがって、lists/tests.pyはもっとすっきり書き直すことができる。

```python
# lists/tests.py

from django.test import TestCase


class HomePageTest(TestCase):

    def test_users_home_template(self):
        response = self.client.get('/')  # URLの解決
        self.assertTemplateUsed(response, 'lists/home.html')
```

単体テスト、lists/view.pyをリファクタリングできたのでコミットしておきましょう。

```sh
$ git add .
$ git commit -m "Refactor home page view to user a template"
```

#### A Little More of Our Front Page

単体テストはパスしまいたが、機能テストは未だ失敗したままです。
テンプレートの中身は単体テストでは評価されないため、機能テストを通してテンプレートが正しいのかどうかを判断します。

```html
<!-- lists/home.html -->
<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
    </body>
</html>
```

```sh
$ python functional_tests.py

[...]
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="id_new_item"]"}
  (Session info: chrome=79.0.3945.130)
```

新しいアイテムを入力する場所を追加します。

```html
<!-- lists/home.html -->
<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
        <input id="id_new_item">
    </body>
</html>
```

```sh
$ python functional_tests.py

[...]
AssertionError: '' != 'Enter a to-do item'
+ Enter a to-do item

```

placeholderを追加しましょう。

```html
<!-- lists/home.html -->
<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
        <input id="id_new_item" placeholder="Enter a to-do item">
    </body>
</html>
```

```sh
$ python functional_tests.py

[...]
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="id_list_table"]"}

```

tableタグを追加します。

```html
<!-- lists/home.html -->
<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
        <input id="id_new_item" placeholder="Enter a to-do item">
        <table id="id_list_table">
        </table>
    </body>
</html>
```

```sh
$ python functional_tests.py

======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 45, in test_can_start_a_list_and_retrieve_it_later
    any(row.text == "1: Buy dorayaki" for row in rows)
AssertionError: False is not true
```

これはfunctional_tests.pyの`.assertTrue(any(~~))`でのエラーです。any(iterator)は引数がiteratorの中にあればTrueを返します。
入力された値を"1: Buy dorayaki"として返す機能は後で実装します。
ひとまずカスタムエラーメッセージを`"New to-do item did not appear in table"`として追加しておきましょう。

```python
# functional_tests.py

# ~~省略~~
table = self.browser.find_element_by_id('id_list_table')
rows = table.find_elements_by_tag_name('tr')
self.assertTrue(
    any(row.text == "1: Buy dorayaki" for row in rows),
    "New to-do item did not appear in table"  # 追加
)
```

```sh
$ python functional_tests.py

======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 46, in test_can_start_a_list_and_retrieve_it_later
    "New to-do item did not appear in table"
AssertionError: False is not true : New to-do item did not appear in table

----------------------------------------------------------------------
```

コミットしておきましょう。

```sh
$ git add .
$ git commit -m "Front page HTML now generated from template"
```

#### Chapter4まとめ
機能テスト、単体テスト、単体テストとコーディングのサイクル、リファクタリングの流れを実装しました。
