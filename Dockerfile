FROM python:3.8

WORKDIR /app
ADD main.py .
ADD style.py .
ADD /src ./src
ADD /tmp ./tmp

RUN pip install streamlit 
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]