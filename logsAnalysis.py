#!/usr/bin/env python3
'''
The goal of this application is to do most of the heavy lifitng in SQL
and to only use python code when necessary. The end user is not required
to create any views to run this program. Just run python3 logsAnalysis.py
in your terminal.
'''

import psycopg2

db_name = "news"

def fetch_query_results(query):
	# Connect to database and fetch query resuslts for a given query.
	db = psycopg2.connect(database=db_name)
	c = db.cursor()
	c.execute(query)
	results = c.fetchall()
	db.close()
	return results

def print_query_results(query_results):
	# Print query results for a fetched query.
    print(query_results[1])
    for index, results in enumerate(query_results[0]):
        print(
            "\t", index+1, "-", results[0],
            "\t ---> ", str(results[1]), "views")


def print_error_results(query_results):
	# Print the error results for the last question.
    print(query_results[1])
    for results in query_results[0]:
        print("\t", results[0], "--->", str(results[1]) + "% errors")

# The following are the three questions requested for this assignment:

# What are the most popular three articles of all time?
ques1_title = ("What are the most popular three articles of all time?")
query1 = (
     "select articles.title, count(*) as views "
     "from articles inner join log on log.path "
     "like concat('%', articles.slug) "
     "where log.status like '%200%' group by " 
     "articles.title, log.path order by views desc limit 3")

# Who are the most popular article authors of all time?
ques2_title = ("Who are the most popular article authors of all time?")
query2 = (
    "select authors.name, count(*) as views from articles inner "
    "join authors on articles.author = authors.id inner join log "
    "on log.path like concat('%', articles.slug) where "
    "log.status like '%200%' group "
    "by authors.name order by views desc")

# On which days did more than 1% of requests lead to errors
ques3_title = ("On which days did more than 1% of requests lead to errors?")
query3 = (
    "select day, perc from ("
    "select day, round((sum(requests)/(select count(*) from log where "
    "substring(cast(log.time as text), 0, 11) = day) * 100), 2) as "
    "perc from (select substring(cast(log.time as text), 0, 11) as day, "
    "count(*) as requests from log where status like '%404%' group by day)"
    "as log_percentage group by day order by perc desc) as final_query "
    "where perc >= 1")

if __name__ == '__main__':
	# Store query results
	popular_articles_results = fetch_query_results(query1), ques1_title
	popular_authors_results = fetch_query_results(query2), ques2_title
	load_error_days = fetch_query_results(query3), ques3_title

	# Print formatted output
	print_query_results(popular_articles_results)
	print_query_results(popular_authors_results)
	print_error_results(load_error_days)