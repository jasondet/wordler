emport numpy as np
import urllib.request
from bs4 import BeautifulSoup

alphabet = 'abcdefghijklmnopqrstuvwxyz'

class Wordler:
    '''A python class for worlding. 

    Example usage: python -i wordler.py

    loading words...
    removing used words...
    enter help(wd) for usage info

    # Decide which starting word is the best today

    >>> wd.compute_entropy('soare')
    4.0793116892301775
    >>> wd.compute_entropy('roate')
    4.079071561863733

    # Try soare. Wordle say its green yellow grey grey grey.

    >>> wd.enter_result('soare', 'gynnn')
    scion scoff scold scoop scout scowl shock shook shoot shout shown showy sloop slosh sloth 
    smock smoky snoop snout snowy spoil spoof spook spool spoon spout stock stoic stomp stony 
    stood stool stoop stout swoon swoop synod 

    # Check entropies to pick the next word

    >>> wd.print_top_entropies()
                               s 0.1243          
                      f 0.2103 f 0.2478          
    f 0.2103 f 0.2103 o 0.2103 d 0.2814 f 0.2103 
    d 0.2814 d 0.2814 d 0.2814 m 0.3330 d 0.2814 
    i 0.2814 i 0.2814 m 0.2814 i 0.3330 i 0.2814 
    m 0.2814 m 0.3330 i 0.3330 y 0.3960 m 0.2814 
    y 0.3960 u 0.3960 y 0.3960 u 0.3960 u 0.3960 
    u 0.3960 k 0.4432 u 0.3960 k 0.5163 w 0.4432 
    w 0.4432 y 0.4637 w 0.4432 h 0.5221 y 0.4637 
    k 0.4432 w 0.5465 k 0.4432 w 0.5465 k 0.5163 
    l 0.5221 h 0.6437 h 0.5221 l 0.6035 h 0.6437 
    h 0.5221 l 0.6651 l 0.5221 p 0.6301 c 0.6714 
    n 0.5548 n 0.7096 c 0.5835 n 0.6396 l 0.6719 
    c 0.5835 c 0.7654 p 0.6301 o 0.6840 n 0.7219 
    p 0.6301 p 0.8549 n 0.6396 c 0.7486 p 0.8549 
    t 0.6633 t 0.9217 t 0.6633 t 0.7606 t 0.9217 
    by-letter max: lpnct 3.118883405489298

    # The highest-entropy choices have a t in the 2nd or 5th position. Look at
    # the entropies for the remaining positions for each choice

    >>> wd.print_top_entropies('.t...')
    ...
    i 1.1868          m 1.1868 i 1.2242 i 1.1868 
    m 1.1868          i 1.2242 y 1.2903 m 1.1868 
    w 1.2785          w 1.2785 h 1.3595 w 1.2785 
    y 1.2903          y 1.2903 w 1.3817 y 1.3511 
    k 1.3286          k 1.3286 k 1.3962 k 1.3962 
    h 1.3595          h 1.3595 n 1.4582 h 1.4788 
    l 1.4330          l 1.4330 l 1.5060 c 1.5358 
    n 1.4582          c 1.4983 p 1.5324 l 1.5454 
    c 1.4983          p 1.5324 o 1.5681 n 1.5874 
    p 1.5324          n 1.5358 c 1.6490 p 1.6995 
    by-letter max: ltncp 3.1704926623780665
    >>> wd.print_top_entropies('....t')
    ...
    i 1.1868 i 1.1868 m 1.1868 i 1.2242          
    m 1.1868 m 1.1868 i 1.2242 y 1.2903          
    w 1.2785 k 1.3286 w 1.2785 w 1.3817          
    y 1.2903 y 1.3511 y 1.2903 k 1.3962          
    k 1.3286 w 1.3817 k 1.3286 h 1.4318          
    l 1.4000 h 1.4994 l 1.4000 n 1.4582          
    h 1.4318 l 1.5407 h 1.4318 l 1.4731          
    n 1.4582 n 1.5714 c 1.4983 p 1.5324          
    c 1.4983 c 1.6115 p 1.5324 o 1.5681          
    p 1.5324 p 1.6995 n 1.5358 c 1.6490          
    by-letter max: lpnct 3.118883405489298

    # An entropy of 3.1-3.2 is near maximal, but those aren't words. Look at how
    # the entropy distributes by removing letters from the by-letter max

    >>> wd.print_top_entropies('l.nct')
    ...
             i 2.6250                            
             u 2.6250                            
             d 2.6533                            
             n 2.6551                            
             t 2.6624                            
             f 2.6747                            
             k 2.6766                            
             l 2.6766                            
             m 2.7263                            
             y 2.7350                            
             w 2.8849                            
             h 2.9457                            
             p 3.1189  
    
    # As soon as we add a vowel in the entropy drops considerably, to ~2.6-ish
    # Compare a few realistic options

    >>> wd.print_top_entropies('pluck')
    2.4911
    >>> wd.print_top_entropies('clint')
    2.5661
    >>> wd.print_top_entropies('tunic')
    2.1888
    >>> wd.print_top_entropies('cling')
    1.8870
    >>> wd.print_top_entropies('pinch')
    2.4494

    # Okay, clint looks good (often true)

    >>> wd.enter_result('clint', 'nnnnn')
    shook  1.5607
    showy  1.5607
    smoky  1.3297
    spoof  1.5607
    spook  1.7918
    swoop  1.5607

    # The top entropy is for spook. It's a 1/6 chance of being the answer, but
    # if it's wrong, will we be able to get it on the next try? Let's check the
    # groups of words corresponding to each possible wordle answer for spook:

    >>> wd.print_groups('spook')
    gnggg: shook
    gngnn: showy
    gngny: smoky
    ggggn: spoof
    ggggg: spook
    gyggn: swoop

    # yes, spook is our optimal guess: if it's right, great, if not, it's result
    # will tell us the answer. Compare to a less-optimal choice, spoof:

    >>> wd.print_groups('spoof')
    gnggn: shook
    gngnn: showy smoky
    ggggg: spoof
    ggggn: spook
    gyggn: swoop

    # Like spook it has a 1/6 chance of being right. But if it's wrong, there is
    # a 2-in-5 chance of the next guess being 50/50, taking us to 5 guesses
    # instead of 4.

    # Happy wordling!
    '''

    def __init__(self):
        self.reload_words()

    def reload_words(self, remove_used=True):
        ''' Reload the official wordle word list.

        Parameters
        ----------
        remove_used : bool
            Set to true to remove from the word list all wordle words used to
            date (requires internet connection)
        '''
        print('loading words...')
        self.words = np.loadtxt('words.txt', dtype='<U5')
        if not remove_used: return 
        print('removing used words...')
        link = 'https://www.fiveforks.com/wordle/block'
        uagent = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
        req = urllib.request.Request(link, headers={'User-Agent': uagent})
        html = BeautifulSoup(urllib.request.urlopen(req).read(), features="lxml")
        used_words = html.body.find('div', attrs={'id':'blist'}).text
        used_words = used_words.replace('\n', ' ')[1:-1].lower().split(' ')
        selected_words = []
        for word in self.words:
            if word not in used_words: selected_words.append(word)
        self.words = np.array(selected_words)

    def find_matches(self, guess, word, as_int=True):
        ''' Compute the wordle pattern for guess w.r.t. word

        Parameters
        ----------
        guess : str
            The guess to be tried. Must be 5 characters. The '.' character will
            be skipped
        word : str
            The word to be used to generate the pattern for guess. Must be 5
            characters.

        Returns
        -------
        pattern : str or int
            If as_int = True, pattern is a <=5-digit integer, where each digit
            corresponds to the character matches: 0 = skipped, 1 = grey, 2 =
            yellow, 3 = green
            If as_int = False, pattern is a string with 'n' = grey, 'y' =
            yellow, 'g' = green
        as_int : bool
            Flag to determine type of returned pattern
        '''

        pattern = ''
        for ii, letter in enumerate(guess):
            if letter == '.': 
                pattern += '.'
                continue
            if word[ii] == letter:
                pattern += 'g'
                continue
            if letter in word: 
                count = 0
                for jj, ll in enumerate(guess):
                    if ll == letter:
                        if word[jj] == ll: continue
                        count += 1
                    if jj == ii: break
                # count is now the minimum number of misplaced occurrences of
                # "letter" that must be found for a yellow assignment
                for jj, ll in enumerate(word):
                    if ll == letter:
                        if guess[jj] == ll: continue
                        count -= 1
                if count <= 0:
                    pattern += 'y'
                    continue
            pattern += 'n'
        if as_int:
            mapping = {'.':'0', 'n':'1', 'y':'2', 'g':'3'} 
            return int(''.join(map(lambda cc: mapping[cc], pattern)))
        return pattern

    def compute_entropy(self, guess):
        ''' Compute the Shannon Entropy for guess

        Loops over the words in the word list (that haven't been eliminated) and
        finds the fraction p_i corresponding to each pattern. Then computes
        
        entropy = Σ_i p_i ln(p_i)

        Parameters
        ----------
        guess : str
            The guess to be tried. Must be 5 characters. The '.' character will
            be skipped

        Returns
        -------
        entropy : float
            The Shannon Entropy for the provided guess

        Example
        -------
        >>> wd.compute_entropy('jason')
        3.011710995054887
        >>> wd.compute_entropy('j....')
        0.07033732735470374
        >>> wd.compute_entropy('....e')
        0.9963387354462877
        '''
        self.patterns = {}
        self.groups = {}
        for word in self.words:
            pattern = self.find_matches(guess, word)
            if pattern not in self.patterns:
                self.patterns[pattern] = 0
                self.groups[pattern] = []
            self.patterns[pattern] += 1
            self.groups[pattern].append(word)
        entropy = 0
        for count in self.patterns.values():
            pp = count/len(self.words)
            entropy -= pp*np.log(pp)
        return entropy

    def print_groups(self, guess):
        ''' Print the groups of words for each pattern for guess

        Useful for when you only have a few words left.

        Parameters
        ----------
        guess : str
            The guess to be tried. Must be 5 characters. The '.' character will
            be skipped
        '''
        self.compute_entropy(guess)
        letters = ['.', 'n', 'y', 'g']
        for pattern, word_list in self.groups.items():
            label = ''
            for ii in range(5):
                label += letters[int(pattern/10**(5-ii-1))]
                pattern = pattern % 10**(5-ii-1)
            print(f"{label}: {' '.join(word_list)}")

    def compute_entropies(self, guess):
        ''' Compute the entropies for all letters in all positions with "."'s in guess

        Parameters
        ----------
        guess : str
            The guess to be tried. Must be 5 characters. Should have at least
            one '.' (otherwise will just return with entropies = 0 for all
            letters for all positions)
        '''
        self.entropies = np.zeros((26,5))
        self.ie_sorted = np.zeros((26,5), dtype=int)
        for ii, letter in enumerate(alphabet):
            for pos in range(5):
                if guess[pos] != '.': continue
                test_guess = guess[:pos] + letter + guess[pos+1:]
                self.entropies[ii,pos] = self.compute_entropy(test_guess)
        for pos in range(5):
             self.ie_sorted[:,pos] = np.argsort(self.entropies[:,pos])

    def print_top_entropies(self, guess='.....'):
        ''' Print the entropies for all letters in all positions with "."'s in guess

        Ordered by position. Better guesses show up at the bottom.

        Parameters
        ----------
        guess : str
            The guess to be tried. Must be 5 characters. If guess contains no
            "."'s, will simply print the entropy of the guess.
        '''
        if '.' not in guess: 
            print(f'{self.compute_entropy(guess):.4f}')
            return
        self.compute_entropies(guess)
        for ii in range(26):
            line = ''
            for pos in range(5):
                jj = self.ie_sorted[ii][pos]
                if self.entropies[jj][pos] == 0: line += ' '*9
                else: line += f'{alphabet[jj]} {self.entropies[jj][pos]:.4f} '
            if line != ' '*len(line): print(line)
        if guess.count('.') <= 1: return
        max_guess = guess
        while '.' in max_guess:
            if max_guess != guess: 
                self.compute_entropies(max_guess)
            max_pos = np.argsort(self.entropies[self.ie_sorted[-1][:],range(5)])[-1]
            letter = alphabet[self.ie_sorted[-1][max_pos]]
            #print(max_guess, max_pos, letter)
            max_guess = max_guess[:max_pos] + letter + max_guess[max_pos+1:]
        print(f'by-letter max: {max_guess} {self.compute_entropy(max_guess)}')


    def enter_result(self, guess, result, ncols=15):
        ''' Eliminate words list by entering wordle's result for guess.

        Prints the words remaining.

        Parameters
        ----------
        guess : str
            The guess that was tried. 
        result : str
            The wordle result for guess. Should be a 5-character string with n,
            g, or y in each position, where n = grey (not in word), y = yellow,
            g = green
        '''
        idx = np.zeros(len(self.words), dtype=int)
        for jj, word in enumerate(self.words):
            if self.find_matches(guess, word, False) == result:
                idx[jj] = 1
        self.words = self.words[np.where(idx)]
        if ncols is not None: self.print_words(ncols)


    def print_words(self, ncols=15):
        ''' Print the words remaining in the list.

        Parameters
        ----------
        ncols : int
            The number of words to write per line
        '''
        icols = 0
        line = ''
        if len(self.words) < ncols*1.3: ncols = 1
        for word in self.words:
            line += word + ' '
            icols += 1
            if icols == ncols:
                if ncols == 1: line += f' {self.compute_entropy(line[:-1]):.4f}'
                print(line)
                line = ''
                icols = 0
        if line != '': print(line)

wd = Wordler()
print('enter help(wd) for usage info')
