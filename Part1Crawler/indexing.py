import os
import lucene

def createIndex(dir):
    if not os.path.exists(dir):
        os.makedir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
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

    for sample in sampleDoc:
        #IDK IF I WROTE THIS PART CORRECTLY AT ALL IM CONFUSED!
        id = sample['id']
        title = sample['title']
        url = sample['url']
        createdUCT = sample['created_utc']
        body = sample['selftext']
        postURLs = sample['postURLs']
        author = sample['author']
        ups = sample['ups']
        downs = sample['downs']
        numComments = sample['num_comments']
        comments = commentsList

        doc = Document()
        doc.add(Field('Id', str(id), metaType)
        doc.add(Field('Title', str(title), metaType)
        doc.add(Field('Url', str(url), metaType)
        doc.add(Field('Created_utc', str(createdUCT), metaType)
        doc.add(Field('Body', str(body), contextType)
        doc.add(Field('postURLs', str(postURLs), metaType)
        doc.add(Field('author', str(author), metaType)
        doc.add(Field('ups', str(ups), contextType)
        doc.add(Field('downs', str(downs), contextType)
        doc.add(Field('numComments', str(numComments), contextType
        doc.add(Field('comments', str(comments), contextType)

        writer.addDocument(doc)
    writer.close()




