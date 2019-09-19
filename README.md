# Welcome to GENAX
**GENAX uses the keywords you enter to dynamically find genes associated with your keywords.**

* GENAX is a web-based server that extracts gene-gene interactions from the biomedical literature. GENAX provides several customizing options, including time, cut-off, weight of edge, and so on. Through dynamic collection, GENAX always provides knowledge extracted from the latest publications. Furthermore, all analysis results can be downloaded in .csv file format.
* All instructions needed to run GENAX are available [here](http://help.genax.tools/) (or click on the document button in the right corner).

The scheme below illustrates the overall processing steps of GENAX.
![GENAX_Step](http://genax.tools/static/GENAX_Step.png)

## Input
GENAX makes a query from user-given keywords and time period. From the query, GENAX collects relevant articles from PubMed.

## Paper Collect
GENAX collects articles with a multi-thread collecting strategy, which allows for a dynamic literature retrieval feature. After all the target papers are collected, GENAX extracts MeSH terms from the papers, which are then converted to gene symbols according to pre-defined rules.

## Network Building
From the paper-gene relationship, GENAX creates edges of the gene network. Genes that are simultaneously referenced in the same paper are the co-occurring genes, and genes that appear alone in the papers are single-occurring genes. GENAX makes contingency tables for all co-occurring gene pairs and calculates the statistical significance of each co-occurring gene pair. All of the gene pairs become edges of the gene network, and statistical significance of the gene pair is based on the weight of the edge. GENAX then creates another network by adding single-occurring nodes to the co-occurring gene network.

## Network Analysis
After network building is complete, there are two networks generated. One is the co-occurring genes only network and the other is the co-occurring genes plus single-occurring genes network. With these two networks, GENAX calculates the centrality of each gene node. The user can obtain the gene scores from the centrality calculation. The user can also access the references from which the genes are collected.

## How to Run on Docker
```bash
$ docker-compose up -d
```
