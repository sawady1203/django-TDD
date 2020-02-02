# Djangoでテスト駆動開発 その3

これはDjangoでテスト駆動開発(Test Driven Development, 以下:TDD)を理解するための学習用メモです。

参考文献は[**Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript (English Edition) 2nd Edition**](https://www.amazon.co.jp/dp/B074HXXXLS/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)を元に学習を進めていきます。

本書ではDjango1.1系とFireFoxを使って機能テスト等を実施していますが、今回はDjagno3系とGoogle Chromeで機能テストを実施していきます。また一部、個人的な改造を行っていますが(Project名をConfigに変えるなど、、)、大きな変更はありません。

⇒⇒[その1](https://qiita.com/komedaoic/items/dd7abd24961250208c7c)はこちら
⇒⇒[その2](https://qiita.com/komedaoic/items/58dc509e8f681da73199)はこちら

## Part1. The Basics of TDD and Django

### Capter3. Testing as Simple Home Page with Unit Tests

Chapter2では機能テストをUnittestを使って記述し、ページタイトルに”To-DO”があるかどうかをテストしました。
今回は実際にアプリケーションを開始してTDDしていきます。

#### Our First Django App, and Our First Unit Test

Djangoは1つのプロジェクト下にいくつかのアプリケーションを構築させる形と取っています。
さっそくDjangoのアプリケーションを作成していきましょう。
ここでは**lists**という名前のアプリケーションを作成します。

```sh
$ python manage.py startapp lists
```

#### Unit Tests, and How They Differ from Functional Tests

機能テスト(Functional Tests)はアプリケーションを外側から(ユーザー視点で)見て機能しているのかどうかをテストしているのに対して、
単体テスト(Unit Tests)はアプリケーションを内側から(開発者視点で)機能しているのかをテストしています。
TDDは機能テスト、単体テストをカバーすることが求められており、開発手順は下記のようになります。

**step1.** 機能テストを書く(ユーザー視点から新しい機能を説明しながら)。

**step2.** 機能テストが失敗したらテストをパスするにはどうコードを書いたら良いのかを考える(いきなり書かない)。
自分の書いたコードがどう振舞って欲しいのかを単体テストを追加して定義する。

**step3.** 単体テストが失敗したら、単体テストがパスする最小のアプリケーションコードを書く。

**step4.** step2とstep3を繰り返して機能テストがパスかどうかを確認する。

#### Unit Testing in Django

ホームページのviewのテストを書いてみるためにlists/tests.pyを確認してみましょう。

```python
# lists/tests.py

from django.test import TestCase

# Create your tests here.
```

これを見るとDjangoが提供するTestCaseクラスを使ってDjangoの単体テストを書くことができることがわかりました。
djagno.test.TestCaseは機能テストで使った標準モジュールであるunittest.TestCaseを拡張したものです。
試しに単体テストを書いてみます。

```python
# lists/tests.py

from django.test import TestCase


class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)

```

Djangoには各アプリケーションのテストを探してテストを実行するテストランナー機能があります。
Djangoのテストランナーを起動してみましょう。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F
======================================================================
FAIL: test_bad_maths (lists.tests.SmokeTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\--your_pass--\django-TDD\lists\tests.py", line 9, in test_bad_maths
    self.assertEqual(1 + 1, 3)
AssertionError: 2 != 3

----------------------------------------------------------------------
Ran 1 test in 0.005s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

lists/tests.pyが実行されてFailedしていうのが確認できました。ここでコミットしておきます。

```sh
$ git status
$ git add lists
$ git commit - m
$ git commit -m "Add app for lists, with deliberately failing unit test"
```

#### Django's MVC, URLs, and View Functions

Djangoはユーザーからの特定のURLに対して何をするべきなのかを決定しておく必要があります。
Djangoのワークフローは次のようになっています。

1. HTTP/requestが特定のURLにくる

2. HTTP/requestに対してどのviewを実行するべきなのかルールが決められているのでルールにしたがってviewを実行する。

3. viewはrequestを処理してHTTP/responseを返す。

したがって、我々が行うことは次の2点です。

1. URLとViewの紐づけ(resolve the URL)ができるか

2. Viewは機能テストをパスすることができるHTMLを変えることができるのか

それではlists/tests.pyを開いて小さなテストを書いてみましょう。

```python
# lists/tests.py

from django.urls import resolve  # 追加
from django.test import TestCase
from lists.views import home_page  # 追加

class SmokeTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

```

`django.urls.resolve`はdjangoが内部で使用しているURLを解決するためモジュールです。
`from lists.views import home_page`は次に記述する予定のviewです。これを次に記述することがわかります。
それではテストしてみます。

```sh
$ python manage.py test

System check identified no issues (0 silenced).
E
======================================================================
ERROR: lists.tests (unittest.loader._FailedTest)
----------------------------------------------------------------------
ImportError: Failed to import test module: lists.tests
Traceback (most recent call last):
  File "C:\--your_user_name--\AppData\Local\Programs\Python\Python37\lib\unittest\loader.py", line 436, in _find_test_path
    module = self._get_module_from_name(name)
  File "C:\--your_user_name--\AppData\Local\Programs\Python\Python37\lib\unittest\loader.py", line 377, in _get_module_from_name
    __import__(name)
  File "C:\--your_path--\django-TDD\lists\tests.py", line 5, in <module>
    from lists.views import home_page
ImportError: cannot import name 'home_page' from 'lists.views' (C:\Users\--your_path--\django-TDD\lists\views.py)


----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
```

ImportErrorが出現しました。内容をみると`lists.views`から`home_page`がimportできないと教えてくれています。
それでは`lists.views`に`home_page`を記述してみましょう。

```python
# lists/views.py

from django.shortcuts import render

home_page = None
```

なにかの冗談みたいですがこれでImportErrorは解決できるはずです。TDDはエラーを解決する最小のコードを書いていくお気持ちを思い出しましょう。

もう一度テストしてみます。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
E
======================================================================
ERROR: test_root_url_resolve_to_home_page_view (lists.tests.SmokeTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\--your_path--\django-TDD\lists\tests.py", line 10, in test_root_url_resolve_to_home_page_view
    found = resolve('/')
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\django\urls\base.py", line 25, in resolve
    return get_resolver(urlconf).resolve(path)
  File "C:\--your_path--\django-TDD\venv-tdd\lib\site-packages\django\urls\resolvers.py", line 575, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
django.urls.exceptions.Resolver404: {'tried': [[<URLResolver <URLPattern list> (admin:admin) 'admin/'>]], 'path': ''}

----------------------------------------------------------------------
Ran 1 test in 0.005s

FAILED (errors=1)
Destroying test database for alias 'default'...

```

確かに`ImportError`は解決しましたが、次もテストが失敗しました。Tracebackを確認すると`'/'`を`resolve`が解決してもDjangoが404エラーを返すことが分かります。つまり、Djangoが`'/'`を解決できていないという意味になります。

#### urls.py

DjangoにはURLとViewをマッピングするurls.pyが存在します。config/urls.pyがメインのurls.pyになります。こちらを確認してみましょう。

```python
# config/urls.py

"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

```

中身を確認すると`"config URL Configuration"`というURLマッピングの書き方が書かれているので参考にします。
今回はFunciton viewsの書き方で`"/"`と`home_page`のマッピングを`urlpatterns`に追加してみましょう。
また、`admin/`はまだ使用しないのでコメントアウトしておきます。

```python
# config/urls.py

from django.contrib import admin
from django.urls import path
from lists import views


urlpatterns = [
    # path('admin/', admin.site.urls),  # コメントアウト
    path('', views.home_page, name='home')
]
```

マッピングができました。テストをします。

```sh
$ python manage.py test
[...]
TypeError: view must be a callable or a list/tuple in the case of include().
```

URLのマッピングを追加したので`404エラー`は解決されましたが、`TypeError`が発生しました。
これは`lists.view`から`home_page`を呼んでも`home_page = None`で何も返ってこなかったためだと思われます。
lists/views.pyを編集してこれを解決しましょう。

```python
# lists/views.py

from django.shortcuts import render

def home_page():
    pass
```

テストしてみます。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK
Destroying test database for alias 'default'...
```

単体テストをパスできました。ここでコミットしておきます。

```sh
$ git add .
$ git status
$ git commit -m "First unit test and url mapping, dummy view"
```

現在のlists/views.pyが実際にHTMLを返しているのかどうかをテストできるようにlists/tests.pyを書き換えていきます。

```python
# lists/tests.py

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page


class SmokeTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_current_html(self):  # 追加
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith.('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endwith('</html>'))
```

`test_root_url_resolve_to_home_page_view`はURLマッピングが正確にできていのかどうかを確認していますが、
`test_home_page_returns_current_html`で正確なHTMLが返せているのかどうかを確認しています。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
E.
======================================================================
ERROR: test_home_page_returns_current_html (lists.tests.SmokeTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\--your_path--\django-TDD\lists\tests.py", line 18, in test_home_page_returns_current_html
    response = home_page(request)
TypeError: home_page() takes 0 positional arguments but 1 was given

----------------------------------------------------------------------
Ran 2 tests in 0.005s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

`TypeError`が出ました。内容を確認すると`home_page() takes 0 positional arguments but 1 was given`とあるので
`home_page()`の定義では引数が指定されていない(0 positional arguments)が、引数が与えられてて(1 was given)おかしいということがわかります。

ということでlists/views.pyを書き換えたいと思います。

```python
# lists/views.py

from django.shortcuts import render


def home_page(request):  # 変更
    pass
```

home_page()関数に引数`request`を追加しました。これでテストをしてみます。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
E.
======================================================================
ERROR: test_home_page_returns_current_html (lists.tests.SmokeTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\--your_path--\django-TDD\lists\tests.py", line 19, in test_home_page_returns_current_html
    html = response.content.decode('utf8')
AttributeError: 'NoneType' object has no attribute 'content'

----------------------------------------------------------------------
Ran 2 tests in 0.005s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

`TypeError`は解決しましたが、次は`AttributeError`が発生しました。
`'NoneType' object has no attribute 'content'`とあるので`home_page(request)`の戻り値がNoneとなっているのが原因のようです。
lists/views.pyを修正します。

```python
# lists/views.py

from django.shortcuts import render
from django.http import HttpResponse  # 追加


def home_page(request):
    return HttpResponse()
```

`django.http.HttpResponse`を返すように修正しました。テストしてみましょう。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F.
======================================================================
FAIL: test_home_page_returns_current_html (lists.tests.SmokeTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\--your_path--\django-TDD\lists\tests.py", line 20, in test_home_page_returns_current_html
    self.assertTrue(html.startswith('<html>'))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 2 tests in 0.005s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

`AttributeError`は解決して`AssertionError`が発生しました。`html.startwith('<html>')`がFalseであるために`False is note ture`というメッセージがでているのがわかります。
lists/views.pyを修正します。

```python
# lists/views.py

from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html>')  # 変更
```

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F.
======================================================================
FAIL: test_home_page_returns_current_html (lists.tests.SmokeTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\--your_path--\django-TDD\lists\tests.py", line 21, in test_home_page_returns_current_html
    self.assertIn('<title>To-Do lists</title>', html)
AssertionError: '<title>To-Do lists</title>' not found in '<html>'

----------------------------------------------------------------------
Ran 2 tests in 0.005s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

同じく`AssertionError`です。`'<title>To-Do lists</title>'`が見つからないとのことです。
lists/views.pyを修正します。

```python
# lists/views.py

from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title>')  # 変更
```

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F.
======================================================================
FAIL: test_home_page_returns_current_html (lists.tests.SmokeTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\--your_path--\django-TDD\lists\tests.py", line 22, in test_home_page_returns_current_html
    self.assertTrue(html.endswith('</html>'))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 2 tests in 0.013s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

同じく`AssertionError`です。`'</html>'`が見つからないとのことです。
lists/views.pyを修正します。

```python
# lists/views.py

from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title></html>')  # 変更
```

これでようやくうまくいくはずです。

```sh
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.004s

OK
Destroying test database for alias 'default'...
```

うまくいきました。単体テストがパスできたので開発サーバーを立ち上げてから機能テストを実行してみましょう。

```sh
# 開発サーバーの立ち上げ
$ python manage.py runserver

# 別のcmdを立ち上げて機能テストを実行
$ python functional_tests.py

DevTools listening on ws://127.0.0.1:51108/devtools/browser/9d1c6c55-8391-491b-9b14-6130c3314bba
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 21, in test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 1 test in 7.244s

FAILED (failures=1)
```

機能テストはFAILEDとなっていますが、これは`unittest.TestCase`の`.fail`を使ってテストをパスしても必ずエラーを発生させるようにしているためでした。
したがって、機能テストがうまくいったことが確認できます！

コミットしておきましょう。


