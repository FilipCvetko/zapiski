FROM python:3.8

WORKDIR /app
ADD main.py .
ADD /src ./src
ADD /tmp ./tmp
ADD /notes ./notes

RUN pip install streamlit 
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]