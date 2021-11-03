FROM python:slim

RUN pip install -r requirements.txt
WORKDIR /robot 
COPY . .
ENTRYPOINT ["python", "instarobot.py"]
