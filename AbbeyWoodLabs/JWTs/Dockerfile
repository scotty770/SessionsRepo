FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget curl unzip gnupg chromium-driver chromium && \
    pip install flask selenium pyjwt
    
COPY app /app
COPY bot /bot
COPY run.sh .

RUN chmod +x run.sh

EXPOSE 3000

CMD ["sh", "run.sh"]

