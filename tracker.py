import json
import os

STATS_FILE = "stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total": 0, "correct": 0}
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def update_accuracy(correct=True):
    stats = load_stats()
    stats["total"] += 1
    if correct:
        stats["correct"] += 1
    save_stats(stats)

def get_accuracy():
    stats = load_stats()
    if stats["total"] == 0:
        return 100.0
    return round((stats["correct"] / stats["total"]) * 100, 2)
