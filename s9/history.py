#
# history.py
#


class History(object):

    def __init__(self):
        self.weightedSentences = []


    def add(self, sent):
        """
        Adds the given sentence with current weight to the history list.
        """
        self.weightedSentences.append(sent)


    def load_history(fpath):
        history = History()
                
        with open(fpath) as f:
            for line in f:
                newSent = []                
                line = line.strip()

                if len(line) == 0:
                    continue

                if line == '#':
                    continue

                line = line.replace('[', '', 1)
                line = line.rstrip(']')
                
                entries = line.split(',')

                weight = eval(entries.pop(-1))

                for e in entries:
                    e = e.strip()
                    e = e.replace('"', '')
                    e = e.replace("'", "")
                    e = e.replace('[', '')
                    e = e.replace(']', '')
                    newSent.append(e)
                
                history.add(list((newSent, weight)))
                
        f.close()
        return history


    def save_history(self, fpath, sents):
        with open(fpath, 'w') as f:
            for s in sents:
                f.write(str(s) + '\n')
        f.close()


    def updateWeight(self, sent, weight):
        for s in self.weightedSentences:
            if s[0] == sent:
                s[1] = weight
                

    def incrementWeight(self, sent):
        for s in self.weightedSentences:
            if s[0] == sent:
                s[1] = s[1] + 1

    def __str__(self):
        return self.weightedSentences


    def sentence_exist(self, sent):
        for s in self.weightedSentences:
            if s[0] == sent:
                return True
        return False


    def get_weight(self, sent):
        for s in self.weightedSentences:
            if s[0] == sent:
                return s[1]
        return -1


if __name__ == "__main__":

    hFile = 'history.txt'
    
    history = History.load_history(hFile)

    for s in history.weightedSentences:
        print(s)
#        print(type(s))

    print('-' * 5)
    
    newSent = ['see', 'Bob', 'run', 'fast']
    newWeight = 5
    history.add(list((newSent, int(newWeight))))

    for s in history.weightedSentences:
        print(s)

    
    history.save_history(hFile, history.weightedSentences)

    print('-' * 5)

    
    history.updateWeight(['see', 'Bob', 'run'], 3)

    for s in history.weightedSentences:
        print(s)

    print('-' * 5)

    history.incrementWeight(['see', 'Bob'])

    for s in history.weightedSentences:
        print(s)    

    history.save_history(hFile, history.weightedSentences)

    print(history.sentence_exist(['see', 'Mary']))

    print(history.sentence_exist(['see', 'Pookie', 'run']))

    print("ok")
