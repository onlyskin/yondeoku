Decided:
- all APIs should interact with the database model
- we have our own user/block abstractions, this is because:
	- there is derived information which it is not sensible to store in the database, either because:
		- the exact implementations may change causing slight changes to the derived information
		- the information is quite large and in more abstracted forms
- separate vocab list generators etc which consume our user/block abstractions




Questions:
- should we have a gUser class as well as a gBlock class or is it unnecessary?
- should we do the processing to work out what words are new in a given section on the server side or on the client side (currently client)
	- the language absolutely known list would have to be passed down to the server
	- all known words would have to be passed down to the server
- how should the abs known grammar words go down?
	- should really be initialised at the start of the website opening
	- eventually for efficiency's sake would need to be specific to the users block's language, but for now not necessary


GUSER OBJECTS
- id property
- unique 'username' property ''
- threshold property
- gBlocks property [{gBlock}]
- known property {'ja': [], 'pl': []}

GBLOCK OBJECTS
- 'language' property as ''
- 'text' property as ''
- 'sections' property as [{Section}...]
- 'readRanges' property as [[]...]

BLOCK MODEL
- 'id' column INTEGER
- 'language' column STRING
- 'text' column STRING
- 'read_ranges' column STRING
- 'user_id' column as FOREIGN KEY INTEGER
- 'user' column as backref to USER MODEL OBJ

DEFINERS
All definers have:
- 'language' property as ''
- define method
	- takes a single lemma
	- returns [{Definition}...]

DEFINITION OBJECTS
- found as ''
- definition []
- pronunciation ''


SECTIONIZERS
All sectionizers have:
- 'language' property as ''
- sectionize method
	- takes a text ''
	- returns [{Section}]

SECTION OBJECTS
All {Section} objects should be found in the 'sections' array
stored on a {gBlock} object
- blockRef [_in, _out]
- text ''
- lemmas set()


LEMMATIZERS
All lemmatizers have:
Array property to a [{Lemma}...]
- 'language' property as ''
- lemmatize method
- takes a Section object
- returns a set({Lemma}...)

LEMMA OBJECTS
All lemmas objects should be found in the 'lemmas' array
stored on a {Section} object
- lemma
- optional index in and out??

GRAMMARWORDS
- a python list variable defined in a file
- contains a list of all the basic grammatical words for the given language

languageAPI - a dictionary mapping language strings to their LangTools class object (see below)

LangTools Class - an object with properties for the language specific functions, etc. that must be defined for each language, where functions, the properties are generally references to constructor functions
- sectionizer
- lemmatizer
- definer
- grammarwords





ROUTE SPECIFIC FUNCTIONS
yondeoku.define.makeDefinitionListFromLemmaList
- takes a list of Lemma objects
- returns a list of lists of Definition objects