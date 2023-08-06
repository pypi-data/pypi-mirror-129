# PopPyGen
A statistically accurate synthetic human population generator for python, based on demographic and regional datasets.

# Installation
```python
pip install poppygen
```

# Usage
```python
#Note: Be Patient, this may take a few minutes for the large datasets to process.
from poppygen import PopulationGenerator
from poppygen.datasets import process_acs, process_safegraph_poi, process_pums

poi_df = process_safegraph_poi()
acs_df = process_acs()

pg = PopulationGenerator(poi_df, acs_df)

local_population = pg.generate_population(population_size=100, census_block_group=[120330001001, 120330036071])
print(local_population[0].baseline)

pg.generate_activity(population=local_population)
print(local_population[0].activity["location"])
```