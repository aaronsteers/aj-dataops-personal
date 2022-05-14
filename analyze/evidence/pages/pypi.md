# Interesting PyPi Stats

```pypi_downloads_query
SELECT
      week_end_date,
      project,
      sum(num_downloads) as num_downloads
FROM `aj-dataops-personal.marts.fact_pypi_downloads_weekly` 
GROUP BY 1, 2
ORDER BY 1 DESC, 2
```

## Meltano Stats

<LineChart 
    data={data.pypi_downloads_query.filter(p => p.project === 'meltano')}  
    x=week_end_date 
    y=num_downloads
/>

## SDK Stats

<LineChart 
    data={data.pypi_downloads_query.filter(p => p.project === 'singer-sdk')}  
    x=week_end_date 
    y=num_downloads
/>
