import json
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

KEYWORDS = [
    "pain", "problem", "hate", "struggle", "frustrated", "issue", 
    "broken", "slow", "hard to", "annoying", "difficult"
]

def fetch_top_stories(limit=50):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()[:limit]
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при получении списка историй: {e}")
        return []

def fetch_story_details(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.warning(f"Не удалось загрузить историю ID {story_id}: {e}")
        return None

def analyze_pains():
    logging.info("Сканирование Hacker News...")
    story_ids = fetch_top_stories()
    if not story_ids:
        logging.error("Не удалось получить список историй или список пуст.")
        return

    report = []
    for s_id in story_ids:
        story = fetch_story_details(s_id)
        if not story or "title" not in story:
            continue

        title = story["title"].lower()
        if any(keyword in title for keyword in KEYWORDS):
            report.append({
                "id": story.get("id"),
                "title": story.get("title"),
                "url": story.get("url", f"https://news.ycombinator.com/item?id={s_id}"),
                "score": story.get("score", 0),
                "comments": story.get("descendants", 0)
            })

    output_filename = "developer_pains_report.json"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        logging.info(f"Сканирование завершено! Найдено записей: {len(report)}. Отчет сохранен в {output_filename}")
    except IOError as e:
        logging.error(f"Ошибка при сохранении отчета: {e}")

if __name__ == "__main__":
    analyze_pains()
