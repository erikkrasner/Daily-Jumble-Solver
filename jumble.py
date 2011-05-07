#!/usr/bin/env python
from itertools import permutations, combinations
import sys
import os

class Word(str):
        def withrarity(self,rarity):
                self.rarity = rarity
                return self

def key(letters):
        return tuple(sorted(letters))

word_dict = {}
def load_dictionary(file_name):
        word_file = open(file_name,'r')
        for line in word_file:
                word, rarity = line.split()
                word = Word(word).withrarity(int(rarity))
                k = key(word)
                if k in word_dict:
                        word_dict[k].append(word)
                else:
                        word_dict[k] = [word]

def dict_file_name(first_letter,length):
        return "word_lists/%s%d" % (first_letter,length)

loaded = set()
directory = set(os.listdir('word_lists'))
def unjumble(jumbled_word):
        k = key(jumbled_word)
        if (k[0],len(k)) not in loaded and k[0] + `len(k)` in directory:
                load_dictionary(dict_file_name(k[0],len(k)))
                loaded.add((k[0],len(k)))
        return word_dict[k] if k in word_dict else []

def jumble_solve(jumble_list, word_lengths):
	def product(list_of_lists):
		if not list_of_lists: yield ()
		else:
			for element in list_of_lists[0]:
				for combo in product(list_of_lists[1:]):
					yield (element,) + combo
	def tuple_difference(tup1, tup2):
		copy = list(tup1)
		for elem in tup2:
			copy.remove(elem)
		return tuple(copy)
	make_words_memo = {}
	def make_words(letter_set,word_lengths):
		assert sum(word_lengths) == len(letter_set)
		if (letter_set,word_lengths) in make_words_memo:
                        return make_words_memo[letter_set,word_lengths]
		if not word_lengths:
			return ((),)
		else:
			word_set = set()
			for letters in combinations(letter_set,word_lengths[0]):
				word_lists = make_words(tuple_difference(letter_set,letters),word_lengths[1:])
				for word_list in word_lists:
					for word in unjumble(letters):
						solution = (word,) + word_list
						word_set.add(solution)
			make_words_memo[letter_set,word_lengths] = word_set
			return word_set
	solutions = [unjumble(scramble) for scramble, _ in jumble_list]
	word_lists = set()
	for solution in product(solutions):
		letters = ()
		for index, guess in enumerate(solution):
			location_set = jumble_list[index][1]
			letters += tuple([guess[n-1] for n in location_set])
		for word_list in make_words(letters,word_lengths):
                        if (solution, word_list) not in word_lists:
                                yield solution, word_list
                                word_lists.add((solution,word_list))
                                
def minus_total_rarity(jumble_solution):
        scrambles,main_puzzle_solution = jumble_solution
        return sum([word.rarity for word in scrambles + main_puzzle_solution])

def input_loop():
	print """For every clue enter in the scrambled word, followed by a space, followed by the positions of the
characters that will figure in the final answer, separated by spaces.
For example: inyar 2 3
When you're done, just press enter."""
	inp = raw_input()
	jumble_list = ()
	while inp:
		words = inp.split()
		jumble_list += ( (words[0],tuple([int(x) for x in words[1:]])), )
		inp = raw_input()
	print """Now enter the final answer, writing the length of each unknown word.
For example: 3 an 8"""
	inp = raw_input()
	word_lengths = ()
	main_puzzle_words = inp.split()
	for word in main_puzzle_words:
		if word.isdigit():
			word_lengths += (int(word),)
        jumble_solutions = sorted([solution for solution in jumble_solve(jumble_list,word_lengths)], key = minus_total_rarity)
	for scrambles, main_puzzle_solution in jumble_solutions:
                for index, unscramble in enumerate(scrambles):
                        print ("%d. %s" % (index + 1, unscramble)),
                print
                next_solution_index = 0
                for word in main_puzzle_words:
                        if word.isdigit():
                                print main_puzzle_solution[next_solution_index],
                                next_solution_index += 1
                        else:
                                print word,
                print

if __name__ == '__main__':
    input_loop()
