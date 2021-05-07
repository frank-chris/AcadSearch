# Acad Search

Experience the live website at [acadsearch.pythonanywhere.com](https://acadsearch.pythonanywhere.com)

## Table of Contents

**[Motivation](#motivation)**<br>
**[What we have built?](#what-we-have-built?)**<br>
**[Working Snapshots](#working-snapshots)**<br>
**[High Level Design](#high-level-design)**<br>
**[Modules of Search Engine](#modules-of-search-engine)**<br>
**[Work Flow](#work-flow)**<br>
**[Evaluation Metrics](#evaluation)**<br>
**[Detailed Report](https://github.com/nishikantparmariam/Data-Science-Project/blob/main/Report.pdf)**<br>
**[Presentation and Demo Video]()**<br>
**[Future Work](#future-work)**<br>
**[Code Structure](#code-structure)**<br>
**[References and Credits](#references-and-credits)**<br>

### Motivation

Students often find the need to search for professors based on various criteria
such as name, university, research topics, top cited papers and rank them based
on factors like citations or h-index. A simple Google search may not allow you to
first shortlist professors based on whether they do research in "adversarial machine
learning" and then rank them according to the number of citations that they have
in the last 5 years

### What we have built?

We have developed a search engine that can cater to the needs
of students looking for professors to approach for projects, internships or jobs.
The search engine allows users to search for professors based on name, university,
research areas and paper titles using 3 different retrieval methods. The engine also
allows users to sort the search results based on criteria like h-index, citations in the
last 5 years etc. We have deployed the search engine publicly as a web application,
and also evaluated its performance in terms of time and quality of results.

### Working Snapshots

![SS2](snapshot-2.png)

![SS1](snapshot-1.png)

## High Level Design

![SS1](high-level-architecture.png)

## Modules of Search Engine

## Work Flow

![SS2](flow-chart.png)

## Evaluation

## Future Work

## Code Structure

```
.
├── Proposal.pdf
├── README.md
├── Report.pdf
├── cleaning
│   └── cleaning_data.py
├── data
│   ├── csrankings-0.csv
│   ├── csrankings-1.csv
│   ├── csrankings-2.csv
│   ├── csrankings-3.csv
│   ├── csrankings-4.csv
│   ├── csrankings-5.csv
│   ├── csrankings-6.csv
│   ├── csrankings-7.csv
│   ├── csrankings-8.csv
│   ├── csrankings-9.csv
│   ├── metadata.csv
│   ├── name_and_affiliation_index_full.json
│   ├── professor_data-0-cleaned.csv        
│   ├── professor_data-0.csv
│   ├── professor_data-1-cleaned.csv        
│   ├── professor_data-1.csv
│   ├── professor_data-2-cleaned.csv        
│   ├── professor_data-2.csv
│   ├── professor_data-3-cleaned.csv        
│   ├── professor_data-3.csv
│   ├── professor_data-4-cleaned.csv        
│   ├── professor_data-4.csv
│   ├── professor_data-5-cleaned.csv        
│   ├── professor_data-5.csv
│   ├── professor_data-6-cleaned.csv
│   ├── professor_data-6.csv
│   ├── professor_data-7-cleaned.csv
│   ├── professor_data-7.csv
│   ├── professor_data-8-cleaned.csv
│   ├── professor_data-8.csv
│   ├── professor_data-9-cleaned.csv
│   ├── professor_data-9.csv
│   ├── tf_idf_scores_topic_and_paper_full.json
│   └── topic_and_paper_index_full.json
├── data_statistics
│   ├── compute_statistics.py
│   └── plots
│       ├── 1.png
│       ├── 2.png
│       ├── 3.png
│       ├── 4.png
│       ├── 5.png
│       └── old
│           ├── 1.png
│           ├── 2.png
│           ├── 3.png
│           ├── 4.png
│           ├── 5.png
│           ├── 6.png
│           └── 7.png
├── evaluation
│   ├── average_query_time.png
│   ├── evaluate.py
│   ├── median_rank.png
│   └── recall_rate.png
├── flow-chart.png
├── helper_functions
│   └── common_functions.py
├── high-level-architecture.png
├── indexing
│   └── build_index.py
├── querying
│   ├── boolean.py
│   ├── compute_tf_idf.py
│   ├── default_rankings.py
│   └── get_tf_idf.py
├── scraping
│   └── scrape_prof_data.py
├── snapshot-1.png
├── snapshot-2.png
└── web_server
    ├── images
    │   ├── placeholder.svg
    │   └── search.png
    ├── read_information.py
    ├── server.py
    └── templates
        └── index.html
```

### References and Credits

This project has been made as a part of project component of the course **Introduction to Data Science** offered at IIT Gandhinagar in Semester-2 AY 2020-21 under the guidance of **Prof. Anirban Dasgupta**.

The contributors of this project are [Nishikant Parmar](https://github.com/nishikantparmariam/), [Chris Francis](https://github.com/frank-chris), [Amey Kulkarni](https://github.com/amey-kulkarni27)