# Djangoでテスト駆動開発 その5

これはDjangoでテスト駆動開発(Test Driven Development, 以下:TDD)を理解するための学習用メモです。

参考文献は[**Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript (English Edition) 2nd Edition**](https://www.amazon.co.jp/dp/B074HXXXLS/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)を元に学習を進めていきます。

本書ではDjango1.1系とFireFoxを使って機能テスト等を実施していますが、今回はDjagno3系とGoogle Chromeで機能テストを実施していきます。また一部、個人的な改造を行っていますが(Project名をConfigに変えるなど、、)、大きな変更はありません。

⇒⇒[その1 - Chapter1](https://qiita.com/komedaoic/items/dd7abd24961250208c7c)はこちら
⇒⇒[その2 - Chapter2](https://qiita.com/komedaoic/items/58dc509e8f681da73199)はこちら
⇒⇒[その2 - Chapter3](https://qiita.com/komedaoic/items/0057b55c8ba763bda6ca)はこちら

## Part1. The Basics of TDD and Django

### Chapter5. Saving User Input: Testing the Database

ユーザーからのインプットがある場合を想定してテスト駆動開発をしていきましょう。

#### Wiring Up Our Form to Send a Post Request

ユーザーからインプットがある場合、それが問題なく保存されていることを確認するテストが必要です。
標準的なHTMLからのPOSTリクエストを想定してみます。
home.htmlにformタグを挿入して見ましょう。

```html
<!-- lists/home.html -->
<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
            <form method="post">
                <input name="item_text" id="id_new_item" placeholder="Enter a to-do item">
            </form>
        <table id="id_list_table">
        </table>
    </body>
</html>

```

機能テストを実行してみましょう。

```sh
$ python functional_tests.py


DevTools listening on ws://127.0.0.1:58348/devtools/browser/2ec9655c-1dd9-4369-a97b-fb7099978b93
E
======================================================================
ERROR: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 42, in test_can_start_a_list_and_retrieve_it_later
    table = self.browser.find_element_by_id('id_list_table')
  File "C:\Users\masayoshi\Documents\03.study\17. Portfolio\django-TDD\venv-tdd\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 360, in find_element_by_id
    return self.find_element(by=By.ID, value=id_)
  File "C:\Users\masayoshi\Documents\03.study\17. Portfolio\django-TDD\venv-tdd\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 978, in find_element
    'value': value})['value']
  File "C:\Users\masayoshi\Documents\03.study\17. Portfolio\django-TDD\venv-tdd\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "C:\Users\masayoshi\Documents\03.study\17. Portfolio\django-TDD\venv-tdd\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="id_list_table"]"}
  (Session info: chrome=79.0.3945.130)


----------------------------------------------------------------------
Ran 1 test in 9.982s

FAILED (errors=1)
```

機能テストが予想していない内容で失敗しました。
Seleniumによる実行画面を確認してみると`csrf_token`によるアクセスエラーでした。
Djangoテンプレートタグを使ってCSRFタグを追加しましょう。

```html
<!-- lists/home.html -->
<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
            <form method="post">
                <input name="item_text" id="id_new_item" placeholder="Enter a to-do item">
                {% csrf_token %}
            </form>
        <table id="id_list_table">
        </table>
    </body>
</html>
```

機能テストを実施します。

```sh
DevTools listening on ws://127.0.0.1:58515/devtools/browser/0bbd1ede-a958-4371-9d8a-99b5cd55b9c3
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 46, in test_can_start_a_list_and_retrieve_it_later
    "New to-do item did not appear in table"
AssertionError: False is not true : New to-do item did not appear in table

----------------------------------------------------------------------
Ran 1 test in 13.718s

FAILED (failures=1)
```

エラー内容が`New to-do item did not appear in table`となりました。
これはまだサーバー側がPOSTリクエストの処理を追加していないためです。

#### Processing a POST Request on the Server

`home_page` View にPOST処理を追加していきましょう。その前に*list/tests.py*を開いて`HomePageTest`にPOSTが保存されているかどうかを確認するテストを追加します。

```python
# lists/tests.py

from django.test import TestCase


class HomePageTest(TestCase):

    def test_users_home_template(self):
        response = self.client.get('/')  # URLの解決
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': "A new list item"})
        self.assertIn('A new list item', response.content.decode())
```

ここで現在の*lists/views.py*を確認しておきます。

```python
# lists/views.py

from django.shortcuts import render


def home_page(request):
    return render(request, 'lists/home.html')
```

現在のViewはリクエストに対して*home.html*を返すのみとなっています。
単体テストを行ってみましょう。

```sh
python manage.py test

======================================================================
FAIL: test_can_save_a_POST_request (lists.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\masayoshi\Documents\03.study\17. Portfolio\django-TDD\lists\tests.py", line 14, in test_can_save_a_POST_request
    self.assertIn('A new list item', response.content.decode())
AssertionError: 'A new list item' not found in '<!-- lists/home.html -->\n<html>\n    <head>\n        <title>To-Do lists</title>\n    </head>\n    <body>\n        <h1>Your To-Do list</h1>\n            <form method="post">\n                <input name="item_text" id="id_new_item" placeholder="Enter a to-do item">\n                <input type="hidden" name="csrfmiddlewaretoken" value="WxS3OX6BLnYLQuT4saIKUU4O18Z9mDZDIfhIrUiBjeeizFlf2ajmbj86QyzEo04R">\n            </form>\n        <table id="id_list_table">\n        </table>\n    </body>\n</html>\n'

----------------------------------------------------------------------
```

テスト結果を確認すると`response.content.decode()`の中身が表示されているのが分かります。
中身を確認すると、`{% csrf_token %}`により`<input type="hidden">`という形でCSRFトークンがDjangoによって追加されていることがわかります。

テストをパスするため、POSTで投げられている`item_text`を返せるようにViewを変更します。

```python
# lists/views.py

from django.shortcuts import HttpResponse  # 追加
from django.shortcuts import render


def home_page(request):
    if request.method == 'POST':
        return HttpResponse(request.POST['item_text'])
    return render(request, 'lists/home.html')

```

これで単体テストはパスしましたが、これは本当に行いたいことではありません。


#### Passing Python Variables to Be Rendered in the Template

Djagnoテンプレートでは`{{  }}`を使ってViewからの変数を利用することが可能です。
これを使ってPOSTさた内容を表示できるように`home.html`に追加しておきましょう。

```html
    <body>
        <h1>Your To-Do list</h1>
            <form method="post">
                <input name="item_text" id="id_new_item" placeholder="Enter a to-do item">
                {% csrf_token %}
            </form>
        <table id="id_list_table">
            <tr><td>{{ new_item_text }}</td></tr>
        </table>
    </body>
```

Viewで`new_item_text`を返すことで`home.html`に表示させることができますが、そもそもリクエストに対して`home.html`を返しているかどうかもテストしておかなければなりません。単体テストに追加しましょう。

```python
def test_can_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': "A new list item"})
    self.assertIn('A new list item', response.content.decode())
    self.assertTemplateUsed(response, 'lists/home.html')  # 追加
```

単体テストを実行すると`AssertionError: No templates used to render the response`となりました。
これはPOST時のレスポンスにHTMLを指定していないためです。Viewを変更しましょう。

```python
def home_page(request):
    if request.method == 'POST':
        return render(request, 'lists/home.html', {
            'new_item_text': request.POST['item_text'],
        })
    return render(request, 'lists/home.html')
```

これで単体テストはパスできました。それでは機能テストを実行してみます。

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

アイテムを追加して表示できているはずにも関わらず、`AssertionError: False is not true : New to-do item did not appear in table`となりました。
エラー内容をより詳細に確認するために、機能テストの一部を書き換えて実行してみます。

```python

self.assertTrue(
    any(row.text == "1: Buy dorayaki" for row in rows),
    f"New to-do item did not appear in table. Contents were: \
    \n{table.text}"
)
```

もう一度実行します。

```sh
$ python functional_tests.py

======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 47, in test_can_start_a_list_and_retrieve_it_later
    \n{table.text}"
AssertionError: False is not true : New to-do item did not appear in table. Contents were:
Buy dorayaki

----------------------------------------------------------------------
```

実際のtableのテキストを確認することができました。
これを見ると`"1: Buy dorayaki" `となるべきところが`Buy dorayaki`となっているためにエラーが出ているようです。

これを解決するViewはまだ後になりそうです。今回は`item_text`が返ってきているのかどうかを確認するためなので、機能テストをそのように書き換えます。

```python
# functional_tests.py
[...]
self.assertIn('1: Buy dorayaki', [row.text for row in rows])
[...]
```

機能テストを実行します。

```sh
$ python functional_tests.py

======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 50, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('1: Buy dorayaki', [row.text for row in rows])
AssertionError: '1: Buy dorayaki' not found in ['Buy dorayaki']

----------------------------------------------------------------------
Ran 1 test in 8.901s

```

やはりエラーが出てしまいました。ポイントは追加されたアイテムを数え上げることですが、
機能テストをパスする最速の方法は`1: `を追加することです。

```html
<table id="id_list_table">
    <tr><td>1: {{ new_item_text }}</td></tr>
</table>
```

これで機能テストを実行すると`self.fail("Finish the test!")`となり、機能テストは(とりあえずは)実行できました。

機能テストがパスできたので、新たに機能テストを更新します。

```python
# django-tdd/functional_tests.py

[...]

# テキストボックスは引続きアイテムを記入することができるので、
# 「どら焼きのお金を請求すること」を記入した(彼はお金にはきっちりしている)
inputbox = self.browser.find_element_by_id('id_new_item')
inputbox.send_keys("Demand payment for the dorayaki")
inputbox.send_keys(Keys.ENTER)
time.sleep(1)

# ページは再び更新され、新しいアイテムが追加されていることが確認できた
table = self.browser.find_element_by_id('id_list_table')
rows = table.find_elements_by_tag_name('tr')
self.assertIn('1: Buy dorayaki', [row.text for row in rows])
self.assertIn('2: Demand payment for the dorayaki',
[row.text for row in rows])

# のび太はこのto-doアプリが自分のアイテムをきちんと記録されているのかどうかが気になり、
# URLを確認すると、URLはのび太のために特定のURLであるらしいことがわかった
self.fail("Finish the test!")

# のび太は一度確認した特定のURLにアクセスしてみたところ、

# アイテムが保存されていたので満足して眠りについた。

[...]

```

これを実行してみましょう。

```sh
$ python functional_tests.py

======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 56, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('1: Buy dorayaki', [row.text for row in rows])
AssertionError: '1: Buy dorayaki' not found in ['1: Demand payment for the dorayaki']

----------------------------------------------------------------------
Ran 1 test in 13.815s
```

やはり`id_list_table`においてitemを数え上げられていないことが原因で機能テストがパスできないようです。

機能テストを更新したのでコミットしておきます。

```sh
$ git commit -a
```
