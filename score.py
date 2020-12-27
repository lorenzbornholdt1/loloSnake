import json
import os.path

MAX_SCORE_LEN = 5000
class ScoreWriter(object):


    def readWriteScore(self, newScore):
       
        data = {}
        data['scores'] = []       

        if os.path.isfile('score.json'):
            try:
                with open('score.json') as json_file:
                    data = json.load(json_file)
            except:
                dummy = 0
        if len(data['scores'])>MAX_SCORE_LEN:
            data['scores'] = []   
        data['scores'].append(newScore)
        with open('score.json', 'w') as outfile:
            json.dump(data, outfile)
        return max(data['scores'])




