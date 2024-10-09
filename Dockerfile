FROM python:3.12.4-alpine

EXPOSE 8001

COPY . /fast_api_poc
RUN python -m venv fapi_env
RUN source fapi_env/bin/activate
WORKDIR /fast_api_poc
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]