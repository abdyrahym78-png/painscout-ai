import requests
import json
import os

def load_config():
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] Ошибка при чтении config.json: {e}. Используются настройки по умолчанию.")
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
        res.raise_for_status()
        story_ids = res.json()[:max_stories]
    except requests.exceptions.HTTPError as http_err:
        print(f"[-] HTTP ошибка при обращении к API: {http_err} (Код ответа: {res.status_code})")
        return
    except requests.exceptions.ConnectionError as conn_err:
        print(f"[-] Ошибка соединения с сетью: {conn_err}")
        return
    except requests.exceptions.Timeout as timeout_err:
        print(f"[-] Превышено время ожидания запроса (таймаут): {timeout_err}")
        return
    except requests.exceptions.RequestException as req_err:
        print(f"[-] Произошла ошибка запроса: {req_err}")
        return
    except Exception as e:
        print(f"[-] Непредвиденная ошибка: {e}")
        return

    pains_found = []
    print(f"[+] Анализируем топ-{len(story_ids)} тем на наличие болей разработчиков...\n")
    
    for s_id in story_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json?print=json"
        try:
            item_res = requests.get(item_url, timeout=5)
            item_res.raise_for_status()
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
        except requests.exceptions.HTTPError as http_err:
            print(f"  [!] HTTP ошибка для элемента {s_id}: {http_err}")
            continue
        except requests.exceptions.ConnectionError:
            print(f"  [!] Ошибка соединения при получении элемента {s_id}")
            continue
        except requests.exceptions.Timeout:
            print(f"  [!] Таймаут при получении элемента {s_id}")
            continue
        except Exception as e:
            print(f"  [!] Ошибка обработки элемента {s_id}: {e}")
            continue

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
    run_pain_scout()
