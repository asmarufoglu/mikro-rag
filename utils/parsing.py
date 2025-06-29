import re

def parse_user_query(user_question):
    """
    Kullanıcının doğal dil sorgusunu analiz eder ve filtre/sıralama kurallarını çıkartır.
    Dönen sözlük şunları içerebilir: duration_filter, from_city, to_city, sort_by (list olabilir)
    """
    query = user_question.lower()
    filters = {}

    # time filtering
    match = re.search(r"(longer than|more than|greater than|uzun.*?(\d+))|(\d+)\s*saat.*(uzun|fazla)", query)
    if match:
        hours = re.findall(r"\d+", match.group())
        if hours:
            filters['duration_filter'] = (">", float(hours[0]))

    match = re.search(r"(shorter than|less than|smaller than|kısa.*?(\d+))|(\d+)\s*saat.*(az|kısa)", query)
    if match:
        hours = re.findall(r"\d+", match.group())
        if hours:
            filters['duration_filter'] = ("<", float(hours[0]))

    # From city
    match = re.search(r"from ([a-zçğıöşü\s]+)", query)
    if match:
        filters['from_city'] = match.group(1).strip().title()
    match = re.search(r"([a-zçğıöşü\s]+)'?dan", query)
    if match:
        filters['from_city'] = match.group(1).strip().title()

    # To city
    match = re.search(r"to ([a-zçğıöşü\s]+)", query)
    if match:
        filters['to_city'] = match.group(1).strip().title()
    match = re.search(r"([a-zçğıöşü\s]+)'?ya|([a-zçğıöşü\s]+)'?ye", query)
    if match:
        filters['to_city'] = (match.group(1) or match.group(2)).strip().title()

    # multiple sorting
    sort_by = []

    if "cheapest" in query or "en ucuz" in query:
        sort_by.append(("avg_price_try", True))  # ascending

    if "most expensive" in query or "en pahalı" in query or "en pahali" in query:
        sort_by.append(("avg_price_try", False))  # descending

    if "most frequent" in query or "en sık" in query:
        sort_by.append(("freq_per_day", False))  # descending

    if "longest" in query or "en uzun" in query:
        sort_by.append(("avg_duration_hr", False))  # descending

    if "fastest" in query or "en kısa" in query or "en kisa" in query:
        sort_by.append(("avg_duration_hr", True))  # ascending

    if sort_by:
        filters["sort_by"] = sort_by if len(sort_by) > 1 else sort_by[0]

    return filters
