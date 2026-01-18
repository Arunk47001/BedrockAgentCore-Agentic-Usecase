FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt .

RUN pip3 install --upgrade pip

# install dependencies
RUN pip3 install -r requirements.txt


COPY src/ /var/task/src/

CMD ["src/main.handler"]


