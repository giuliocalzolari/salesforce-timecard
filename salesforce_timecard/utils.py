def print_table(myDict, colList=None, sep='\uFFFA'):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   sep: row separator. Ex: sep='\n' on Linux. Default: dummy to not split line.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] or '') for col in colList])
   colSize = [max(map(len,(sep.join(col)).split(sep))) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   line = formatStr.replace(' | ','-+-').format(*['-' * i for i in colSize])
   item=myList.pop(0); lineDone=False
   while myList:
      if all(not i for i in item):
         item=myList.pop(0)
         if line and (sep!='\uFFFA' or not lineDone): print(line); lineDone=True
      row = [i.split(sep,1) for i in item]
      print(formatStr.format(*[i[0] for i in row]))
      item = [i[1] if len(i)>1 else '' for i in row]


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