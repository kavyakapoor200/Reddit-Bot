# fallback_runner.py
import threading
import time
from bot_logic import subreddits, generate_fallback_post, post_to_subreddit, can_post

# Fallback loop ON/OFF switch
fallback_running = False
fallback_thread = None

def fallback_loop():
    global fallback_running
    fallback_running = True

    print("⚙️ Fallback auto-posting started...")

    while fallback_running:
        for sr, config in subreddits.items():

            if not fallback_running:
                break   # stop immediately

            # Allow post only if active hours + cooldown
            if can_post(sr):
                print(f"📌 Posting fallback content to {sr}...")

                try:
                    title, post = generate_fallback_post(sr, config["instruction"])
                    post_to_subreddit(sr, title, post)
                    print(f"✅ Successfully posted to {sr}")

                except Exception as e:
                    print(f"❌ Error posting to {sr}: {e}")

            else:
                print(f"⏳ Skipping {sr} (cooldown or inactive hours)")

            time.sleep(10)   # small delay in between

        print("😴 Sleeping for 15 minutes before next cycle...")
        time.sleep(900)      # 15-minute gap

    print("🛑 Fallback loop stopped.")


def start_fallback():
    """
    Starts fallback posting in background thread
    """
    global fallback_thread, fallback_running

    if fallback_running:
        print("⚠️ Fallback already running!")
        return

    fallback_thread = threading.Thread(target=fallback_loop, daemon=True)
    fallback_thread.start()
    print("🚀 Fallback thread started!")


def stop_fallback():
    """
    Stops the fallback loop safely
    """
    global fallback_running
    fallback_running = False
    print("🛑 Stop signal sent.")
