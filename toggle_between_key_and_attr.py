import sublime_plugin
import re
import string
from sublime import Region

re_key = re.compile("^\[(['\"])(.*)\\1\]$")
re_attr = re.compile("^(\.)(.*)$")

class ToggleBetweenKeyAndAttr(sublime_plugin.TextCommand):

  def matcher(self,text):
    res = re_key.match(text)
    if not res:
      res = re_attr.match(text)
    return res

  def replacer(self, v, edit, sel, text, res):
    old_quotes = res.group(1)
    text = res.group(2)

    if old_quotes == '.':
      text = '[\'' + text + '\']'
      flag = 'key'
    else :
      text = '.' + text
      flag = 'attr'

    v.replace(edit, sel, text)
    return flag


  def run(self, edit):
    v = self.view
    if v.sel()[0].size() == 0:
        v.run_command("expand_selection", {"to": "word"})

    for sel in v.sel():

        cur_start = sel.begin()
        cur_end = sel.end()

        text = v.substr(sel)
        res = self.matcher(text)
        tmp = sel
        if not res:
          #first check one character to the left to see if its a attr
          sel1 = Region(sel.begin() - 1, sel.end())
          text = v.substr(sel1)
          res = self.matcher(text)
          tmp = sel1
          if not res:
            #now expand selection one character to the right to see if its a string
            sel2 = Region(sel.begin() - 2, sel.end() + 2)
            text = v.substr(sel2)
            res = self.matcher(text)
            tmp = sel2
            if not res:
              #this is a mute point
              continue

        flag = self.replacer(v, edit, tmp, text, res)
        
        sel.clear()
        if flag == 'key':
          sel.add(Region(cur_start+1, cur_end+1))
        else :
          sel.add(Region(cur_start-1, cur_end-1))
# ['abc']
# ["abc"]
# .abc

