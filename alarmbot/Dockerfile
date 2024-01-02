FROM public.ecr.aws/lambda/python:3.9

# Copy requirements.txt
COPY src/ ${LAMBDA_TASK_ROOT}/src

# Install the specified packages
RUN pip install --upgrade pip && pip install -e src

# Copy all files in ./app
COPY app.py ${LAMBDA_TASK_ROOT}/app.py

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]