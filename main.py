import requests
import json
import os

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"keywords": ["saas", "auth", "boilerplate"], "max_stories": 20}

def run_pain_scout():
    print("=" * 60)
    print(" 🚀 PainScout AI — Автоматический скаут потребностей разработчиков")
    print("=" * 60)
    
    config = load_config()
    keywords = config.get("keywords", [])
    max_stories = config.get("max_stories", 20)
    
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=json"
    
    try:
        print("[+] Подключение к Hacker News API...")
        res = requests.get(url, timeout=10)
        story_ids = res.json()[:max_stories]
    except Exception as e:
        print(f"[-] Ошибка сети: {e}")
        return

    pains_found = []
    print(f"[+] Анализируем топ-{len(story_ids)} тем на наличие болей разработчиков...\n")
    
    for s_id in story_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json?print=json"
        try:
            item_res = requests.get(item_url, timeout=5)
            item = item_res.json()
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
        except Exception:
            continue

    print("\n" + "=" * 60)
    print(f"[✓] Сканирование завершено. Выявлено релевантных болей: {len(pains_found)}")
    
    output_file = "developer_pains_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(pains_found, f, indent=4, ensure_ascii=False)
        
    print(f"[+] Отчет успешно сохранен в файл: {output_file}")
    print("=" * 60)

if __name__ == "__main__":
    run_pain_scout()
