def apply_filters(df, filters):
    filtered_df = df.copy()

    # time filtering
    if "duration_filter" in filters:
        operator, value = filters["duration_filter"]
        if operator == ">":
            filtered_df = filtered_df[filtered_df["avg_duration_hr"] > value]
        elif operator == "<":
            filtered_df = filtered_df[filtered_df["avg_duration_hr"] < value]

    # from_city 
    if "from_city" in filters:
        filtered_df = filtered_df[filtered_df["from_city"].str.lower() == filters["from_city"].lower()]

    # to_city 
    if "to_city" in filters:
        filtered_df = filtered_df[filtered_df["to_city"].str.lower() == filters["to_city"].lower()]

    # multiple sorting
    if "sort_by" in filters:
        if isinstance(filters["sort_by"], list):
            # multiple sorting: column and directions seperating
            columns = [col for col, _ in filters["sort_by"]]
            orders = [asc for _, asc in filters["sort_by"]]
            filtered_df = filtered_df.sort_values(by=columns, ascending=orders)
        else:
            column, ascending = filters["sort_by"]
            filtered_df = filtered_df.sort_values(by=column, ascending=ascending)

    return filtered_df
