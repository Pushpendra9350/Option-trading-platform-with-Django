Option trading application to place realtime order with stock price simulation 


### Video Demo: https://www.youtube.com/watch?v=M1monefFIdg

#### Screenshot
<img width="1435" alt="Screenshot 2022-10-26 at 10 36 17 PM" src="https://user-images.githubusercontent.com/43174363/198102165-36078d1e-69d6-4e31-89a2-dc06a485f4ea.png">

#### Simple Architecture
![Group 130](https://user-images.githubusercontent.com/43174363/198601499-b072db4d-383d-4f14-9db8-d25128de7570.png)

##### To run the project server
```git
python manage.py runserver
```

##### To run the celery
```git
celery -A StockPortal.celery worker -l INFO
```

##### To run the websocket
```git
python manage.py runserver 8080
```

##### To run the redis service
```git
brew services start redis
```
