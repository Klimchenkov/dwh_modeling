FROM python:3.10.5
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY ./backend/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt --no-cache-dir

COPY ./backend /backend

EXPOSE 5000

CMD ["python", "app.py"]