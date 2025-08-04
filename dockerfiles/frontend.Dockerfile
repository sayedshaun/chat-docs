# docker/frontend.Dockerfil

FROM python:3.10-slim

WORKDIR /app

RUN pip install streamlit==1.47.0
RUN pip install requests==2.32.4
RUN pip install python-dotenv==1.1.1

COPY . .