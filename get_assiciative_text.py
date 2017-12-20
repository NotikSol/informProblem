#!/usr/bin/python3
from get_definition import get_definition
from get_keywords2 import get_keywords
from normalize_term import normalize_term
import sys

tree = {}

def get_graph(word0 = "Дерево", n = 0):
	global tree

	print(n, word0, file=sys.stderr)

	if n < 3:
		definition_text = get_definition(word0)
		keywords = get_keywords(definition_text)

		for word in keywords:
			if word != word0 and len(word) > 3:
				tree.update({(word0, word):1})
				get_graph(word, n+1)

		#print(tree)

if __name__ == '__main__':
	get_graph('файзрахманов_рустам_абубакирович')
	print("digraph g {\n\trankdir=LR;")
	for definition, word in tree.keys():
		definition, word = [ normalize_term(_) for _ in [definition, word] ]
		if definition != word: print("\t\"%s\" -> \"%s\"" % (definition, word))
	print("}")
	#graph = get_graph(definition = "дерево")
	# понятие -> понятие2
