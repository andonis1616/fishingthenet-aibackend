# Using lightweight alpine image
FROM python:3.10

# Installing packages
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/app
# COPY Pipfile Pipfile.lock script.sh ./
COPY . .

ENV FLASK_APP=main.py

# Install API dependencies
RUN pipenv install --system --deploy 

# Start app
EXPOSE 8000
CMD ["pipenv", "run", "flask", "--debug", "run", "-h", "0.0.0.0", "-p", "8000"]
