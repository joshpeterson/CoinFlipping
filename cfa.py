import unittest
import sys
import random

def main():
    if sys.argv[1] == "Problem 1":
        problem1(int(sys.argv[2]), False)
    if sys.argv[1] == "Problem 2":
        problem2(int(sys.argv[2]))
    if sys.argv[1] == "test":
        sys.argv.remove("test")
        unittest.main()

def problem1(iterations, displayAllDuesValues):
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

def duesStrategyChooser(chosenSequences, iterations):
    duesValues = {}
    for chosenSequence in chosenSequences:
        duesValues[chosenSequence] = take(duesGenerator(chosenSequence), iterations)

    return duesValues

def duesGenerator(chosenSequence):
    while True:
        yield calculateDues(chosenSequence)

def calculateDues(chosenSequence):
    return calculateDuesWithFlipGenerator(chosenSequence, flipGenerator())

def calculateDuesWithFlipGenerator(chosenSequence, flips):
    allFlips = []
    while True:
        allFlips.append(flips.next())
        if chosenSequence in ''.join(allFlips):
            break
    return len(allFlips)

def flipTournament(yourSequence, opponentSequence):
    return flipTournamentWithFlipGenerator(yourSequence, opponentSequence, flipGenerator())

def flipTournamentWithFlipGenerator(yourSequence, opponentSequence, flips):
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
    return random.choice(['H', 'T'])

def flipGenerator():
    while True:
        yield flipCoin()

def generateRandomHeadTailSequence(size):
    return ''.join(take(flipGenerator(), size))

def take(generator, n):
    values = []
    i = 0;
    for value in generator:
        if i >= n:
            break
        values.append(value)
        i += 1

    return values

def mean(values):
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
        self.assertEqual(flipTournamentWithFlipGenerator('HTHTH', 'THTHTH', (i for i in ['H','T', 'H', 'T', 'H'])), 'HTHTH')
    def test_SequenceWhichAppearsFirstButNotAtStartIsReturned(self):
        self.assertEqual(flipTournamentWithFlipGenerator('HTHTH', 'TTTHH', (i for i in ['H','T', 'T', 'T', 'H', 'H'])), 'TTTHH')
    def test_RaisesAnExceptionWhenSequencesAreTheSame(self):
        self.assertRaises(ValueError, flipTournamentWithFlipGenerator, 'HTHTH', 'HTHTH', (i for i in ['H','T', 'T', 'T', 'H']))

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
        self.assertEqual(calculateDuesWithFlipGenerator('HHHHH', (i for i in ['H','H', 'H', 'H', 'H'])), 5)
    def test_ReturnsSixWhenAllButFirstMatch(self):
        self.assertEqual(calculateDuesWithFlipGenerator('HHHHH', (i for i in ['T', 'H','H', 'H', 'H', 'H'])), 6)
    def test_ReturnsFiveWhenFirstFiveMatch(self):
        self.assertEqual(calculateDuesWithFlipGenerator('HHHHH', (i for i in ['H','H', 'H', 'H', 'H', 'H'])), 5)

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

if __name__ == '__main__':
    main()
