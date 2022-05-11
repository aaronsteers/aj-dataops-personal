# Rick and Morty Fun Facts

This page is filled with fun facts from the [Rick and Morty API](https://rickandmortyapi.com/). Data is sourced from the Singer tap [tap-rickandmorty](https://github.com/aaronsteers/tap-rickandmorty).

## Known Characters

```characters_query
select
    *
from tap_rickandmorty.characters
order by created
```

There are **{ data.characters_query.length }** Rick and Morty characters in our dataset!

## Characters by Species

```characters_by_species
select
    species, count(*) num_characters
from tap_rickandmorty.characters
group by species
order by 2 desc
```

<Chart data={data.characters_by_species} x=species y=num_characters>
    <Bar/>
</Chart>

{#each data.characters_query as characters_query}

## {characters_query.name}

[{characters_query.name}]({characters_query.url}) is a {characters_query.gender} {characters_query.species} and is currently {characters_query.status}.
<img alt="{characters_query.name}" src="{characters_query.image}" >

---

{/each}
