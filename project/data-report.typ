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


= Is North America more suitable for tourists than South America?

The aim of my MADE @made project is to answer this question based on open data.

== Data Sources

As of now, I am using two main data sources, as well as one extra data source for visualization purposes.

=== Data Source 1: INFORM Risk

The INFORM Risk Index @inform-risk is provided by the Joint Research Centre of the European Commission. Its purpose is to evaluate the risk of humanitarian crises. While the risk of humanitarian crises is obviously not the same thing, I have chosen this data source to indicate the individual risk for tourists, because the data is of high quality and has global coverage. Additionally, the index is not only open data but also open source, meaning that it is possible (although out of scope for this one-semester project) to adapt the methodology towards the risk profile of tourists.

// TODO: What is the structure and quality of your data? (Compare lecture D01)

The INFORM Risk Index is published under the @cc-by-4 license @inform-risk-license. As such, it is possible to use the data without major limitations, provided that proper attribution is given. In addition to the attribution already present here, I will add additional notices (directly or as metadata) to derivatives like the final report or the resulting dataset.

=== Data Source 2: International Comparison Program

The International Comparison Program @icp is managed by the World Bank on behalf of the United Nations Statistical Commission. One of its aims is, to produce #quote("comparable price level indexes (PLIs) for participating economies"). As such, it was a natural choice for me to use this dataset to compare the price levels of different American countries.

// TODO: What is the structure and quality of your data? (Compare lecture D01)

The results of the International Comparison Program 2021 are also licensed under the @cc-by-4 license @icp-license. Consequently, I will take the same measures as with the INFORM Risk dataset to ensure proper license adherence.

=== Extra Data Source: Natural Earth

The Natural Earth dataset @natural-earth is a public domain map of the world, which is primarily intended for visualization purposes but a closer inspection shows that there is also lots of useful metadata attatched to the dataset.

// TODO: What is the structure and quality of your data? (Compare lecture D01)

As the Natural Earth dataset is in the @public-domain @natural-earth-license, the data can be used without limitations and no attribution is required.

== Data Pipeline

My data pipeline is based on Dagster @dagster. After comparison of different competing frameworks, I chose Dagster because it offers a good compromise between framework size and feature set.

// #figure(
//   image("media/assets.svg", width: 80%),
//   caption: "The data pipeline.",
// )


// TODO:
// - Describe your data pipeline on a high level, which technology did you use to implement it
// - Which transformation or cleaning steps did you do and why?
// - What problems did you encounter and how did you solve them?
// - Describe what meta-quality measures you implemented, how does your pipeline deal with errors or changing input data?

== Result and Limitations

// TODO:
// - Describe the output data of your data pipeline
//   - What is the data structure and quality of your result? (Compare lecture D01)
// - What data format did you choose as the output of your pipeline and why
// - Critically reflect on your data and any potential issues you anticipate for your final report

#pagebreak()

== License Glossary
#print-glossary(entry-list)

== Bibliography
#bibliography("data-report-refs.yml", title: none, style: "spie")
