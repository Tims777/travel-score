#import "@preview/glossarium:0.5.1": *
#show: make-glossary

#let entry-list = (
  (
    key: "cc-by-4",
    short: "CC-BY 4.0",
    long: "Creative Commons Attribution 4.0",
    description: [ #link("https://creativecommons.org/licenses/by/4.0/")],
  ),
  (
    key: "public-domain",
    short: "CC0",
    long: "public domain",
    description: [ #link("https://creativecommons.org/publicdomain/") ],
  ),
)
#register-glossary(entry-list)

#set heading(numbering: "1.")


#text(15pt)[*Is North America more suitable for tourists than South America?*]

The aim of my MADE @made project is to answer this question based on open data.

= Data Sources

As of now, I am using two main data sources, as well as one extra data source for visualization purposes.

== Data Source 1: INFORM Risk

The INFORM Risk Index @inform-risk is provided by the Joint Research Centre of the European Commission. Its purpose is to evaluate the risk of humanitarian crises. The risk of humanitarian crises is obviously not the same thing as the individual risk for tourists, which I want to analyze. However, I have chosen the INFORM Risk dataset despite this lack in relevancy, because the data is of high quality in all other dimensions (accuracy, completeness, consistency and timeliness). Additionally, the index is not only open data but also open source, meaning that it is possible (although out of scope for this one-semester project) to adapt the methodology towards the risk profile of tourists.

The INFORM Risk Index is published under the @cc-by-4 license @inform-risk-license. As such, it is possible to use the data without major limitations, provided that proper attribution is given. In addition to the attribution already present here, I will add additional notices (directly or as metadata) to derivatives like the final report or the resulting dataset.

== Data Source 2: International Comparison Program

The International Comparison Program @icp is managed by the World Bank on behalf of the United Nations Statistical Commission. One of its aims is, to produce #quote("comparable price level indexes (PLIs) for participating economies"). As such, it was a natural choice for me, to use this dataset to compare price levels of different American countries. From my investigations, the dataset is of high quality regarding accuracy and consistency. However, the data is only complete for earlier years, so I limited myself to data for the year 2021.

The results of the International Comparison Program are also licensed under the @cc-by-4 license @icp-license. Consequently, I will take the same measures as with the INFORM Risk dataset to ensure proper license adherence.

== Extra Data Source: Natural Earth

The Natural Earth dataset @natural-earth is a public domain map of the world, which is primarily intended for visualization purposes but a closer inspection shows that there is also lots of useful metadata attached to the dataset. The data and metadata is of exceptionally high quality.

As the Natural Earth dataset is in the @public-domain @natural-earth-license, the data can be used without limitations and no attribution is required, although of course possible.

= Data Pipeline

My data pipeline is programmed in Python @python and based on the Dagster framework @dagster. After comparison of different competing frameworks, I chose Dagster because it offers a good compromise between framework size and offered features.

== Structure of the Pipeline <structure>

In a first step, the datasets are extracted from their respective source URLs and parsed into a Pandas @pandas `DataFrame` or GeoPandas @geopandas `GeoDataFrame`. Thanks to the (Geo)Pandas libraries and the Python standard libraries, this is possible with only few lines of code, regardless of the original format (JSON, CSV, Shapefile). It is also easily possible, to perform simple reshaping and cleaning operations on the data (see @reshaping).

After the largely unmodified datasets have been stored (see @io), sub-datasets are derived in cases where only part of the original data is relevant for the rest of the data pipeline. As such, a dataset `icp_metrics_2021` is extracted from the `icp_metrics` dataset and an `americas` dataset is extracted from the `countries` dataset.

All original datasets or one of their sub-datasets are eventually merged into a `combined_dataset`. This dataset can then be used to produce derivatives like visualizations and it will serve as the ground truth for the travel score calculation in the future.

#figure(
  image("media/web-ui-pipeline.png", width: 80%),
  caption: "The pipeline structure as seen in the Dagster Web UI.",
)

== Reshaping and Cleaning <reshaping>

Depending on the specific dataset, different reshaping and cleaning operations are performed. All of them make use of the Pandas library, which provides as powerful toolset for such purposes. For example, multiple rows can be grouped together using `pivot` or unwanted metadata at the end of the file can be discarded with `drop`.

== File System <io>

Between two pipeline stages, Dagster will automatically persist all in- and outputs (#quote("assets")) to the file system. By default, the Python-specific Pickle format is used. However, for this project a custom IO-manager was employed to achieve asset storage in the form of SQLite @sqlite databases.

== Encountered Problems

The main problem encountered was choosing the right dataset from different available versions. Both, European Commission and World Bank provide numerous different options to access their data in different formats. However, none of those options truly fits the requirements of this project.

In the spirit of rapid prototyping, this problem has been worked around for now by manually creating download links, that contain just the desired data in an easily processable format. However, this is neither the intended solution from the viewpoint of MADE, nor is it clear whether the ICP download link will continue to work over longer periods of time. Therefore, it might be a good idea to revisit this problem again towards the end of the project, in order to find a more permanent solution.

== Meta-quality Measures

There are no automatic meta quality measures in place yet. However, it is easily possible to manually review the meta quality using Dagsters Web UI, by looking at the metadata which is added to each assets by the custom IO-manager. Additionally, the use of the SQLite format as discussed in @io allows for straightforward inspection of the full datasets.

#figure(
  image("media/web-ui-metadata.png", width: 80%),
  caption: "Per-dataset metadata as seen in the Dagster Web UI.",
)

= Result and Limitations

The main output of my current data pipeline is the combined dataset described in @structure. The output dataset inherits its nature from its ancestor datasets and is therefore of high quality regarding accuracy and completeness. The timeliness suffers a little, due to the ICP data being from the year 2021, while the consistency suffers as the INFORM data is taken from the most recent 2024 report. Regarding its relevancy, the dataset has yet to proove itself during the final report.

#figure(
  grid(
    columns: 2,
    image("../data/risk_map.svg", width: 100%),
    image("../data/price_map.svg", width: 100%),
  ),
  caption: [Visualizations of the combined dataset, indicators `INFORM` (left) and `PX.WL` (right).],
)

As discussed in @io, the SQLite format was chosen for all assets. In practice, this format showed better compatibility with (Geo)Pandas than CSV while at the same time it is far more universal than the Pickle format.

#pagebreak()

= License Glossary

#print-glossary(entry-list)

= Bibliography

#bibliography("data-report-refs.yml", title: none, style: "spie")
