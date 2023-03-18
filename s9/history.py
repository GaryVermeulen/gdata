#
# history.py
#


class History(object):

    def __init__(self):
        self.weightedSentences = []


    def add(self, sent):
        """
        Adds the given sentence with current weight to the history.
        """
        self.weightedSentences.append(sent)


    def load_history(fpath):
        """
        Loads the history from file
        """

        history = History()
                
        with open(fpath) as f:
            for line in f:
                line = line.strip()

                if len(line) == 0:
                    continue

                if line == '#':
                    continue
                
                entries = line.split(';')
                sentence = entries[0].strip()
                weight = entries[1].strip()
                history.add(sentence + ';' + weight)
        f.close()
        return history


    def save_history(self, fpath, sents):
        """
        Loads the history from file
        """
                
        with open(fpath, 'w') as f:
            for s in sents:
                f.write(s + '\n')
        f.close()


    def updateWeight(self, sent, weight):

        sent = sent.replace('[', '')
        sent = sent.replace(']', '')
        ws = self.weightedSentences
        
        for i in range(len(ws)):
            tmp = ws[i]
            tmp = tmp.replace('[', '')
            tmp = tmp.replace(']', '')
            tmp = tmp.split(';')
            if tmp[0] == sent:
                newWS = '[' + tmp[0] + '];' + str(weight)
                ws[i] = newWS
                
        self.weightedSentences = ws


    def incrementWeight(self, sent):
        sent = sent.replace('[', '')
        sent = sent.replace(']', '')
        ws = self.weightedSentences
        
        for i in range(len(ws)):
            tmp = ws[i]
            tmp = tmp.replace('[', '')
            tmp = tmp.replace(']', '')
            tmp = tmp.split(';')
            if tmp[0] == sent:
                weight = eval(tmp[1]) + 1
                newWS = '[' + tmp[0] + '];' + str(weight)
                ws[i] = newWS
                
        self.weightedSentences = ws



    def __str__(self):
        return self.weightedSentences



if __name__ == "__main__":

    hFile = 'history.txt'
    
    history = History.load_history(hFile)

    for s in history.weightedSentences:
        print(s)
        print(type(s))

    newSent = "['see', 'Bob', 'run', 'fast']"
    newWeight = 5
    history.add(newSent + ';' + str(newWeight))

    print('-' * 5)

    for s in history.weightedSentences:
        print(s)
    
    history.save_history(hFile, history.weightedSentences)

    print('-' * 5)

    history.updateWeight("['see', 'Bob', 'run']", 3)

    for s in history.weightedSentences:
        print(s)

    print('-' * 5)

    history.incrementWeight("['see', 'Bob']")

    for s in history.weightedSentences:
        print(s)    

    history.save_history(hFile, history.weightedSentences)

    print("ok")
