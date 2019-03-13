from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import WordPunctTokenizer as WPT

wt = WPT()
ma = MA()

def normalize_term(term):
	rez = []
	for word in wt.tokenize(term):
		try:
			rez += [ma.parse(word)[0].normal_form]
		except (IndexError):
			print(word)
	return ' '.join(rez).strip('\n')

if __name__ == '__main__':
	print(normalize_term("какие-то длинные слова"))
