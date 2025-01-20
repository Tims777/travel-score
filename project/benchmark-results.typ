#set heading(numbering: "1.")
#set page(numbering: "1")
#set math.equation(numbering: "(1)", block: true)
#set par(justify: true)

#let datasets = yaml("report/datasets.yml")
#let licenses = yaml("report/licenses.yml")
#let licenses = (
  licenses
    .pairs()
    .map(((k, v)) => (
      k,
      (
        short: v.short,
        long: v.long,
        description: link(v.url),
      ),
    ))
    .to-dict()
)

#import "@preview/glossy:0.4.0": *
#show: init-glossary.with(licenses)

#show link: set text(fill: blue.darken(60%))

#let license(name) = link(
  label("licenses"),
  ref(label(name + ":short")),
)

#align(center)[#text(18pt)[*Travel Score -- Open data for tourists*]]
#align(center)[#text(18pt)[_Benchmark Results_]]

= Introduction

As discussed in the Analysis Report @travel-score-analysis, there is a lack of open @opendefinition datasets in the context of travel and tourism.
This project set out to explore, whether it is possible to create such a dataset based on existing open data sources. While the Analysis Report describes, how such a dataset can be created, it remained unclear, how accurate the resulting dataset actually is. The following benchmark results shall answer this question.

= Methodology

The Travel Score combined dataset, which is sourced from several open data sources, was compared to the Travel & Tourism Development Index @ttdi, which serves as the ground truth here (see @data-sources). The comparison was realized by analyzing the correlation between similar indicators from both datasets.

#figure(
  table(
    columns: (1fr, 1fr),
    align: center + horizon,
    table.header(
      [*Open Data Sources*],
      [*Ground Truth*],
    ),
    ..datasets.values().slice(0, 1).map(v => [#v.name #ref(label(v.data-ref))]),
    table.cell(rowspan: datasets.len())[Travel & Tourism Development Index @ttdi],
    ..datasets.values().slice(1).map(v => [#v.name #ref(label(v.data-ref))]),
  ),
  caption: [Data sources, which the following benchmark is based upon.],
) <data-sources>


= Results

#figure(
  image("report/media/benchmark.svg"),
  caption: [Open data indicators for American countries plotted in relation to their respective TTDI score.],
) <results>

= Discussion

The benchmark results show a strong (either positive or negative) correlation for most pairs of open and TTDI indicators. This speaks for the quality of both datasets, considering that the indicators were calculated using different primary indicators and methodologies but still achieve very similar results in describing the real world situation.

The only exception is the OpenStreetMap-derived _Tourism score_, which has no correlation with the TTDI indicator _Tourist Services and Infrastructure_. In partial, this might be explained through the fact that the TTDI indicator is broader, including also investment and productivity aspects in addition to the availability of tourism resources itself. More likely however, this could indicate incomplete data on the OpenStreetMap side or a flaw in the methodology that was used to calculate the resource scores from the raw OpenStreetMap data.

As a consequence, the _Tourism score_ and potentially also identically derived scores (_Natural score_ and _Historic score_) should be inspected for flaws in the underlying data or methodology, for example by comparing them with additional datasets if available. Additionally, investigation of existing outliers from the otherwise well-correlated indicator pairs could lead to interesting insights.

= Bibliography

#bibliography("report/refs.yml", title: none, style: "spie")
