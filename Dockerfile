FROM public.ecr.aws/lambda/python:3.8

# Copy app code
COPY ./app ${LAMBDA_TASK_ROOT}

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["api_handler.handler"]