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
  File "C:\~~pass~~\django-TDD\lists\tests.py", line 9, in test_bad_maths
    self.assertEqual(1 + 1, 3)
AssertionError: 2 != 3

----------------------------------------------------------------------
Ran 1 test in 0.005s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

lists/tests.pyが実行されてFailedしていうのが確認できました。ここでコミットしておきます。


