#import "@preview/diatypst:0.4.0": *
#import "@preview/mannot:0.2.0": *

#set text(font: "DejaVu Sans Mono")

#let main-color = rgb("#2bad95")

#let datasets = yaml("report/datasets.yml")
#let licenses = yaml("report/licenses.yml")
#let refs = yaml("report/refs.yml")

#show: slides.with(
  title: "Travel Score",
  subtitle: "Open Data for Tourists",
  authors: "Simon Zimmermann",
  title-color: main-color,
  // date: datetime.today().display("[day].[month].[year]"),
  ratio: 16 / 9,
  count: false,
  toc: false,
  layout: "small",
)

#set heading(numbering: none)

= Motivation

== Ranking Travel Destinations by Attractivity

#align(horizon)[
  #grid(
    columns: (52%, auto),
    [
      There are 35 American countries.

      #v(1em)

      - Where can go as a tourist?
        - Is it safe?
        - How affordable is it?
        - What is there to do?
    ],
    [#image("report/media/map_of_america.svg", height: 100% - 1em)],
    grid.cell(colspan: 2)[#align(center)[_Can we answer these questions using open data?_]]
  )
]

== Open Data to the rescue?

#align(horizon)[
  #grid(
    columns: (2fr, 1fr),
    row-gutter: 1.5em,
    grid.header([=== Travel & Tourism Datasets]),
    [
      - High quality T&T datasets do exist
        - But they are not open
    ],
    grid(
      columns: 2,
      image("report/media/logos/world-economic-forum.svg", width: 70%),
      image("report/media/logos/un-tourism.svg", width: 70%),
    ),

    [
      - Open datasets do exist
        - But they are not directly about T&T
    ],
    grid(
      columns: (70%, auto),
      image("report/media/logos/european-commission.svg", width: 90%),
      image("report/media/logos/openstreetmaps.svg", width: 90%),
    ),
  )
]

= Data Processing

== Travel-related Data Sources

#let license(name) = licenses.at(name).short
#align(horizon)[
  #table(
    columns: (2fr, 1fr),
    [*Data source*], [*License*],
    ..datasets
      .values()
      .map(v => (
        [#v.name],
        [#license(v.license)],
      ))
      .flatten()
  )
]

== Data Pipeline
#align(center)[
  #image("report/media/pipeline.svg", height: 100%)
  // Simplified view of Dagster-based data pipeline
]

== Combined Dataset

#align(center)[
  #image("report/media/combined-dataset.svg", height: 100% - 2em)
  Full dataset contains 35 rows and 89 columns
]

== Benchmarking against TTDI

#context {
  set page(margin: (y: 0em), footer: none, header: none)
  place(top + center, dy: 1em)[
    #let heading = query(selector(heading).before(here())).last()
    #text(fill: main-color, weight: "bold")[#heading.body]
  ]
  align(bottom + center)[
    #image("report/media/benchmark.svg", height: 90%)
  ]
}

== Travel Score Calculation
#align(horizon)[

  #text(size: 1.5em)[
    #math.equation($
      "travel score" =
      mark("safety", tag: #<safety>, color: #green) dot
      mark("affordability", tag: #<affordability>, color: #main-color) dot
      mark("attractiveness", tag: #<attractiveness>, color: #blue)
    $) <travel-score>
  ]

  #annot(<safety>, pos: bottom + left, yshift: 1em, text-props: (size: 12pt))[risk factors]

  #annot(<affordability>, pos: bottom + left, yshift: 4em, text-props: (size: 12pt))[price level of consumption]

  #annot(
    <attractiveness>,
    pos: bottom + left,
    yshift: 7em,
    text-props: (size: 12pt),
  )[natural, historic & touristic resources]

]

= Results

== Result Maps

#context {
  set page(margin: (y: 0em), footer: none, header: none)
  place(top + center, dy: 1em)[
    #let heading = query(selector(heading).before(here())).last()
    #text(fill: main-color, weight: "bold")[#heading.body]
  ]
  align(bottom + center)[
    #image("report/media/combined_map.svg", height: 90%)
  ]
}

== Top 3 Countries

#context {
  set page(margin: (top: 4em))

  align(center)[
    #image("report/media/radar_plot.svg", height: 100%)
  ]
}

== Limitations

#align(horizon)[
  === Methodology
  - Objective ranking does not consider personal preferences
  - Limited amount of push- & pull-factors could be included
  - Aggregation at country level is not ideal

  === Data
  - Lower accuracy due to biases?
  - Data misaligned with tourist perspective?
]

= Outlook

== Further Ideas

#align(horizon)[
  === Zooming in
  - Calculate scores on finer resolution than per-country
    - Possible with OSM data
    - Requires new data sources for risk and price level

  === Zooming out
  - Calculate scores for other continents as well
    - This is possible with current data sources!
    - But OSM is heavily biased towards Europe
    - Improved methodology is necessary
]

== References

#context {
  set page(margin: (top: 3.25em, bottom: 0.25em), footer: none)
  let ref(id) = text(size: 8pt, link(refs.at(id).url))
  align(horizon)[
    #list(
      marker: none,
      spacing: 1.5em,
      [*Travel Score* \ #ref("travel-score-git")],
      [*Travel & Tourism Development Index* \ #ref("ttdi")],
      ..datasets
        .values()
        .map(val => [
          *#val.name* \ #ref(val.data-ref)
        ]),
    )
  ]
}
