FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends tzdata ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY moneypenny.py /app/moneypenny.py
RUN useradd --create-home runner
USER runner
CMD ["python", "-u", "moneypenny.py"]
