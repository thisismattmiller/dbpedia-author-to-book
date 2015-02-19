import rdflib, json
from urllib2 import URLError


class DBpediaAuthorBooks(object):


	#what predicates we will look for with the assumtion that the subject will be a book
	author_predicates = [
		'http://dbpedia.org/ontology/author'
	]

	#what predicate to return the object for each book
	book_predicates = [
		'http://dbpedia.org/ontology/abstract',
		'http://dbpedia.org/property/name',
		'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
		'http://xmlns.com/foaf/0.1/depiction',
		'http://www.w3.org/2000/01/rdf-schema#comment'
		'http://www.w3.org/2000/01/rdf-schema#label'
	]

	dbpedia_resource_base = "http://dbpedia.org/resource/"


	author_uri = ""



	def __init__(self,author_uri):

		if author_uri.find("http://") == -1:
			author_uri = self.dbpedia_resource_base+author_uri

		self.author_uri = author_uri

		self.process_authors(author_uri)



	def process_authors(self,author_uri):

		g = self.load_graph(author_uri)

		books_uris = []
		for pred in self.author_predicates:
			books_uris += list(x for x in g.subjects(predicate=rdflib.URIRef(pred) ) )

		books = []

		for book_uri in books_uris:
			books.append(self.process_book(book_uri))

		self.books = books




	def process_book(self,book_uri):


		g = self.load_graph(book_uri)	

		book = {}

		for pred in self.book_predicates:

			results = list(x for x in g.objects(predicate=rdflib.URIRef(pred) ) )

			book[pred] = []

			for x in results:

				if type(x) != rdflib.term.URIRef:
					book[pred].append({ "lang" : x.language, 'value' : x.value })
				else:
					#lets not go any deeper into retriving more uris
					book[pred].append({ "lang" : 'en', 'value' : str(x) })

				 

		return book


	def load_graph(self,uri):

		g=rdflib.Graph()

		try:
			g.parse(uri)
		except URLError as e:
			print ("Network error")
			raise e

		return g


	def print_books(self):

		print (json.dumps(self.books,indent=2))

if __name__ == "__main__":

	author_books = DBpediaAuthorBooks('George_Eliot')

	author_books.print_books()
