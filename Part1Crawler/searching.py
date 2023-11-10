

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    #PLS CHANGE to meet our reddit variables and stuff:

    parser = QueryParser('Context', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs= searcher.search(parsed_query,10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc= searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "text": doc.get("Context")
        })

    print(topkdocs)