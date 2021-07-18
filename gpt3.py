import os
from collections import deque, defaultdict
from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
depth = int(os.getenv("MESSAGE_DEPTH"))
users = defaultdict(lambda: deque(maxlen=depth * 2 + 1))


@app.route("/bot", methods=["POST"])
def bot():
    in_msg = request.values.get("Body", "")
    user_id = request.values.get("WaId", "random")

    users[user_id].append(f"User: {in_msg}")
    resp = MessagingResponse()
    msg = resp.message()

    chat = "\n".join(users[user_id]) + "\nBot:"

    response = openai.Completion.create(
        engine="ada",
        prompt=chat,
        temperature=0.4,
        max_tokens=50,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["Bot:"],
    )
    text = response["choices"][0]["text"].split("\n", maxsplit=1)[0]
    users[user_id].append(f"Bot: {text}")

    msg.body(f"{text}")
    return str(resp)


if __name__ == "__main__":
    app.run()
