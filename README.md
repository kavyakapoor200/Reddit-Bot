# Reddit Posting Bot 🤖

This project is an **automated Reddit posting bot** built using:
- **[PRAW](https://praw.readthedocs.io/)** (Python Reddit API Wrapper)
- **[Perplexity API](https://docs.perplexity.ai/)** (LLM for content generation)

The bot can:
1. **Strategy-based posting** → User provides a trading strategy, bot generates subreddit, title, and post body using Perplexity and posts directly.  
2. **Subreddit-based fallback posting** → If user does not provide a strategy, bot automatically generates posts for pre-configured subreddits following custom rules (active hours, cooldown, instructions).  

---

## 🔹 Features

- **Reddit Auto-login** via PRAW  
- **Perplexity LLM integration** for post generation  
- **Active hours control** (different per subreddit)  
- **Cooldown management** using `last_posted.json`  
- **Flair assignment** (when available)  
- **Post-removal check** (wait 20s, detect auto-mod/mod removal)  
- **Indian retail trading context** (mentions Zerodha, NSE/BSE in some subs)  
- **Two posting modes:**  
  - **Strategy-based** → Posts your custom trading strategy with personalized title + body  
  - **Subreddit-based fallback** → Automatically generates relevant posts for each subreddit if no strategy given  

---

## 🔹 Installation

Clone the repository:
git clone https://github.com/<your-username>/reddit-posting-bot.git
cd reddit-posting-bot

