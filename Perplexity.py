import configparser
import requests
from openai import OpenAI

class Perplexity():
    def __init__(self,config_ = './config.ini'):
        if type(config_) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        elif type(config_) == configparser.ConfigParser:
            self.config = config_

    def submit(self, message):
        conversation = [{"role": "user", "content": message}]
        client = OpenAI(api_key = self.config['PERPLEXITY']['API_KEY'], base_url="https://api.perplexity.ai")
        response = client.chat.completions.create(model = "mistral-7b-instruct", messages = conversation,)
        return response.choices[0].message.content

if __name__ == '__main__':
    Perplexity_test = Perplexity()

    while True:
        
        user_input = input("Typing anything to GPT:\t")
        response = Perplexity_test.submit(user_input)
        print(response)
