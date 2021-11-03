FROM python:slim

WORKDIR /robot 
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "instarobot.py"]
