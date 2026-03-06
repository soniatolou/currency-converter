Hey! This is a project I've been working on as part of my studies to become an AI & Machine Learning Engineer. It actually started out as a course assignment, but I wanted to take it a bit further and make it feel like a "real" tool.

The main goal was to get comfortable working with APIs and handling data in a smart way. Instead of just doing basic calculations, I hooked this up to the **Open Exchange Rates API** so it pulls live, actual data from the web.

### How it works

Basically, you can flip USD into almost any currency. But since I wanted it to be useful, I also added a way to convert between any two currencies—like SEK to EUR—where the app handles all the "middle-man" math with USD in the background.

### The Techy Bits

I used **Python** for the logic and the **Requests** library to handle the internet talk. For security, I used **Dotenv** so my API keys stay private (very important!). The data is managed through **JSON** and the whole thing is built with an object-oriented approach to keep the code clean.

### Want to play around with it?

1. Just clone the repo: `git clone https://github.com/soniatolou/currency-converter.git`
2. Install the requirements: `pip install -r requirements.txt`
3. You'll need an API key from Open Exchange Rates. Pop that into a `.env` file like this: `APP_ID=your_key_here`
4. Run it: `python main.py`

It’s been a fun challenge to bridge the gap between a school assignment and a working application!
