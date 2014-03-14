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
      flag ='attr'

    v.replace(edit, sel, text)
    return flag

  def run(self, edit):
    v = self.view
    if v.sel()[0].size() == 0:
        v.run_command("expand_selection", {"to": "word"})

    flag = 'init'
    rescue = 'init'

    ori_start = v.sel()[0].begin()
    ori_end = v.sel()[0].end()

    for sel in v.sel():

        cur_begin = sel.begin()
        cur_end = sel.end()

        text = v.substr(sel)
        res = self.matcher(text)
        tmp = sel
        if not res:
          #first check one character to the left to see if its a attr
          sel = Region(cur_begin - 1, cur_end)
          text = v.substr(sel)
          res = self.matcher(text)
          if not res:
            #now expand selection one character to the right to see if its a string
            sel = Region(cur_begin - 2, cur_end + 2)
            text = v.substr(sel)
            res = self.matcher(text)
            if not res:
              #this is a mute point
              continue

        this_flag = self.replacer(v, edit, sel, text, res)

        if flag=='init':
          flag = this_flag

        if flag!=this_flag:
          rescue = 'rescue'

    if rescue == 'rescue':
      v.sel().clear()
    elif flag=='key':
      v.sel().clear()
      v.sel().add(Region(ori_start + 1, ori_end + 1 ))
    elif flag=='attr':
      v.sel().clear()
      v.sel().add(Region(ori_start - 1, ori_end - 1 ))
    else :
      # nothing

# ['abc']
# ["abc"]
# .abc

