FROM public.ecr.aws/lambda/python:3.8

COPY . ${LAMBDA_TASK_ROOT}
COPY ./utils ${LAMBDA_TASK_ROOT}/utils

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip install awscli

CMD [ "api.lambda_handler" ]