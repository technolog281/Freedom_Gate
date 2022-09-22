# Freedom_Gate
Alpha version of proxy handler

1. На данный момент сервис в разработке, пока что умеет только парсить hidemy.name и сохранять весь список прокси в БД MongoDB.
  При повторном добавлении выдаёт в лог "It seems that dictionary in MongoDB yet, update document, wait..." и обновляет поулченные данные в БД.


Дальнейшая судьба проекта:
  1. Планируется перейти с Selenium на Playwright.
  2. Добавить сайтов с прокси-листами для обработки (хотя бы 10, дальше посмотрим)
  3. Стандартизация JSON-объектов попадающих в БД, разделение по типу прокси:
    1. HTTP
    2. HTTPS
    3. Socks 4
    4. Socks 5
  4. Добавить сервис проверки прокси по заданным параметрам и закинуть его в cron: 
    1. Стандартный Ping (время ответа)
    2. Проверка работы сокета (вопрос реализации, проверка открыт ли порт, на который мы ломимся)
    3. Проверка доступа основного набора сайтов через этот прокси (список сайтов будет задаваться в yml-файле)
  5. Завернуть весь сервис в Docker-контейнеры.
  6. Добавить возможность работы с сервисом через Telegram-бота, схема получения запросов / отправки ответов пока смутно, но представляется.
  7. Прикрутить web-интерфейс бота через Django, с возможностью фильтрации прокси, online-теста отклика и доступности сайтов (указание в web-интерфейсе)
  8. Создать desktop-версию сервиса для работы в автоматическом режиме (включил сервис - он передал в конфиг системы новый прокси, в случае отказа прокси - автообновление)
      С реализацией desktop-версии пока всё плохо, даже не представляю, возможна ли работа из скрипта с системными настройками, но это в последнюю очередь.
      
      
На этом пока всё, ждите новостей :)
