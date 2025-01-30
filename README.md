# Travel Score

This repository contains code and reports for my
[MADE](https://oss.cs.fau.de/teaching/specific/made/) project `travel-score`.
While my original goal was to compare potential travel destinations in terms of
their attractiveness, I quickly realized that this could be an easy task given
the right dataset, which unfortunately does not exist. This projects goal has
therefore shifted towards creating such a dataset.

## Abstract

Finding high-quality, tourism- and travel-related open datasets is a non-trivial
task. While there are some high-quality datasets available,[^unwto][^ttdi] they
cannot be used freely (e.g. not commercially) and are therefore not open data as
defined by the Open Definition.[^opendefinition] This project aims to create
such an open dataset, by combining open data from different sources.

[^unwto]: https://www.unwto.org/tourism-statistics/tourism-statistics-database

[^ttdi]: https://www.weforum.org/publications/travel-tourism-development-index-2024/

[^opendefinition]: https://opendefinition.org/

## Results

![Choropleth maps of North and South America, depicting the ](./project/report/media/combined_map.svg)

The above map is a visualization of the calculated travel scores for North and South America.
You can find the full dataset in the [release section](https://github.com/Tims777/travel-score/releases).

## Detailed Reports

Please refer to the following documents for more details about this project.

- [Data Report](./project/data-report.pdf)
- [Analysis Report](./project/analysis-report.pdf)
- [Benchmark Results](./project/benchmark-results.pdf)
- [Presentation Slides](./project/slides.pdf)

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

I extract data from OSM to serve as an indicator for resources (e.g. natural or
historic) that are relevant for tourists.

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

> The TTDI measures the set of factors and policies that enable the sustainable
> and resilient development of T&T.

While the TTDI would have been an excellent data source to build my project
upon, this was not possible, as the data is licensed under terms that prohibit
the publication of derivatives. However, to get an impression of how accurate my
own dataset is, I use the TTDI data for benchmarking purposes.

After comparing both datasets, I realized that it might be interesting for
others to see the results as well. Therefore, I contacted the World Economic
Forum, publishers of the TTDI, and asked for approval to publish my results. The
following is an extract from the relevant correspondence, slightly simplified
but with the wording unchanged.

> **Usage of TTDI data as benchmark for open data project**
>
> I am currently working on a university project about tourism in the Americas,
> for which I collected data from several open data sources. Because the
> resulting dataset is similar in nature, I used your TTDI dataset to benchmark
> my own data. However, due to the nature of the CC BY-NC-ND license, I cannot
> publish my analysis results although I would like to do so.
>
> Therefore, I would like to ask your written approval of publishing my analysis
> (as part of my Git repository at https://github.com/Tims777/travel-score), if
> you feel that this is in line with your goals and vision. To give you an
> impression of what my analysis results look like, I attached the current
> version as SVG.
>
> My project is of academic nature and as such, my use of the TTDI is
> non-commercial.

> **Re: Usage of TTDI data as benchmark for open data project**
>
> The Forum can exceptionally authorize the described use of the material,
> provided that (i) the remaining conditions of the
> [Creative Commons
Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.en)
> Public Licence must be respected; and (ii) you shall not use the Forum’s
> materials beyond the described scope or in any manner that may be harmful for
> the World Economic Forum.
>
> The authorization herein is revocable at the will of the World Economic Forum.
