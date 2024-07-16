    A python class for worlding. 

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

    # Okay, clint looks good (as it often does)

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
    gggng: shook
    nygng: showy
    yygng: smoky
    ngggg: spoof
    ggggg: spook
    nggyg: swoop

    # yes, spook is our optimal guess: if it's right, great, if not, it's result
    # will tell us the answer. Compare to a less-optimal choice, spoof:

    >>> wd.print_groups('spoof')
    nggng: shook
    nygng: showy smoky
    ggggg: spoof
    ngggg: spook
    nggyg: swoop

    # Like spook it has a 1/6 chance of being right. But if it's wrong, there is
    # a 2-in-5 chance of the next guess being 50/50, taking us to 5 guesses
    # instead of 4.

    # Happy wordling!
