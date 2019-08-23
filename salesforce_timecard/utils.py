


def clean_data(rs):
   clean_data = []
   for r in rs:
      r.pop("pse__Project__c", None)
      r.pop("pse__Assignment__c", None)
      t = {}
      for k,v in r.items():
         new_k = k.replace("pse__", "").replace("__c", "")
         t[new_k] = v
      clean_data.append(t)
   return clean_data