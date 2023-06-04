#class node para ser usada na criação da arvore de decisão
from DataFrame import *

class Node:
     
   def __init__(self,examples,attribute=None,classification=None):
      self.examples = examples
      self.attribute = attribute
      self.classification = classification
      self.branches = {}                     #dicionario onde as chaves são os branches e o valor unico da chave é o nó que o branch dá origem

   def add_branch(self, value, subtree):
        self.branches[value] = subtree

   def is_leaf(self):
      return self.classification is not None

   def get_classification(self):
      return self.classification

   def get_attribute(self):
      return self.attribute

   def get_branches(self):
      return self.branches




