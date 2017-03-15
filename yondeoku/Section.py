class Section(object):
	'''Language independent Section class. Objects of this type
	are to be found in the 'sections' Array on gBlock instances.
	{Sections}'s lemma property is initialised as an empty [].
	The appropriate language's lemmatizer is then mapped over a
	{gBlock}'s 'sections' Array to fill in the lemma Arrays.
	The Section's blockRef property is a simple 2 element Array
	representing the index in and out of the block's text property
	that corresponds to this section.'''

	def __init__(self, _in, _out, text):
		self.blockRef = [_in, _out]
		self.text = text
		self.lemmas = []