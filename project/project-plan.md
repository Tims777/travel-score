# Project Plan

## Title

Travel Score

## Main Question

- Is North America more suitable for tourists than South America?

## Description

From what I have heard, the general opinion seems to be that South America is
generally "less suitable" for tourists than North America. But is this really
true?

I would love to find a fact based yes or no answer to that question, although
most likely the correct answer can only be "it depends". This project shall
therefore seek a broader perspective first, by focusing on different push and
pull factors for tourists on a per country basis, such as risks, required
budget, diversity of attractions and activities, etc.

The different factors will then be analyzed statistically to identify potential
biases or relationships between them. If possible, the factors will finally be
aggregated into a single "travel score" per country, but if the data is found to
be highly biased, this step may be omitted.

## Datasources

### Datasource1: INFORM Risk

- Metadata URL: https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk
- Data URL:
  https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI/Countries/Scores/?WorkflowId=482&IndicatorId=INFORM,HA,VU,CC
- Data Type: JSON
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

> The INFORM Risk Index is a global, open-source risk assessment for
> humanitarian crises and disasters.

I want to use the RISK score as an indicator for tourist safety.

### Datasource2: International Comparison Program

- Metadata URL:
  https://datacatalog.worldbank.org/search/dataset/0066092/International-Comparison-Program-2021
- Data URL: https://api.worldbank.org/v2/indicators
- Data Type: XML
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

> A worldwide statistical initiative to collect comparative price data and
> detailed GDP expenditures to produce purchasing power parities (PPPs) for the
> world’s economies

I want to use the ICP data as an indicator for destination costliness.

### Datasource3: OpenStreetMap

- Metadata URL: https://download.geofabrik.de/
- Data URL: (multiple)
- Data Type: PBF
- License: [ODbL](https://opendatacommons.org/licenses/odbl/1.0/)

> OpenStreetMap is a free, editable map of the whole world that is being built
> by volunteers largely from scratch and released with an open-content license.

At a later stage, I might extract data from OSM to serve as an indicator for the
amount of tourist attractions.

### Additional Datasource: Travel & Tourism Development Index

- Metadata URL:
  https://www.weforum.org/publications/travel-tourism-development-index-2024/
- Data URL: https://www3.weforum.org/docs/WEF_TTDI_2024_edition_data.xlsx
- Data Type: XLSX
- License: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)

While the TTDI would be an excellent data source to build my project upon, this
is unfortunately not possible as the data is licensed under terms that prohibit
the publication of any derivatives. However, I might use this data set to
benchmark my own indicators against the TTDI ones.

## Work Packages

1. Initial setup of project and pipeline
   [#1](https://github.com/Tims777/travel-score/issues/1)
2. Extraction of INFORM and ICP datasets
   [#2](https://github.com/Tims777/travel-score/issues/2)
3. Produce first iteration of output data
   [#4](https://github.com/Tims777/travel-score/issues/4)
4. Statistical analysis of extracted data
   [#3](https://github.com/Tims777/travel-score/issues/3)
5. Investigation of sensible OSM elements
   [#5](https://github.com/Tims777/travel-score/issues/5)
6. Basic testing (system- and unit-tests)
   [#9](https://github.com/Tims777/travel-score/issues/9)
7. Extraction and integration of OSM data
   [#6](https://github.com/Tims777/travel-score/issues/6)
8. Advanced data analysis and visualizations
   [#7](https://github.com/Tims777/travel-score/issues/7)
9. Result validation by comparison with TTDI
   [#8](https://github.com/Tims777/travel-score/issues/8)
