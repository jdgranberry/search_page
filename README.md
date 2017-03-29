Search Page Data Mining & Information Retrieval Assignment
==========================================================
Assignment
----------
Create a web page featuring two methods
of search:

1. Create a webpage that allows the user the select two modes of search.
2. Use a web search API (from Google, Bing, etc.) to return webpage results.
3. Use an open source search platform, such as Lucene, Solr, or Elasticsearch, 
   to search an arbitrarily-chosen locally-hosted dataset.
3. Host the page in any manner you see fit.


Design Choices
--------------
1. The webpage is based on Flask with Jinja2 templating, written in Python 3.
   This was chosen for ease of use and speed of development. HTML templates 
   are purposefully bland since functionality is the priority here.
   
2. Google Custom Search Engine API is used to provide basic web search 
   functionality, albeit with no customization. It allows 100 searches per 
   day for its free tier, and auth keys are stored and loaded server side.
   
3. Elasticsearch is chosen, and to speed development, a containerized
   single-node Docker instance is being used. The dataset, `data/lyrics.csv`,
   contains 50 years of pop music lyrics and is loaded row-by-row using 
   Logstash.
   
4. The webpage is to be deployed to AWS EC2.

