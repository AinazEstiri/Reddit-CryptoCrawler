import logging, sys
logging.disable(sys.maxsize)

import os, glob,json, lucene
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
from flask import Blueprint, render_template, request, redirect, url_for, session

display = Blueprint('display', __name__)
views = Blueprint('views', __name__)

def create_index(index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    store = SimpleFSDirectory(Paths.get(index_dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    json_files = glob.glob("Data/*.json")
    seen = set()
    
    for file_name in json_files:
        with open(file_name, 'r') as file:
            for line in file:
                try:
                    json_data = json.loads(line)
                    username = json_data.get('username')
                    timestamp = json_data.get('timestamp')
                    body = json_data.get('body')
                    title = json_data.get('title')
                    # missing code
                    ids = json_data.get('id')
                    if ids in seen: 
                        continue
                    seen.add(ids)
                    # added the id stuff 
                    doc = Document()
                    doc.add(Field('Username', str(username), StringField.TYPE_STORED))
                    doc.add(Field('Timestamp', str(timestamp), StringField.TYPE_STORED))
                    doc.add(Field('Body', str(body), TextField.TYPE_STORED))
                    doc.add(Field('Title',str(title), StringField.TYPE_STORED))
                    writer.addDocument(doc)
                except json.JSONDecodeError:
                    pass  # Skip invalid JSON lines silently

    writer.close()
#added word limit

def limit_words(text, limit): 
    words = text.split() 
    if len(words)<= limit:
        return text
    else: 
        return ' ' .join(words[:limit])+'...'
     
        

def retrieve(index_dir, query):
    print("retrieve")
    print("index_dir:", index_dir, "query:", query)
    try:
        store = SimpleFSDirectory(Paths.get(index_dir))
    except Exception as e:
        print(f"Failed to open directory: {e}")
    reader = DirectoryReader.open(store)
    searcher = IndexSearcher(reader)
    searcher.setSimilarity(BM25Similarity())

    parser = QueryParser('Body', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
       # limited_text = limit_words(doc.get("Body"), 50) 
        topkdocs.append({
            "score": hit.score,
            #old line
           # "text": doc.get("Body"),
           # "text": limited_text,
            "text": limit_words(doc.get("Body"), 50), 
            "title": doc.get("Title")
        })

    reader.close()
    return topkdocs


@display.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        vm_env = lucene.getVMEnv() 
        vm_env.attachCurrentThread()

        query = session.get('query')
        print("session stuff: ")
        print(query)
        index_dir = 'sample_lucene_index/'            
        documents = retrieve(index_dir, query)
#        print("successfully got documents") 
        print(documents)
    else:
        qsearch = request.form.get('searchQuery')
        if not qsearch:
            return redirect(url_for('views.home'))
        else:
            session['query'] = qsearch
            print(qsearch.split())
            return redirect(url_for('display.results'))
    return render_template("results.html", documents=documents, query=query)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        qsearch = request.form.get('searchQuery')
        if qsearch:
            session['query'] = qsearch
            print(qsearch.split())
            return redirect(url_for('display.results'))
    return render_template("home.html")

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
create_index('sample_lucene_index/')
results = retrieve('sample_lucene_index/', 'crypto')
# print("after creating the index and retrieving the results from data")
print(results)

