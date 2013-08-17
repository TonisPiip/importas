#!/usr/bin/python
"""

Tonis Piip
13-8-2013

*To be used in conjuction with emacs have option to
 use stdin as input and stdout as output


                    import-as

Discription:
  The is line of code: that imports a module so that its contence
  is added to the local namespace:

       from <module> import *
       from pygame.locals import * #A real line of code that is seen
                                   #in many games/and tutorials  made with pygame

can get ugly fast when used with multiple imports
  It also makes the code harder to read and understand
  when the reader is unfamlure with the modlue.

  The proper way to fix code with this problem would be to replace
  the line with:

       import module as <short-name>
       import pygame.locals.* as <pyg_loc> #possbil
  
  however one these lines of code are changed, the code will not run
  becaues there are many undefined variables.

  Every line of code has to be parsed to prefix any referances to anything in "dir(module)"

"""


import sys
from optparse import OptionParser

def read_stdin():
    return sys.stdin.readlines()
        
def write_stdout(s):
    sys.stdout.write(s)

def commandline_parser():
    
    parser = OptionParser("Import +")
    
    parser.add_option("-r", "--readfile", help = "file to be read",
                        type = str, 
                        nargs = 1,
                        dest = "input",
                        default = None)
    
    parser.add_option("-o", "--output", help = "file to be writen to",
                        type = str,
                        nargs = 1,
                        dest = "output",
                        default = None)
    
    parser.add_option("-s", "--stdinout", help = "use stdin, stdout for input,output",
                        dest = "std",
                        action = "store_true",
                        default = "False")

    parser.add_option("-t", "--test", help = "will run testing function rather then input",
                      action = "store_true",
                      default = False)

                        
    options, extra_args =  parser.parse_args()
    return options



class PythonParser():
    
    def __init__(self,):
        self.source_ittorator = None
        self.write_to_output = None

    def each_line(self):
        if self.source_ittorator is None: raise TypeError()
        for i in self.source_ittorator:
            yield i

    def set_source_ittorator(self, source_ittorator):
        "source_function: ittorator that spits out lines"
        self.source_ittorator = source_ittorator
        
    def set_write_to_output_function(self, func):
        self.write_to_output = func

class Importas(PythonParser):

    def __init__(self,):
        self.repalcements = {}
        PythonParser.__init__(self,)

    def add_replacement(self, target, replacement):
        self.repalcements[target] = replacement

    def run(self):
        
        for line in self.each_line():
            if self.is_import_line(line):
                module_name, short_name = self.parse_import_line(line)
                if short_name is not None:
                    for attr in self.get_import_contence(module_name):
                        self.add_replacement(attr, short_name + "." + attr)
            else:
                line = self.work_line(line)
            self.write_to_output(line)

    def work_line(self, line):
        import re
        pattern = "([^a-zA-Z0-9._])"
        result = []
        for element in re.split(pattern, line):
            for target, replacement in self.repalcements.items():
                if element.startswith(target):
                    element = element.replace(target, replacement)
                    break
            result.append(element)
        return "".join(result)


    def is_import_line(self, line):
        
        if line.strip().startswith("import") or \
           line.strip().startswith("from"):
           return True
        else: 
            return False
    
    def parse_import_line(self,line):
        """possible formats for an import statment:

        import foo
        import foo as bar
        from foo import bar, baz
        from foo import *
        import foo.foo as bar
        """
        short_name = self.get_shortname(line)
        import_file = self.get_import_module(line)
        return import_file, short_name

    def get_import_module(self, line):
        l = line.split()
        return l[ l.index("import") + 1].strip(",")
        
    def get_shortname(self, line):
        if "as" not in line:
            return None
        line, short_word = line.split("as")
        if "#" in short_word:
            short_word = short_word.split("#")[0]
        short_word = short_word.strip()
        if " " in short_word:
            short_word = short_word.split()[0]            
        return short_word #remove whitespace

    def get_import_contence(self, module_string):
        """ """
        import importlib
        #Don't eval anything that's not just an import statment
        if len(module_string.split()) != 1: raise TypeError("Module string can only be ONE thing") 
        module_string = module_string.strip("*.")
        
        module = importlib.import_module(module_string)
        #mod = eval( "__import__('%s')"%module_string.split('.',1)[0])        
        attr = dir(module)
        return [ a for a in attr if not a.startswith("_")]

    

    

print("-----")

def test():
    f = """import os as OS
path.foo()
os.path.foo()
"""
    print(f)
    i = Importas()
    i.set_source_ittorator([l + "\n" for l in f.split("\n")])
    i.set_write_to_output_function(write_stdout)
    i.run()

if __name__ == "__main__":
    c = commandline_parser()
    if c.test is True:
        test()
    
    i = Importas()
    if c.input is None:
        i.set_source_ittorator(read_stdin())
    else:
        in_file = open(c.input,)
        i.set_source_ittorator(in_file.readlines())
        in_file.close()

    if c.output is None:
        i.set_write_to_output_function(write_stdout)
    else:
        out_file = open(c.output, "w")
        i.set_write_to_output_function(out_file.write)
    print("parsing file")
    i.run()
    if c.output is not None:
        out_file.close()
    
