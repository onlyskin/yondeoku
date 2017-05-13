import codecs

from yondeokuApp import db, app, User, Block, Word

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/fake.db'

ctx = app.app_context()
ctx.push()

db.create_all()

me = User(username='Sam', password='password')

def get_blocks_from_files():
	def block_from_filename(filename, language):
		with codecs.open('backup/' + filename, 'r', 'utf-8') as f:
			return Block(language=language, text=f.read())

	pl_files = ['block' + str(x) for x in range(4)]
	pl_blocks = map(lambda x: block_from_filename(x, 'pl'), pl_files)
	ja_files = ['block' + str(x) for x in range(4, 5)]
	ja_blocks = map(lambda x: block_from_filename(x, 'ja'), ja_files)
	all_blocks = pl_blocks + ja_blocks
	return all_blocks

def get_words_from_file():
	def get_words(filename, language):
		with codecs.open('backup/' + filename, 'r', 'utf-8') as f:
			def word_from_string(string):
				if string != '':
					return Word(language=language, word=string)

			words = f.read().split('\n')
			Words = map(lambda x: word_from_string(x), words)
			Words = filter(lambda x: x != None, Words)
			return Words
	pl_words = get_words('pl_known', 'pl')
	ja_words = get_words('ja_known', 'ja')
	return pl_words + ja_words

all_blocks = get_blocks_from_files()
for block in all_blocks:
	me.blocks.append(block)

all_words = get_words_from_file()
for word in all_words:
	me.known.append(word)

db.session.add(me)
db.session.commit()

