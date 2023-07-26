# RAII_AI_Support

## Описание проекта:  
Проект представляет из себя реализацию нейронной сети [RoBERTa](https://huggingface.co/docs/transformers/model_doc/roberta) дообученной на [наборе данных](https://github.com/v4ndi/RAII_AI_Support/tree/main/training_model_and_dataset) службы поддержки онлайн-магазина. Сам алгоритм классифицирует текстовые данные на английском языке по 11 классам. Прием обращений осуществляется через интрфейс телеграмм-бота [main.py](https://github.com/v4ndi/RAII_AI_SupportV_2/blob/main/src/main.py). Вторым приложением в проекте выступает веб-сервис, реализованный не фреймворке Flask, исходником для запуска локального сервера и приложения является [app.py](https://github.com/v4ndi/RAII_AI_SupportV_2/blob/main/src/app.py). Веб-сервис предостовляет возможность просмотра всех обращений, сортировки их по дате, статусу и типу. Также немаловажным является возможность ответить на обращение и просмотреть статистику количества обращений и их типа за последний месяц.  
Основная логика связи первого и второго приложения это то, что они связаны с одной базой данных. Одино необходимо для добавления обращений в БД, а другое для просмотра и аналитики.

## Скриншоты проекта
<image src="/img/main_page_example.png" alt="Главная страница веб-интерфейса">
<image src="/img/stats_web_example.png" alt="Страница со статистикой веб-интерфейса">
<image src="/img/Telegram_interface.png" alt="Интерфейса телеграмм для приема обращений в службу поддержки">

## Сборка и запуск проекта
1. Скачать папку binary_files и положить ее в директирию в ту же, где лежит src [ссылка на гугл драйв](https://drive.google.com/drive/folders/1Z1I8zdrQaM1V76g6IMhsXjKADshBYK2J?usp=sharing)
2. 
