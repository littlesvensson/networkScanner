FROM python:3.10.4
COPY . ./
CMD ["python","./scanner.py"]