FROM python:3.10.4
COPY scanner.py ./
CMD ["python","./networkScanner.py"]