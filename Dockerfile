FROM python:3.8-alpine
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt
COPY . .
# DON'T FORGET TO EXCLUDE ALL THE TEST FILES IN DOCKER IGNORE
EXPOSE 8087
ENTRYPOINT [ "python", "bot.py"]