# Сокращение ссылок с помощью Bitly

Скрипт сокращает ссылку при помощи сервиса Bitly или выводит количество переходов по ней, если была введена уже сокращенная ссылка.

## Установка

1. Нужно зарегистрироваться на сайте [bitly.com](https://bitly.com/) для получения токена к API Bitly. После регистрации токен можно сгенерировать по [ссылке](https://bitly.com/a/oauth_apps), достаточно получить `GENERIC ACCESS TOKEN`.

2. В директории приложения создать файл настроек `.env` с содержимым:
```#!bash

BITLY_GENERIC_ACCESS_TOKEN=полученный_от_bitly_токен

```

3. Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```#!bash

pip install -r requirements.txt

```

## Запуск

```#!bash

$ python3 main.py <link>

```

### Пример запуска с длинной ссылкой
```#!bash

$ python3 main.py https://www.google.com/

```

Результат работы скрипта
```#!bash

http://bit.ly/2SjxUR5

```

### Пример запуска с уже сокращенной ссылкой
```#!bash

$ python3 main.py http://bit.ly/2SjxUR5

```

Результат работы скрипта
```#!bash

Количество переходов по ссылке: 1

```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
