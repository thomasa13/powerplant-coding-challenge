FROM python:3.12-slim-bookworm
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV DEBUG=False
ENV PORT=8888
ENV HOST=0.0.0.0
EXPOSE 8888
CMD ["python", "app.py"] 