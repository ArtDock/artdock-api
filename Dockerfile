FROM python:3.9-slim
ENV APP_HOME /app
ARG PORT=80
ENV PORT=${PORT}
ENV PYTHONPATH /app

WORKDIR $APP_HOME
COPY . ./
COPY /app .
RUN apt-get update && apt-get install -y build-essential
RUN python -m venv venv && \
    /bin/bash -c "source venv/bin/activate && pip install -r requirements.txt"
CMD exec venv/bin/gunicorn --bind :${PORT} --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app