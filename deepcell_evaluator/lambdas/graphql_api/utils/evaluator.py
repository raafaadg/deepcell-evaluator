class Evaluator():
    def __init__(self, sub:str, string:str):
        self.sub=sub
        self.string=string
        self.conditions = []
        self.message = ''
        self.result = None
        self.evaluate()
        
    def evaluate(self):
        
        self.fetch_conditions()
        
        if not self.conditions:      
            self.sub = self.sub.lower()  
            self.string = self.string.lower()  
            self.result = self.sub
            for a in range(len(self.sub)):
                aux = self.sub[0:a+1]
                if len(self.sub.replace(aux,'')) == 0 and len(aux) < len(self.result):
                    self.result = aux
                         
            self.message = f'The smallest subset of substring {self.sub} is {self.result} with length {len(self.result)}'
            self.result = len(self.result)
    
    def fetch_conditions(self):
        rules = [
            {
                'function' : lambda sub, string: (sub == '') or (string == ''),
                'condition': 'Both parameters can not be empty.'
            },
            {
                'function' : lambda sub, string: not isinstance(sub, str) and not isinstance(string, str),
                'condition': 'Both parameters must be string.'
            },
            {
                'function' : lambda sub, string: not (len(string)/len(sub)).is_integer() if ((sub != '') or (string != '')) else True,
                'condition': 'The division of lengths from sub and string must be integer'
            },
            {
                'function' : lambda sub, string: len(string.replace(sub, '')) > 0,
                'condition': 'Provided String is not a unique sequence of provided Sub string'
            }
        ]
        for rule in rules:
            try:
                if rule['function'](self.sub, self.string):
                    self.conditions.append(rule['condition'])
            except:
                self.conditions.append(rule['condition'])
                
        if self.conditions:
            self.result = -len(str(self.string))
                
                    
    def get_evaluation(self):
        return self.result, self.conditions
    
    def to_json(self):
        return {
            'result': self.result,
            "conditions": self.conditions,
            "message": self.message
        }