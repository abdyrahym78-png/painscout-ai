import requests
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_config():
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Ошибка при чтении config.json: {e}. Используются настройки по умолчанию.")
    return {"keywords": ["saas", "auth", "boilerplate", "problem", "error"], "max_stories": 30}

def fetch_top_stories(limit=30):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=json"
    try:
        logging.info("Подключение к Hacker News API...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()[:limit]
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при получении списка историй: {e}")
        return []

def fetch_story_details(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.warning(f"Не удалось загрузить историю ID {story_id}: {e}")
        return None

def analyze_pains():
    print("=" * 60)
    print(" 🚀 PainScout AI — Автоматический скаут потребностей разработчиков")
    print("=" * 60)
    
    config = load_config()
    keywords = config.get("keywords", [])
    max_stories = config.get("max_stories", 30)
    
    story_ids = fetch_top_stories(max_stories)
    if not story_ids:
        logging.error("Не удалось получить список историй или список пуст.")
        return

    pains_found = []
    print(f"[+] Анализируем топ-{len(story_ids)} тем на наличие болей разработчиков...\n")
    
    for s_id in story_ids:
        item = fetch_story_details(s_id)
        if item and "title" in item:
            title = item["title"]
            lower_title = title.lower()
            
            matched_kw = [kw for kw in keywords if kw in lower_title]
            if matched_kw:
                print(f"  [🎯 Найдена боль] {title}")
                pains_found.append({
                    "id": s_id,
                    "title": title,
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={s_id}"),
                    "matched_keywords": matched_kw,
                    "suggested_offer": "Идеально подходит для продвижения готового SaaS-шаблона или утилиты."
                })

    print("\n" + "=" * 60)
    print(f"[✓] Сканирование завершено. Выявлено релевантных болей: {len(pains_found)}")
    
    output_file = "developer_pains_report.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pains_found, f, indent=4, ensure_ascii=False)
        print(f"[+] Отчет успешно сохранен в файл: {output_file}")
    except Exception as e:
        print(f"[-] Ошибка при сохранении отчета в файл {output_file}: {e}")
    print("=" * 60)

if __name__ == "__main__":
    analyze_pains()
