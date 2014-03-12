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
    else :
      text = '.' + text

    v.replace(edit, sel, text)


  def run(self, edit):
    v = self.view
    if v.sel()[0].size() == 0:
        v.run_command("expand_selection", {"to": "word"})

    cur_start = v.sel()[0].begin()
    cur_end = v.sel()[0].end()

    for sel in v.sel():
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

        self.replacer(v, edit, tmp, text, res)

    v.sel().clear()
    v.sel().add(Region(cur_start, cur_end))

# ['abc']
# ["abc"]
# ['abc']

