🎬 YouTube Liked Videos Cleaner (Python)

A tiny sidekick script that helps you bulk-unlike YouTube videos — because sometimes your algorithm needs a hard reset 🧹✨.

⚙️ What it does

🔑 Uses OAuth2 login (opens your browser once, then remembers the token locally).
📂 Fetches your “Liked Videos” playlist.
🗑️ Cleans up in batches (no spammy requests — plays nice with Google’s API limits).

🛠️ How to set it up (quick quest mode)

🏗️ Make a Google Cloud project → enable YouTube Data API v3.
🔐 Create OAuth2 credentials (Desktop App) → grab your credentials.json.
📁 Drop credentials.json next to remove\_likes.py (⚠️ don’t commit it to GitHub).
📦 Install the dependencies:
pip install -r requirements.txt

🎯 Why I built this

Because YouTube doesn’t let us bulk-unlike, and I got tired of click-click-clicking a thousand times.
This little script was born out of boredom, but ended up being a neat dive into APIs, authentication flows, and handling the real-world boss fight → rate limits 🕹️.
