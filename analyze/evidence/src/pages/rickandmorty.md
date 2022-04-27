# Rick and Morty Fun Facts

This page is filled with fun facts from the [Rick and Morty API](https://rickandmortyapi.com/). Data is sourced from the Singer tap [tap-rickandmorty](https://github.com/aaronsteers/tap-rickandmorty).

```characters_query

select
    name as character_name
from raw_rickandmorty.characters
```

{#if data.characters_query.length }

## Known Characters

There are **{ data.characters_query.length }** Rick and Morty characters in our dataset!

{:else }

_**Oops! The system could not connect to your data - or there is no data to query.**_

{/if}
