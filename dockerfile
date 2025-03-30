FROM python:3.11-slim

WORKDIR /TranslationApp

RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm -v && node -v


COPY server/ server/
COPY requirements.txt .
COPY server/run.sh server/run.sh


COPY client/ client/

COPY setup.sh setup.sh


RUN pip install -r requirements.txt
RUN cd client/transpiler/ && npm install


RUN chmod +x server/run.sh
RUN chmod +x setup.sh


EXPOSE 5000
EXPOSE 3000


ENTRYPOINT [ "./setup.sh" ]
# CMD bash -c "bash server/run.sh & cd client && npm run dev"
