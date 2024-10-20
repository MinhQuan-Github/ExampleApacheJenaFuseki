import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, RDF
from tqdm import tqdm

BOOK = Namespace("http://example.org/book#")

df = pd.read_csv('books_chunk_1k.csv', on_bad_lines='skip', sep=';')

g = Graph()

output_file = 'books_chunk_1k.rdf'

with open(output_file, 'wb') as rdf_file: 
    batch_size = 50
    num_batches = len(df) // batch_size + 1

    for batch in tqdm(range(num_batches), desc="Converting to RDF"):
        start_idx = batch * batch_size
        end_idx = min((batch + 1) * batch_size, len(df))
        current_batch = df.iloc[start_idx:end_idx]

        for index, row in current_batch.iterrows():
            try:
                book_uri = URIRef(f"http://example.org/book/{row['ISBN']}")

                g.add((book_uri, RDF.type, BOOK.Book))
                g.add((book_uri, BOOK.hasISBN, Literal(row['ISBN'])))
                g.add((book_uri, BOOK.hasTitle, Literal(row['Book-Title'])))
                g.add((book_uri, BOOK.hasAuthor, Literal(row['Book-Author'])))
                g.add((book_uri, BOOK.hasPublicationYear, Literal(row['Year-Of-Publication'])))
                g.add((book_uri, BOOK.hasPublisher, Literal(row['Publisher'])))
                g.add((book_uri, BOOK.hasImageSmall, Literal(row['Image-URL-S'])))
                g.add((book_uri, BOOK.hasImageMedium, Literal(row['Image-URL-M'])))
                g.add((book_uri, BOOK.hasImageLarge, Literal(row['Image-URL-L'])))

                print(f"Added book: {row['Book-Title']} with ISBN: {row['ISBN']}")

            except Exception as e:
                print(f"Error processing row {index}: {e}")
                continue 

    rdf_file.write(g.serialize(format='xml').encode('utf-8')) 

print("Conversion completed successfully!")
