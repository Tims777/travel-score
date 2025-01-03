# Travel Score

This repository contains code and reports for my
[MADE](https://oss.cs.fau.de/teaching/specific/made/) project `travel-score`.
While my original goal was to compare potential travel destinations in terms of
their attractiveness, I quickly realized that this could be an easy task given
the right dataset, which unfortunately does not exist. This projects goal has
therefore shifted towards creating such a dataset.

## Abstract

Finding high-quality, tourism- and travel-related open datasets is a non-trivial
task. While there are some high-quality datasets available,[^unwto] [^ttdi], they
cannot be used freely (e.g. not commercially) and are therefore not open data as
defined by the Open Definition.[^opendefinition]

This project aims to create such an open dataset, by combining open data from
different sources.

[^unwto]: https://www.unwto.org/tourism-statistics/tourism-statistics-database

[^ttdi]: https://www.weforum.org/publications/travel-tourism-development-index-2024/

[^opendefinition]: https://opendefinition.org/

## Datasources

### Datasource1: INFORM Risk

- URL: https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

> The INFORM Risk Index is a global, open-source risk assessment for
> humanitarian crises and disasters.

I use the RISK score as an indicator for tourist safety.

### Datasource2: International Comparison Program

- URL: https://www.worldbank.org/en/programs/icp
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

> A worldwide statistical initiative to collect comparative price data and
> detailed GDP expenditures to produce purchasing power parities (PPPs) for the
> world’s economies

I use the ICP data as an indicator for destination costliness.

### Datasource3: OpenStreetMap

- URL: https://planet.openstreetmap.org/
- License: [ODbL](https://opendatacommons.org/licenses/odbl/1.0/)

> OpenStreetMap is a free, editable map of the whole world that is being built
> by volunteers largely from scratch and released with an open-content license.

I extract data from OSM to serve as an indicator for resources that are relevant
for tourists (natural, historic, touristic infrastructure).

### Datasource4: Natural Earth

- URL: https://www.naturalearthdata.com/
- License: public domain

> Natural Earth is a public domain map dataset available at 1:10m, 1:50m, and
> 1:110 million scales.

I am using Natural Earth as data source for country boundaries & administrative
details.

### Additional Datasource: Travel & Tourism Development Index

- URL:
  https://www.weforum.org/publications/travel-tourism-development-index-2024/
- License: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)

While the TTDI would be an excellent data source to build my project upon, this
is unfortunately not possible as the data is licensed under terms that prohibit
the publication of any derivatives. However, I might use this dataset to
benchmark my own indicators against the TTDI ones.
