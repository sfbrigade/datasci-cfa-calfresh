# Code for America Get Calfresh NLP Project 
This project is a part of the [Data Science Working Group](http://datascience.codeforsanfrancisco.org) at [Code for San Francisco](http://www.codeforsanfrancisco.org).  Other DSWG projects can be found at the [main GitHub repo](https://github.com/sfbrigade/data-science-wg).

#### -- Project Status: [Active]

## Project Intro/Objective
The purpose of this project is help Code for America process and analyze text response data from Get Calfresh applications to better understand the circumstances in which people apply to the program. Goals of the project are to: 
  1. Spellcheck the text for better downstream processing and analysis 
  2. Remove Personal Identifying information from the text 
  3. Complete Exploratory Data Analysis and Topic Modelling of the Text

### Partner
* Code for America
* https://www.codeforamerica.org, https://www.getcalfresh.org
* Partner contact: Eric Gianella
* If you do not have a partner leave this section out

### Methods Used
* Data Pipelines
* Natural Language Processing
* Object Oriented Programming


### Technologies
* Python
* Jupyter Notebook
* NLTK and other NLP libraries

## Project Description
### About Calfresh
19.4% of Californians did not have enough resources to meet basic needs in 2016 (source: the Economist). One of the initiatives supervised by the Californian state to help those in need is called CalFresh, also known the Supplemental Nutrition Assistance Program (SNAP). Although the application process can be confusing and difficult to navigate, Code for America’s GetCalFresh program is ensuring that everyone can access food assistance benefits. CalFresh consists of providing monthly food benefits to assist low-income households in purchasing the food they need to maintain adequate nutritional levels. These benefits are issued on an Electronic Benefit Transfer (EBT) card which looks like any other credit card. 

### Partnership with DSWG
Code for America wishes to utilize the rich information within the free response portion of the Get Calfresh applications in order to better understand the sentiments and circumstances underlying the reasons people apply.  The hope is that this will help educate the public and break common stereotypes and stigmas associated with food stamp program recepients.  Additionally, this information may also serve to encourage others to apply as well. The DSWG is helping CFA process the text data so that spelling errors are corrected, which will allow personal information to be removed effectively and aid in downstream analysis.  We also plan to use machine learning and NLP methods such as topic modelling to help classify and quantify circumstances in the response text.

## Needs of this project

- NLP processing Pipelines
- SpellChecker Improvements
- Data exploration/descriptive statistics
- Topic Modelling

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. The Data for this project contains sensitive information.  Please reach out to the leads for access.
3. Data Processing Code (including our custom spellchecker) can be accessed [here](https://github.com/sfbrigade/datasci-cfa-calfresh/tree/master/2-Data-Processing)


## Featured Notebooks/Analysis/Deliverables
* [Calfresh Text Processing Notebook](https://github.com/sfbrigade/datasci-cfa-calfresh/blob/master/2-Data-Processing/CalFresh-Text-Processing.ipynb)


## Contributing DSWG Members

**Team Leads (Contacts) : [Rocio Ng](https://github.com/RocioSNg)(@rocio)**

#### Other Members:

|Name     |  Slack Handle   | 
|---------|-----------------|
|[Ian Patrick Colrick ](https://github.com/icolrick)| @icorlick      |
|[Melodie Belot] |     @Melodie   |

## Contact
* If you haven't joined the SF Brigade Slack, [you can do that here](http://c4sf.me/slack).  
* Our slack channel is `#datasci-calfresh`
* Feel free to contact team leads with any questions or if you are interested in contributing!
