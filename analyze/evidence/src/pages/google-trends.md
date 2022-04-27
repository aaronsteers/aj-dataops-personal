# Google Trends

This page is filled with fun facts from the **Google Trends**. Data is sourced from the BigQuery Sample Data Project titled `google_trends`.

```google_trends_query

SELECT
    term,
    week,
    rank,
    refresh_date,
    week
    # , * ## uncomment to explore all columns
FROM `bigquery-public-data.google_trends.top_terms`
WHERE refresh_date = "2022-04-26"
  AND week = '2022-04-24'
  and dma_id = 819 # 'Seattle-Tacoma WA'
ORDER BY rank asc
LIMIT 1000
```

## Top Search Results in Seattle Region

{#each data.google_trends_query as google_trends}

- #{google_trends.rank}: {google_trends.term}

{/each}
