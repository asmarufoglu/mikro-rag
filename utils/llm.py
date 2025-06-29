from tabulate import tabulate

def generate_answer(filtered_df, user_input):
    """
    Filtrelenmiş DataFrame'e göre doğal dilde cevap üretir.
    """
    if filtered_df.empty:
        return "Sonuç bulunamadı."

    top_result = filtered_df.iloc[0]
    from_city = top_result['from_city']
    to_city = top_result['to_city']
    duration = top_result['avg_duration_hr']
    price = top_result['avg_price_try']
    company = top_result['company']
    freq = top_result['freq_per_day']

    explanation = (
        f"**Önerilen Sefer:** {from_city} - {to_city} arası "
        f"{company} firmasıyla. Ortalama süre: {duration} saat, "
        f"fiyat: {price} TL, günlük {freq} sefer yapılmakta."
    )

    table = tabulate(filtered_df.head(5).values.tolist(),
                     headers=filtered_df.columns.tolist(),
                     tablefmt="github")

    return explanation + "\n\n```text\n" + table + "\n```"
