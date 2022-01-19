# Define Spellclean_textker  Peter Novigs
class SpellChecker:
    
    def __init__(self, freq_word, letters):
        
        self.w_rank = {}
        self.letters = letters
        
        N = sum(freq_word.values())
        for term in freq_word:
            self.w_rank[term] = freq_word[term] / N
    
    def P(self, word): 
        "Probability of 'word'."
        return self.w_rank.get(word, 0)

    def known(self, words): 
        "The subset of 'words' that appear in the dictionary of w_rank."
        return set(w for w in words if w in self.w_rank)

    def edits1(self, word):
        "All edits that are one edit away from 'word'."
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in self.letters]
        inserts    = [L + c + R               for L, R in splits for c in self.letters]
        
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word): 
        "All edits that are two edits away from 'word'."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
    
    def correction(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key = self.P)
    
    def candidates(self, word): 
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])
