docker run -d -p 5672:5672 rabbitmq

pip install -r requirements.txt

celery -A tasks worker --loglevel=INFO