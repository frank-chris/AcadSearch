# Acad Search

Experience the live website at [acadsearch.pythonanywhere.com](https://acadsearch.pythonanywhere.com)

![SS1](https://github.com/nishikantparmariam/Data-Science-Project/blob/main/snapshot-1.png)

![SS2](https://github.com/nishikantparmariam/Data-Science-Project/blob/main/snapshot-2.png)

This project has been made as a part of project component of the course **Introduction to Data Science** offered at IIT Gandhinagar in Semester-2 AY 2020-21 under the guidance of **Prof. Anirban Dasgupta**.

The contributors of this project are [Nishikant Parmar](https://github.com/nishikantparmariam/), [Chris Francis](https://github.com/frank-chris), [Amey Kulkarni](https://github.com/amey-kulkarni27)

### Table of Contents
**[Proposal](#installation-instructions)**<br>
**[Code Structure](#compatibility)**<br>
**[Modules of Search Engine](#compatibility)**<br>
**[Evaluation](#notes-and-miscellaneous)**<br>
**[Detailed Report](#usage-instructions)**<br>
**[Video](#troubleshooting)**<br>
**[Future Work](#building-the-extension-bundles)**<br>



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