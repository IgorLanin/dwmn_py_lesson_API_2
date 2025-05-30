# Обрезка ссылок с помощью VK API

Скрипт сокращает ссылку через VK API и возвращает обрезанную ссылку. Если передать обрезанную ссылку, скрипт вернет количество переходов по ней.


### Как установить

Для работы скрипта понадобится сервисный токен приложения VK API ("Сервисный ключ доступа"). 
Прочитать, что такое [сервисный токен](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/tokens/service-token).
Порядок действий: 
1. Авторизоваться/зарегистрироваться на сайте [vk.com](https://vk.com/).
2. Согласно [инструкции](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/create-application) создать приложение.
   В процессе создания приложения можно указать следующие данные:
   - Тип приложения - Web
   - Базовый домен - example.com
   - Доверенный Redirect URL - https://example.com

После создания приложения, токен можно будет найти в созданном приложении:

![image](https://github.com/user-attachments/assets/10b38281-d3e0-4331-98ee-e72dbd7dc0a4)

Токен понадобится добавить в ```.env``` - файл в переменную ```VK_ID_TOKEN```.

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Рекомендуется использовать [virtualenv](https://pypi.org/project/virtualenv/)/venv для изоляции проекта.


### Работа скрипта в командной строке

Для работы со скриптом необходимо указать запрос в командной строке в формате: ```python  название_скрипта ссылка```

Пример работы команды ```python main.py https://github.com/IgorLanin```:

![image](https://github.com/user-attachments/assets/6f8e6a81-7842-429c-9436-f9a2e0ac0eef)

Если передать обрезанную ссылку, выведется количество переходов по ней:

![image](https://github.com/user-attachments/assets/9b2c6f4a-c859-4226-936c-0475595d61db)



### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
