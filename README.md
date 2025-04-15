# Установка зависимостей

pip install -r requirements.txt

# Запуск

python main.py ip1,ip2

После этого скрипт 

- Получит нагрузку серверов (через команду uptime).

- Выберет сервер с наименьшей нагрузкой.

- Определит второй сервер как peer_host.

- Запустит playbook Ansible, передав целевые переменные.


# Принятые решения и возникшие вопросы

## Оценка нагрузки

Для оценки нагрузки Использована команда `uptime` и разбор среднего значения нагрузки для выбора наименее загруженного сервера.

## Подключение и установка PostgreSQL

Для Debian используется `apt`, для CentOS – `yum`. Дополнительно для CentOS производится инициализация базы данных через `postgresql-setup`.

## Настройка подключения

В PostgreSQL изменен параметр `listen_addresses` на *, чтобы база принимала внешние подключения. Для контроля доступа используется настройка файла `pg_hba.conf`, где добавлено правило: пользователь student может подключаться только с IP-адреса второго сервера (peer_host), а для всех остальных пользователей разрешены подключения с любого IP. Для пользователя student дополнительно прописано правило reject для всех других диапазонов, что гарантирует нужное поведение.
