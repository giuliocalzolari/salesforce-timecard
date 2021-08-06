class HoursCounter(object):
   def __init__(self, rs):
      self.data = {"Name": "Total"}
      self.card = {}
      self.report = []
      self.sum = 0
      self.card_sum = 0
      self.clean_data(rs)

   def add(self, _k ,v):
      k = replace_all(_k, {"pse__": "", "_Hours__c": "", "__c": ""})
      if "_Hours__c" in _k:
         if k not in self.data.keys():
            self.data[k] = 0
         self.data[k] += int(v)
         self.sum += int(v)
         self.card_sum += int(v)
      self.card[k] = v

   def summary(self):
      self.data["SUM"] = self.sum
      self.report.append(self.data)

   def project_sum(self):
      self.card["SUM"] = self.card_sum
      self.report.append(self.card)
      self.card = {}
      self.card_sum = 0


   def clean_data(self, rs):
      for r in rs:
         r.pop("Id", None)
         r.pop("pse__Project__c", None)
         r.pop("pse__Assignment__c", None)

         for k,v in r.items():
            self.add(k, v)
         self.project_sum()
      self.summary()




def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text
