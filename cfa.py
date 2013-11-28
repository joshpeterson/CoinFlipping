#
# This code can be used to solve the coin flipping problems proposed in the
# November 2013 issue of Communications of the ACM.
# http://cacm.acm.org/magazines/2013/11/169037-puzzled-coin-flipping/abstract
#
import unittest
import sys
import random
import argparse

def main():
    """ Parse arguments and execute the action requested by the user. """
    args = parseArguments()
    if args.test:
        sys.argv.remove(sys.argv[1])
        unittest.main()
    elif args.problem == 1:
        problem1(args.iterations, False)
    elif args.problem == 2:
        problem2(args.iterations)
    elif args.problem == 3:
        problem3(args.iterations)
    else:
        print 'Try using the -h option for usage details.'

def problem1(iterations, displayAllDuesValues):
    """ Execute the first problem.

    Parameters
    ----------
    iterations : int
        The number of iterations to use when running the simulation.
    displayAllDuesValues : bool
        True to output the value computed at each iteration, False to output only the average.

    """
    sequenceMeans = {}
    duesValues = duesStrategyChooser(allHeadsTailsCombinations, iterations)
    for chosenSequence in sorted(duesValues.keys()):
        sequenceMeans[chosenSequence] = mean(duesValues[chosenSequence])

    for chosenSequence in sorted(sequenceMeans.iterkeys(), key=lambda k: sequenceMeans[k]):
        if not displayAllDuesValues:
            print chosenSequence + ': ' + str(sequenceMeans[chosenSequence])
        else:
            print chosenSequence + ': ' + str(sequenceMeans[chosenSequence]) + ' ' + ''.join(str(duesValues[chosenSequence]))

def problem2(iterations):
    """ Execute the second problem.

    Parameters
    ----------
    iterations : int
        The number of iterations to use when running the simulation.

    """
    sequenceWins = {}
    for yourSequence in allHeadsTailsCombinations:
        for opponentSequence in allHeadsTailsCombinations:
            if yourSequence != opponentSequence:
                wins = 0
                for i in range(iterations):
                    if flipTournament(yourSequence, opponentSequence) == yourSequence:
                        wins += 1
                sequenceWins[yourSequence] = float(wins)/iterations

    for winningSequence in sorted(sequenceWins.iterkeys(), key=lambda k: sequenceWins[k], reverse=True):
        print winningSequence + ': ' + str(sequenceWins[winningSequence])

def problem3(iterations):
    """ Execute the third problem.

    Parameters
    ----------
    iterations : int
        The number of iterations to use when running the simulation.

    """
    goodBets = 0
    for i in range(iterations):
        winnings = 1
        for j in range(1000):
            oneHundredFlipSequence = take(flipGenerator(), 100)
            if oneHundredFlipSequence.count('H') == 50:
                winnings += 19
            else:
                winnings -= 1
        if winnings >= 1000:
            goodBets += 1

    print 'You made money ' + str(goodBets) + ' out of ' + str(iterations) + ' times.'

def duesStrategyChooser(chosenSequences, iterations):
    """ Return a dictionary mapping each possible head/tail sequence to a list
    containing the number of clips required to generate it at each iteration.

    Parameters
    ----------
    chosenSequences : list of string
       A list of head/tail sequences to test. 
    iterations : int
        The number of iterations to use when running the simulation.

    """
    duesValues = {}
    for chosenSequence in chosenSequences:
        duesValues[chosenSequence] = take(duesGenerator(chosenSequence), iterations)

    return duesValues

def duesGenerator(chosenSequence):
    """ Return a generator to calculate the number of flips required
    to obtain the given head/tail sequence. Each time it is called,
    a new set of flips will be used.

    Parameters
    ----------
    chosensequence : string
        The head/tail sequence to test.

    """
    while True:
        yield calculateDues(chosenSequence)

def calculateDues(chosenSequence):
    """ Return the number of flips required to obtain the given head/tail
    sequence.

    Parameters
    ----------
    chosensequence : string
        The head/tail sequence to test.

    """
    return calculateDuesWithFlipGenerator(chosenSequence, flipGenerator())

def calculateDuesWithFlipGenerator(chosenSequence, flips):
    """ Return the number of flips required to obtain the given head/tail
    sequence. Use the given generator to determine the series of flips.

    Parameters
    ----------
    chosensequence : string
        The head/tail sequence to test.
    flips : generator
        A generator which provides a series of head/tail flips.

    """
    allFlips = []
    while True:
        allFlips.append(flips.next())
        if chosenSequence in ''.join(allFlips):
            break
    return len(allFlips)

def flipTournament(yourSequence, opponentSequence):
    """ Return the one of the two input head/tail sequences that occurs first
    in a series of flips.

    Parameters
    ----------
    yourSequence : string
        One head/tail sequence to test.
    opponentSequence : string
        Another head/tail sequence to test.

    """
    return flipTournamentWithFlipGenerator(yourSequence, opponentSequence, flipGenerator())

def flipTournamentWithFlipGenerator(yourSequence, opponentSequence, flips):
    """ Return the one of the two input head/tail sequences that occurs first
    in a series of flips. Use the given generator to determine the series of flips.

    Parameters
    ----------
    yourSequence : string
        One head/tail sequence to test.
    opponentSequence : string
        Another head/tail sequence to test.
    flips : generator
        A generator which provides a series of head/tail flips.

    """
    if yourSequence == opponentSequence:
        raise ValueError('Sequences cannot have the same value: ' + yourSequence)
    allFlips = []
    while True:
        allFlips.append(flips.next())
        flipSequence = ''.join(allFlips)
        if yourSequence in flipSequence:
            return yourSequence
        if opponentSequence in flipSequence:
            return opponentSequence

def flipCoin():
    """ Return a random 'H' or 'T' string. """
    return random.choice(['H', 'T'])

def flipGenerator():
    """ Return a generator for a random head/tail sequence. """
    while True:
        yield flipCoin()

def take(generator, n):
    """ Return a list of values from a generator.

    Parameters
    ----------
    generator : generator
        A generator to iterate.
    n : int
        The number of values to return.

    """
    values = []
    i = 0;
    for value in generator:
        if i >= n:
            break
        values.append(value)
        i += 1

    return values

def mean(values):
    """ Compute the mean of a list fo values.

    Parameters
    ----------
    values : list of int
        A list of numbers to average.

    """
    if not values:
        return 0
    return float(sum(values))/len(values)

allHeadsTailsCombinations = [
    'HHHHH', 'HHHHT', 'HHHTH', 'HHHTT',
    'HHTHH', 'HHTHT', 'HHTTH', 'HHTTT',
    'HTHHH', 'HTHHT', 'HTHTH', 'HTHTT',
    'HTTHH', 'HTTHT', 'HTTTH', 'HTTTT',
    'THHHH', 'THHHT', 'THHTH', 'THHTT',
    'THTHH', 'THTHT', 'THTTH', 'THTTT',
    'TTHHH', 'TTHHT', 'TTHTH', 'TTHTT',
    'TTTHH', 'TTTHT', 'TTTTH', 'TTTTT']

class FlipTournamentTests(unittest.TestCase):
    def test_SequenceWhichAppearsFirstIsReturned(self):
        self.assertEqual(flipTournamentWithFlipGenerator('HTHTH', 'THTHTH', mockFlipGenerator('HTHTH')), 'HTHTH')
    def test_SequenceWhichAppearsFirstButNotAtStartIsReturned(self):
        self.assertEqual(flipTournamentWithFlipGenerator('HTHTH', 'TTTHH', mockFlipGenerator('HTTTHH')), 'TTTHH')
    def test_RaisesAnExceptionWhenSequencesAreTheSame(self):
        self.assertRaises(ValueError, flipTournamentWithFlipGenerator, 'HTHTH', 'HTHTH', mockFlipGenerator('HTTTH'))

class DuesStrategyChooserTests(unittest.TestCase):
    def test_ReturnsDictionaryWithInputSequenceAsAKey(self):
        self.assertTrue('TTTTT' in duesStrategyChooser(['TTTTT'], 1).keys())
    def test_ReturnsDictionaryWithSecondInputSequenceAsAKey(self):
        self.assertTrue('HHHHH' in duesStrategyChooser(['TTTTT', 'HHHHH'], 1).keys())
    def test_EachSequenceIsAddedOnlyOnce(self):
        self.assertEqual(len(duesStrategyChooser(['TTTTT', 'TTTTT'], 1).keys()), 1)
    def test_LengthOfValueListIsNumberOfIterations(self):
        self.assertEqual(len(duesStrategyChooser(['TTTTT'], 8)['TTTTT']), 8)

class CalculateDuesTests(unittest.TestCase):
    def test_ReturnsFiveWhenAllMatch(self):
        self.assertEqual(calculateDuesWithFlipGenerator('HHHHH', mockFlipGenerator('HHHHH')), 5)
    def test_ReturnsSixWhenAllButFirstMatch(self):
        self.assertEqual(calculateDuesWithFlipGenerator('HHHHH', mockFlipGenerator('THHHHH')), 6)
    def test_ReturnsFiveWhenFirstFiveMatch(self):
        self.assertEqual(calculateDuesWithFlipGenerator('HHHHH', mockFlipGenerator('HHHHHH')), 5)

class FlipGeneratorTests(unittest.TestCase):
    def test_ReturnsTenFlips(self):
        self.assertEqual(len(take(flipGenerator(), 10)), 10)

class TakeTests(unittest.TestCase):
    def test_TakeOneGetsFirstValue(self):
        self.assertEqual(take(self.integerGenerator(10), 1), [1])
    def test_TakeFiveGetsFirstFiveValues(self):
        self.assertEqual(take(self.integerGenerator(10), 5), [1, 2, 3, 4, 5])
    def test_TakeWithMoreValuesThanGeneratorGetsAllPossibleValues(self):
        self.assertEqual(take(self.integerGenerator(3), 5), [1, 2, 3])
    def test_TakeZeroGetsEmptyList(self):
        self.assertEqual(take(self.integerGenerator(3), 0), [])

    def integerGenerator(self, n):
        i = 1
        while i <= n:
            yield i
            i += 1 

class MeanTests(unittest.TestCase):
    def test_MeanOfEmptyListIsZero(self):
        self.assertEqual(mean([]), 0)
    def test_CalculatesMeanOfList(self):
        self.assertEqual(mean([1, 2, 3, 4]), 2.5)

def mockFlipGenerator(sequence):
    """ Return a generator that provides each character in a string, one at a time.
    Parameters
    ----------
    sequence : string
        The string to parse and provide input to the generator.
    """
    for character in sequence:
       yield character

def parseArguments():
    """ Parse the command line arguments to this utility. """
    parser = argparse.ArgumentParser(description = 'This is a utility which uses Monte Carlo simulations to solve the Coin Flippers of America puzzles from the Communications of the ACM magazine (November 2013 issue).')
    parser.add_argument('-t', '--test', help='execute unit tests', action='store_true')
    parser.add_argument('-p', '--problem', help='perform problem 1, 2, or 3', choices=[1, 2, 3], type=int)
    parser.add_argument('-i', '--iterations', help='number of iterations to use', type=int)
    return parser.parse_args()

if __name__ == '__main__':
    main()
