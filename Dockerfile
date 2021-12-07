FROM 736487896839.dkr.ecr.eu-west-2.amazonaws.com/python:3.8-alpine
RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

RUN apk add curl openssl bash --no-cache
RUN curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl

COPY . .
EXPOSE 8087
ENTRYPOINT [ "python", "bot.py"]
