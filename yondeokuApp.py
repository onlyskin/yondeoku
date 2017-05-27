import json

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from yondeoku.languageAPI import languageAPI
from yondeoku.gBlock import gBlock
from yondeoku.Section import Section
from yondeoku.Lemma import Lemma
# from yondeoku.make_study_list import make_study_list

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/real.db'
db = SQLAlchemy()
db.init_app(app)

DEBUG = True
PORT = 3000
HOST = '0.0.0.0'

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'

map_table = db.Table('user_word_map_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('word_id', db.Integer, db.ForeignKey('word.id')),
    )

class User(db.Model):
	id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	known = db.relationship('Word', secondary=map_table, backref='users')
	threshold = db.Column(db.Integer, nullable=False, default=8)
	blocks = db.relationship('Block', backref="user")
	__table_args__ = (
		db.CheckConstraint(username != '', name='check_username_not_empty_string'),
		db.CheckConstraint(password != '', name='check_password_not_empty_string'),
		db.CheckConstraint(threshold > 0, name='check_threshold_greather_than_0'),
		)

class Block(db.Model):
	id = db.Column(db.Integer, db.Sequence('block_id_seq'), primary_key=True)
	language = db.Column(db.String, nullable=False)
	text = db.Column(db.String, nullable=False)
	# readRanges are stored as a jsonified list of lists
	read_ranges = db.Column(db.String, nullable=False, default='[]')
	user_id = db.Column(db.ForeignKey('user.id'))
	__table_args__ = (
		db.CheckConstraint(language != '', name='check_language_not_empty_string'),
		db.CheckConstraint(text != '', name='check_text_not_empty_string'),
		)

class Word(db.Model):
	id = db.Column(db.Integer, db.Sequence('word_id_seq'), primary_key=True)
	language = db.Column(db.String, nullable=False)
	word = db.Column(db.String, nullable=False)
	__table_args__ = (
		db.UniqueConstraint('language', 'word'),
		db.CheckConstraint(language != '', name='check_language_not_empty_string'),
		db.CheckConstraint(word != '', name='check_word_not_empty_string'),
		)

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'

def _get_all_read_sections(gBlocks):
    all_sections = reduce(lambda a, b: a + b, [x.sections for x in gBlocks])
    read_sections = [s for s in all_sections if s.read]
    return read_sections

def _get_user_read_sections(user_id, language):
    gBlocks = _get_user_gBlocks(user_id, language)
    return _get_all_read_sections(gBlocks)

def _get_user_known_words(user_id, language):
    user = User.query.filter_by(id=user_id).first()
    return [w.word for w in user.known if w.language == language]

def _get_grammatical_words(block_id):
    language = _get_block_language(block_id)
    return languageAPI[language]().grammarWords

def _get_block_language(block_id):
    block = Block.query.filter_by(id=block_id).first()
    return block.language

def _get_user_gBlocks(user_id, language):
    user = User.query.filter_by(id=user_id).first()
    return [gBlock(x) for x in user.blocks if x.language == language]

from yondeoku._get_lemmas_above_threshold import _get_lemmas_above_threshold

def _get_lemmas_from_sections(sections):
    return reduce(lambda a, b: a + b, [x.lemmas for x in sections], [])

def _get_user_lemmas_above_threshold(user_id, language):
    gBlocks = _get_user_gBlocks(user_id, language)
    lemmas = _get_lemmas_from_sections(_get_all_read_sections(gBlocks))
    return _get_lemmas_above_threshold(lemmas, 8)

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
    	# this will only work once the user's blocks have been
    	# converted to gBlocks
        if isinstance(obj, User):
            return {
                "id": obj.id,
                "username": obj.username,
                "threshold": obj.threshold,
                "known": obj.known,
                "blocks": obj.gBlocks
            }
        if isinstance(obj, gBlock):
            return {
                "id": obj.id,
                "language": obj.language,
                "text": obj.text,
                "read_ranges": obj.readRanges,
                "sections": obj.sections,
                "readSections": obj.readSections
            }
        if isinstance(obj, Word):
            return {
                "language": obj.language,
                "word": obj.word
            }
        if isinstance(obj, Section):
        	return {
        		"text": obj.text,
        		"lemmas": obj.lemmas,
        		"blockRef": obj.blockRef,
                "read": obj.read
        	}
        if isinstance(obj, Lemma):
        	return {
        		"word": obj.word
        	}
        if isinstance(obj, set):
        	return list(obj)
        return super(ModelEncoder, self).default(obj)

def get_user_data_json(username):
    activeUser = User.query.filter_by(username=username).first()
    activeUser.gBlocks = map(lambda x: gBlock(x), activeUser.blocks)
    return json.dumps(activeUser, cls=ModelEncoder, sort_keys=True, indent=4,
            separators=(',', ': '))

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/tests')
def tests():
    return render_template('runner.html')

@app.route('/user/<username>', methods=['GET'])
def user(username):
	'''This retrieves the user data for user with specific
	username and returns it as json to the webpage.'''
	return get_user_data_json(username)

@app.route('/add_block/<username>', methods=['POST'])
def add_block(username):
    block_text = request.get_json()['text']
    block_language = request.get_json()['language']

    user = User.query.filter_by(username=username).first()
    b = Block(language=block_language, text=block_text)
    user.blocks.append(b)
    print user.blocks[-1].text
    db.session.add(user)
    db.session.commit()
    return get_user_data_json(username)

@app.route('/delete_block/<username>', methods=['POST'])
def delete_block(username):
    block_id = request.get_json()['id']

    block = Block.query.filter_by(id=block_id).first()

    db.session.delete(block)
    db.session.commit()

    return get_user_data_json(username)

from yondeoku._get_next_words import _get_next_n_words_and_section_indices

def make_study_list(user_id, block_id):
    current_block = Block.query.filter_by(id=block_id).first()
    current_gBlock = gBlock(current_block)

    above_threshold_word_set = _get_user_lemmas_above_threshold(user_id, current_block.language)
    grammatical_word_set = _get_grammatical_words(block_id)
    known_word_set = _get_user_known_words(user_id, current_block.language)
    exclude_set = above_threshold_word_set.union(grammatical_word_set).union(known_word_set)

    return _get_next_n_words_and_section_indices(current_gBlock, exclude_set, 10)

@app.route('/get_study_words', methods=['POST'])
def get_next_words():
    print 'get study words received post'
    print request.get_json()

    user_id = request.get_json()['user_id']
    block_id = request.get_json()['block_id']
    study_list = make_study_list(user_id, block_id)

    return json.dumps(study_list, cls=ModelEncoder)

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'

if __name__ == '__main__':
	app.run(debug=DEBUG, host=HOST, port=PORT)
