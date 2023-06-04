import sys
from id3 import *
from Node import *
from DataFrame import *
from predict import *
from TestFrame import *


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
   
def read_csv(file):         #ler csv e passar strings que representam números para numeros
    dataset = []
    with open(file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            row = line.strip().split(',')
            converted_row = []
            for value in row:
                try:
                    converted_value = float(value)
                    converted_row.append(converted_value)
                except ValueError:
                    converted_row.append(value)
            dataset.append(converted_row)
    return dataset

def main():
    #PARTE 1: Árvore
        #treino print da arvore
    file1 = sys.argv[1]                 #ficheiro
    train_set = read_csv(file1)         #matriz
    df1 = DataFrame(train_set)          #DataFrame
    attributes = df1.get_attributes()   #list atributos
    
    #informação para discretizar test_set
    atributos_a_discretizar=df1.six_plus_attributes()
    atributo_splits={}  # atributo: splits point list
    for a in atributos_a_discretizar:
        atributo_splits[a]=df1.best_split_points_of(a)
    

    print()
    print("———————————————————————")
    print("ID3 Tree Visualization:")
    print("———————————————————————")
    print()
    df1.discretize()
    root=learn_decision_tree(df1,attributes,df1)
    print_tree(root,indent="                 ")

    #PARTE 2:  se houver um 2º ficheiro;
        #remover label de f.csv 
        #guardar real classification em lista;
        #prever com teste e comparar Predict com True_values
    if(len(sys.argv)>2):

        file2 = sys.argv[2]                                     #ficheiro
        _pre_test_set = read_csv(file2)                          #matriz
        test_frame = TestFrame(_pre_test_set, atributos_a_discretizar, atributo_splits)
        print()
        print("ATENÇÃO: Estamos a considerar que o ficheiro para o teste vêm sem class/label ")
        print("será retornada lista com a mesma ordem do input com as respetivas classificõe ")
        print()

        test_frame._discretize()
        test_set = test_frame.get_frame()


        #y_real=[row[-1] for row in pre_test_set]                #list ultima coluna__
        #y_real=y_real[1:]                                       #remover nome da label
     
        #test_set=[row[:-1] for row in pre_test_set]             #remover ultima coluna
        test_att=test_set[0]                                    #lista dos atributos
                                                                #a linha dos nomes do atributo é removida na função predict_all
    
        y_pred=predict_all(test_set,root,test_att)              #list previsões pela mesma ordem da coluna
        print()
        print("———————————————————————")
        print("Previsões:")
        #print("Evaluation of the model:")
        print("———————————————————————")
        #print("Y_REAL: ",y_real)
        #print()
        print("Y_PRED: ",y_pred)
        print()
        #print("Accuracy_: ", accuracy(y_pred,y_real))       
        #print()


main()