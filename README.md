# Mini-Rag-App

## Requirements
pip install -r requirements.txt

## Run Docker Compose Service
cd docker
cp .env .env.example

update .env with you credentials
## to run app
uvicorn main:app --reload --host 0.0.0.0 --port 5000 
ip addr show eth0 
