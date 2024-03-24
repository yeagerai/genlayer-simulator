# To build GenVM Image

FROM python:3.11-slim

WORKDIR /usr/src/app

RUN mkdir /genvm

COPY . ./genvm

RUN pip install --no-cache-dir -r genvm/requirements.txt

EXPOSE 80 11434

ENV NAME GenVM
ENV PYTHONPATH "${PYTHONPATH}:/genvm"

CMD ["python", "/genvm/contract_execution.py"]