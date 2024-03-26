FROM python
WORKDIR /APP
COPY chatbot.py /APP/
COPY Firebase.py /APP/
COPY requirements.txt /APP/
COPY Perplexity.py /APP/
COPY comp7940-797cf-firebase-adminsdk-k9zfo-457c0104e5.json /APP/

RUN pip install pip update
RUN pip install -r requirements.txt

ENV ACCESS_TOKEN=6092016938:AAGJTW--MIaB4Q2GcRio8L1TVDDmg0OWMZI
ENV API_KEY=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

CMD python chatbot.py
