import os
from collections import deque
from flask import Flask, request
import requests
import openai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
depth = os.getenv("MESSAGE_DEPTH")

@app.route('/bot', methods=['POST'])
def bot():
    print(request.values)
    in_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()

    # response = openai.Completion.create(
        # engine="ada",
        # prompt="You: What have you been up to?\nFriend: Watching old movies.\nYou: Did you watch anything interesting?\nFriend:",
        # temperature=0.4,
        # max_tokens=60,
        # top_p=1.0,
        # frequency_penalty=0.5,
        # presence_penalty=0.0,
        # stop=["Bot:"]
    # )

    msg.body(f"Jo")
    return str(resp)


if __name__ == '__main__':
    app.run()