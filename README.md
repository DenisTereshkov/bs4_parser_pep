[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Practicum.Yandex](https://img.shields.io/badge/-Practicum.Yandex-464646?style=flat&logo=Practicum.Yandex&logoColor=56C0C0&color=008080)](https://practicum.yandex.ru/)
# Парсер документации python и PEP
## Описание
Парсер информации о python с **https://docs.python.org/3/** и **https://peps.python.org/**
## Установка:
### Клонируйте репозиторий
### Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
venv\Scripts\activate
```
### Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
### Перейдите в деррикторию ./src
```
cd src/
```
### запустите файл main.py выбрав необходимый парсер и аргументы(приведены ниже)
```
python main.py [функция парсера] [аргументы]
```
### Чтобы получить информацию о командах в терминале.
```
python main.py -h
```
### Функции парсера
- pep
Парсер выводящий список статусов документов pep
и количество документов в каждом статусе. 
```
python main.py pep
```
- whats-new   
Парсер выводящий список изменений в python.
```
python main.py whats-new
```
- latest_versions
Парсер выводящий список версий python и ссылки на их документацию.
```
python main.py latest-versions
```
- download   
Парсер скачивающий архив с документацией.
```
python main.py download
```

### Аргументы
- -o {pretty,file}, --output {pretty,file}   
Дополнительные способы вывода данных   
pretty - выводит данные в командной строке в таблице  
```
python main.py [функция парсера] --output pretty
``` 
file - сохраняет информацию в формате csv в папке ./results/
```
python main.py [функция парсера] --output file
```