import requests

fuseki_endpoint = 'http://localhost:3030/books/sparql'
sparql_query = """
PREFIX ns1: <http://example.org/book#>

SELECT ?bookTitle ?authorName
WHERE {
  ?book ns1:hasTitle ?bookTitle .
  ?book ns1:hasAuthor ?authorName .
}
"""

response = requests.post(fuseki_endpoint, data={'query': sparql_query})

if response.status_code == 200:
    print(response.json()) 
else:
    print(f"Error: {response.status_code}")
