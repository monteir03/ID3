from DataFrame import *
from Node import *

def learn_decision_tree(examples, attributes, parent_examples): #inicializar com data_set completo e lista de atributos
   
    if examples.size == 0:
        return Node(parent_examples, classification=parent_examples.plurality_value())

    elif examples.all_same():
        return Node(examples, classification=examples.get_if_all_same())

    elif len(attributes) == 0:
        return Node(examples, classification=examples.plurality_value())

    best_attribute = examples.most_important(attributes)
    best_attribute_values = examples.values_of(best_attribute)
    tree = Node(examples, attribute=best_attribute)
   
    remaining_attributes = attributes.copy()
    remaining_attributes.remove(best_attribute)

    for value in best_attribute_values:
        relevant_examples = examples.sub_data_frame(best_attribute,value)
        subtree = learn_decision_tree(relevant_examples,remaining_attributes,examples)
        tree.add_branch(value, subtree) #the subtree entre aqui recursivamente ## dict

    return tree
    
def print_tree(node, indent=""):
    if node.is_leaf():
        classification = node.get_classification()
        count = node.examples.size
        print(f"{indent}{classification} ({count})") #f indica uma format string
    else:
        attribute = node.get_attribute()
        branches = node.get_branches()
        print(f"{indent}<{attribute}>")
        for value, subtree in branches.items():
            print(f"{indent}    {value}:")
            print_tree(subtree, indent + "        ")



