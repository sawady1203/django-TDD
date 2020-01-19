# Djangoでテスト駆動開発 1

これはDjangoでテスト駆動開発(Test Driven Development, 以下:TDD)を理解するための学習用メモです。

参考文献は[**Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript (English Edition) 2nd Edition**](https://www.amazon.co.jp/dp/B074HXXXLS/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)を元に学習を進めていきます。


## 仮想環境の構築

```sh
# 仮想環境の作成
$ python -m venv venv-tdd

# 仮想環境の有効化
$ venv-tdd/Script/activate

# pipとsetuptoolsのアップデート
$ python -m pip install --upgrade pip setuptools

# DjangoとSeleniumのインストール
$ pip install django selenium
    installing collected packages: sqlparse, pytz, asgiref, django, urllib3, selenium
    Successfully installed asgiref-3.2.3 django-3.0.2 pytz-2019.3 selenium-3.141.0 sqlparse-0.3.0 urllib3-1.25.7
```

Google Chromeを使って機能テストを実施するので、Google ChromeのWebドライバーをダウンロードする。

Google Chromeバージョン: 79.0.3945.130（Official Build） （64 ビット）なので、
Google Chrome Driverは[ChromeDriver 79.0.3945.16](http://chromedriver.chromium.org/downloads)をダウンロードした。





## Part1. The Basics of TDD and Django

### Chapter1. Geeting Django Set Up Using a Functional Test

Websiteを作成することを決めたとき、通常の最初のステップはweb-frameworkをインストールして設定を書き換えて、、と進めていくが、TDDでは必ずテストを最初に書く。

TDDの開発サイクルは、下記を徹底することである。

- テストを書く
- テストを実行して失敗することを確認する。
- テストが成功するようにコードを書く。

最初に我々が確認したいことは、、、

- 確認事項
  - Djangoがインストールされていて、問題なく働くこと。

- 確認方法
  - ローカルでDjangoの開発用サーバーが確認できること。

これを実施するためにSeleniumを使ってブラウザを自動で操作させる。

#### 機能テストを書く

functional_tests.pyを作成する。

```python
# django-tdd/functional_tests.py

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

```

これが最初の機能テストとなる。これを実行する。

```sh
$ python functional_tests.py

    Traceback (most recent call last):
    File "functional_tests.py", line 8, in <module>
        assert 'Django' in browser.title
    AssertionError
```

ブラウザがseleniumによって自動で起動されるが、エラーページが表示されるのがわかる。

#### Djagnoを起動する

この機能テストをクリアさせるためにDjagnoプロジェクトを開始して、開発用サーバーを起動する。

```sh
$ django-admin startproject config .

$ python manage.py runserver

    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).

    You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    January 19, 2020 - 15:36:31
    Django version 3.0.2, using settings 'config.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
```

Django(3.0.2)はconfig.settingsを使って開発用サーバ`http://127.0.0.1:8000/`を起動したことがわかる。

ここで別のシェルを起動して仮想環境を有効にした後、機能テストを実行する。

```sh
$ python manage.py functional_tests.py

    DevTools listening on ws://127.0.0.1:54716/devtools/browser/6ddf9ee8-7b35-41f5-8700-d740ef24c8dc
```

この結果、AssertionErrorは表示されず、ブラウザでもエラーは表示されなかった。

機能テストを実行して、Djagnoが確かに機能していることが確認された！！！！

#### Gitレポジトリに登録

TDDはVersion Control Systemとともに進められる。

```sh
$ git init .

$ type nul > .gitignore
```

gitで管理したくないものを.gitignoreで管理する。

```sh
#.gitignore
db.sqlite3
debug.log
/venv-tdd
```

.gitignoreを作成したので、これで変更を追加する。

```sh
$ git add .
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   .gitignore
        new file:   .vscode/settings.json
        new file:   README.md
        new file:   README_Part1.md
        new file:   chromedriver.exe
        new file:   config/__init__.py
        new file:   config/__pycache__/__init__.cpython-37.pyc
        new file:   config/__pycache__/settings.cpython-37.pyc
        new file:   config/__pycache__/urls.cpython-37.pyc
        new file:   config/__pycache__/wsgi.cpython-37.pyc
        new file:   config/asgi.py
        new file:   config/settings.py
        new file:   config/urls.py
        new file:   config/wsgi.py
        new file:   functional_tests.py
        new file:   manage.py
```

ここで変更に加えたくない*hoge.pyc*や、*__pycache__*フォルダなどが変更に追加されてしまった。これを除外させたい。

```sh
$ git rm -r --chashed config/__pycache__ .vscode
```

.gitignoreを編集する

```sh
# .gitignore
db.sqlite3
debug.log
/venv-tdd
.vscode
__pycache__
*.pyc
```

```sh
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   .gitignore
        new file:   README.md
        new file:   README_Part1.md
        new file:   chromedriver.exe
        new file:   config/__init__.py
        new file:   config/asgi.py
        new file:   config/settings.py
        new file:   config/urls.py
        new file:   config/wsgi.py
        new file:   functional_tests.py
        new file:   manage.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   .gitignore
        modified:   README_Part1.md

```

狙い通りにgit statusが修正された。
これでコミットする。

```sh
$ git add .
```

ここで、commitする前に、Djagnoのconfig/settings.pyでのSECRET_KRYなどもgitにコミットさせたくない。

```sh
$ git rm -r --cached config/settings.py
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   .gitignore
        new file:   README.md
        new file:   README_Part1.md
        new file:   chromedriver.exe
        new file:   config/__init__.py
        new file:   config/asgi.py
        new file:   config/urls.py
        new file:   config/wsgi.py
        new file:   functional_tests.py
        new file:   manage.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   README_Part1.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        config/settings.py

```

python-dotenvをつかってシステム変数を.envファイルにまとめてコミットしないようにする。

```sh
$ pip install python-dotenv
```

config/settings.pyを変更

```python
# config/settings.py
"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from dotenv import load_dotenv  # 追加

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = os.path.basename(BASE_DIR)  # 追加

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# .envの読み込み
load_dotenv(os.path.join(BASE_DIR, '.env'))  # 追加

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')  # 変更

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # 変更


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 変更
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
```

この状態で変更を追加して、コミットする。

```sh
$ type nul > .env
```

.envにSECRET_KEYを追加。

```sh
# .env
SECRET_KEY = 'your_secret_key'
```

変更を記録する。

```sh
$ git add .
$ git status
$ git commit -m "first commit!"
```