# LogoSearchBot
This is bot on Telegram that can search logos on photo

To deploy this bot on your local machine you need to have **python 3.11** and **PostgreSQL 15.5** and at first clone this repo

```git clone https://github.com/muzy4ukV/LogoSearchBot.git```

Then clone **yolov5** repo and install all necessary packages for it

```git clone https://github.com/ultralytics/yolov5.git```

In project folder create a virual enviroment and activate it

```
python -m venv .venv
.venv/Scripts/activate/
```

Install all requirements from requirements.txt to it

```pip install -r requirements.txt```

Create database

> createdb -U postgres -h localhost -p 5432 LogoSearchBotDB

Add the table to it

> psql -U postgres -h localhost -p 5432 -d LogoSearchBotDB -a -f script.sql

Create an .env file with this sctructure

| Variable name | Value | Example |
| -------- | ------- | ------- |
| BOT_TOKEN | Token from Telegeam API | bot123456:ABCDEF1234ghIklzyx57W2v1u123ew11 |
| DB_USER | DB user name | postgres |
| DB_PASSWORD | Password to DB | Qwert12345 |
| DB_HOST | Name of host | localhost |
| DB_PORT | Port | 5432 |
| DB_NAME | Name of db | LogoSearchBotDB |
| WAIT_TIME_SETTINGS | Delay for correct processing of photo albums | 2 |
| NUM_OF_REQUESTS_TO_HIDE_MSG | The number of requests after which the message is hidden | 3 |
| MAX_MEDIA_SIZE_BYTES | Maximum bytes for files | 15728640 |

Finally you need to run ***main.py*** file

```python main.py```
