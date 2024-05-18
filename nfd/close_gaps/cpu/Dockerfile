FROM python:3.9-slim

RUN pip install psutil kubernetes

COPY set_nfd_cpu_labels.py /set_nfd_cpu_labels.py

ENTRYPOINT ["python", "/set_nfd_cpu_labels.py"]
