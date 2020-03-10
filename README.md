This is a proof of concept to recurrently fetch data from pubmed and extract words into a psql data base. A working prototype of this is hosted on google cloud at http://35.236.199.231:5000/

indexer.py takes a csv file (oa_file_list.csv) containing a list of pubmed article links. indexer.py saves these links in the psql database in a structured format. The structure of the database can be found in genie.sql.

extractor.py takes each link in the database and fetches the article from that link. extractor then parses the article as xml and obtains the abstract. Next, words from the abstract will be extracted using a scispacy model. The words in each abstract will be used to update the total word count of each word in the database.

finally, app.py is a flask server that serves an html table containing a list of 1000 most popular words from the database.

I hope ideas from this proof of concept will help you in any way. I'd be happy to discuss any aspect of this proof of concept.

source .env
psql postgresql://postgres:genie1234@localhost:5432/genie
nohup flask run --host 0.0.0.0 > server.out &
