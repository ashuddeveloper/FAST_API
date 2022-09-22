pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-dotenv

docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head

docker-compose build
docker-compose up

'''
uid generator 

Get Json data from API body 
Add it to Queue
From another container get json data and add to postgresql
Send back the record id back to user


Create 2 queues 
app -> consumer
consumer -> reciver

1st queue json data with task id 
2nd queue task id and record id/ Error


'''