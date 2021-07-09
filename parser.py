from html.parser import HTMLParser

packets = []

class MyParser(HTMLParser):
  def init(self):
    self.packages = []
    self.package = {'name': None, 'version': None, 'description': None } 
    self.in_a = False
    self.in_name = False 
    self.in_version = False 
    self.in_description = False
  def reset(self):
    HTMLParser.reset(self)

  def handle_starttag(self, tag, attr):
    if tag == 'a' and find_val(attr, 'package-snippet'):
      self.in_a = True
      print('yes')
    elif tag == 'span' and find_val(attr, 'package-snippet__name'):
      self.in_name = True
    elif tag == 'span' and find_val(attr, 'package-snippet__version'):
      self.in_version = True
    elif tag == 'p' and find_val(attr, 'package-snippet__description'):
      self.in_description = True
  def handle_endtag(self, tag):

    if self.in_a and tag == 'a':
      self.in_a = False
      self.packages.append(self.package)
      self.package = {'name': None, 'version': None, 'description': None }

    if self.in_a and self.in_name and tag == 'span':
      self.in_name = False

    if self.in_a and self.in_version and tag == 'span':
      self.in_version = False

    if self.in_a and self.in_description and tag == 'p':
      self.in_description = False

  def handle_data(self, data):
    if self.in_a and self.in_name:
        self.package['name'] = data

    if self.in_a and self.in_version:
      self.package['version'] = data
 
    if self.in_a and self.in_description:
      self.package['description'] = data
p = MyParser()
p.init()
p.reset()
def find_val(l, val):
  for v in l:
    if v[1] == val:
      return True
  return False
with open('./res.html') as f:
  for line in f.readlines():
    p.feed(line)
    p.reset()

p.feed('<a class="package-snippet"><span class="package-snippet__name">buddy</span><span class="package-snippet__version">yoyo</span></a>')

strings = []
for package in p.packages:
  left = f"{package['name']} ({package['version']})"  
  right =  f"{package['description']}"
  strings.append([left,right])
longest = 0
for left,right in strings:
    if len(left) > longest:
      longest = len(left)

for (left, right) in strings:
  print(left.ljust(longest + 5, ' ') + right)

