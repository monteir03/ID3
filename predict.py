def _index_of(atributo,atri_list):  #retorna o indice correspondente a um atributo na matriz 
    indice = 0
    while indice < len(atri_list) and atri_list[indice] != atributo:
        indice += 1
    return indice

def predict_example(example,node,atri_list):
    if node.is_leaf():
        return node.get_classification()        #se for folha retorna logo, senão:
    
    attribute = node.get_attribute()            #guarda o atributo do nó em que o exemplo se encontra

    indice = _index_of(attribute,atri_list)
    value = example[indice]                     #guarda o valor para o atributo do exemplo em questão
    
    if value not in node.get_branches():        #se esse valor não tem ramificação, 
        return None                             #então não existe classificação, senão:
        
    subtree = node.get_branches()[value]        #desce para o nó descendente do ramo com valor value(dict de chave value que guarda o nó)
    return predict_example(example,subtree,atri_list)    #recursivamente descea a arvore até retornar classificação ou None

def predict_all(test_set,decision_tree,atri_list):       #aplicar a todos os exemplos e retornar uma lista
    predictions = []

    for example in test_set[1:]:                                        #cuidado porqeu aqui começo em 1
        prediction = predict_example(example, decision_tree,atri_list)
        predictions.append(prediction)
    return predictions

def accuracy(y_predict,y_real):
    total=len(y_predict)
    well_classificated=0

    for i in range(total):
        if y_predict[i]==y_real[i]:
            well_classificated+=1
    
    acc = well_classificated/total
    return acc
