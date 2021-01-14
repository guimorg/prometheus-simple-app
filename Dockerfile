FROM python:3.7-alpine AS requirements_builder

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN apk add --no-cache \
    gcc \
		libc-dev \
		linux-headers \
		bash && \
		python3 -m pip install -U wheel virtualenv pip && \
		python3 -m virtualenv venv && \
		venv/bin/python3 -m pip install -r requirements.txt

FROM python:3.7-alpine
WORKDIR /app

RUN apk add --no-cache \
    bash \
		gcc

COPY --from=requirements_builder /app/venv /app/venv
COPY . /app

ENV PATH="/app/venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/venv"

EXPOSE 5000
VOLUME /app
CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0:5000", "application:application"]
