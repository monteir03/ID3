import math

class DataFrame:

    def __init__(self, dt):
        #propriedades importantes
        self.dt = dt                            #matriz que representa o dataset
        self.rows = len(dt)                     #numero TOTAL de linhas 
        self.cols = len(dt[0])                  #numero TOTAL de colunas 
        #facilidades
        self.attributes = dt[0]                 #lista de atributos
        self.label = dt[0][self.cols-1]         #nome da target label
        self.size = len(dt)-1

    def index_of(self,atributo):                #retorna o indice correspondente a um atributo na matriz 
        indice=0
        while self.dt[0][indice]!=atributo:
            indice+=1
        return indice

    def values_of(self,atributo):               #valores que um atributo pode ter
        i = self.index_of(atributo)
        lista=[]
        for j in range(1,len(self.dt)):
            if self.dt[j][i] not in lista:
                lista.append(self.dt[j][i])
        return lista

    def label_values(self):                     #valores que a target label tem
        lista = self.values_of(self.label)
        return lista
    
    def all_same(self):                         #True se todos os exemplos teem a mesma classe(se é folha)
        aux = self.label_values()
        if len(aux)==1:
            return True
        return False
    
    def get_if_all_same(self):                  #para usar em ID3.py
        return self.dt[1][self.cols-1]

    def most_important(self,attribute_list):    #retorna o atributo mais importante de acordo com a Gain
        max_gain = -100000000
        best_attribute = None

        for attribute in attribute_list:
            gain = self.Gain(attribute)
            if gain > max_gain:
                max_gain = gain
                best_attribute = attribute

        return best_attribute    

    #if there´s no more expansion
    def plurality_value(self):
        dic={}
        i_label = self.index_of(self.label)       #indice da coluna da label
        lista = self.values_of(self.label)        #lista dos valores da abel

        for value in lista:                     #cria um dicionario com os vaores da label como chaves.
            dic[value]=0

        for i in range(1,self.rows):               #percorre o dataset apenas 1 VEZ
            v = self.dt[i][i_label]
            if v in dic.keys():
                dic[v] += 1                      #atualiza o dicionario 

        major_val=max(dic,key=dic.get)        #retorna a chave com maior frequencia
        return major_val

    def sub_data_frame(self,attribute,value):
        new_data = [self.dt[0]]         #linha com titulos
        for i in range(1, self.rows):
            if self.dt[i][self.index_of(attribute)] == value:
                new_data.append(self.dt[i])
        dt = DataFrame(new_data)
        return dt
    
    def get_attributes(self):  #removemos a Label e o ID
        return self.attributes[1:-1]
    
# Gain Remainder e H_label são funções que servirão para decidir o atributo que maior ganho(ou seja, apenas trabalha com atributos)
    def H_label(self):                         #this is the entropy of the label for the all dataset 
        i_label = self.index_of(self.label)  
        v_label = self.values_of(self.label)    #lista com os valores unicos que label toma
        total_instances = self.rows-1           #vai ser usado para dividir pelo total  #cuidado rows not cols
        entropy = 0
        for value in v_label:
            v_count = 0
            for line in self.dt[1:]:
                if line[i_label] == value:
                    v_count += 1
            probability = v_count/total_instances
            entropy -= probability * math.log2(probability)  #porque log2(x) é negativo para x<1
        return entropy 

    def Remainder(self,attribute):                      #função que retorna entropia depois de attribute selecionado ser testado
        
        remainder = 0
        lines = self.rows-1
        attribute_index = self.index_of(attribute)      #coluna do atributo
        label_index = self.index_of(self.label)         #coluna da label
        attribute_values = self.values_of(attribute)    #valores unicos que o atributo toma
        label_values = self.attributes                  #valores unicos que a label toma

        for v in attribute_values:                      #para cada valor do atributo faz:
            value_count = 0                             #para contar a frequencia com que um valor surge no dataset
            value_probabilities = []                    #guarda a frequencia de "p" e "n" da label separadamente para o valor de atributo em questão

            for l_v in label_values:
                label_value_count = 0                   

                for row in self.dt[1:]:                     
                    if row[attribute_index] == v and row[label_index] == l_v:   
                        label_value_count += 1                                         

                value_count += label_value_count                #frquencia do valor do atributo ("p"+"n")
                value_probabilities.append(label_value_count)   #frequencia de "p" e "n" separadamente para um valor do atributo

            if value_count != 0:                                #evita calculos desnecessarios
                value_probabilities = [c / value_count for c in value_probabilities]    #probabilidades para cada "p" e "n" deoendendo do valor-> Ap/Ap+An, An/Ap+An  
                entropy_value = sum([-p * math.log2(p) for p in value_probabilities])           #aplica a fórmula
                remainder += (value_count / lines) * entropy_value                              #faz o mesmo para cada valor e soma ao remainder e multiplica pela probablidade do valor
        return remainder

    def Gain(self,attribute):
        return self.H_label()-self.Remainder(attribute)  
    

    #Discretização
    #iremos calcular a information Gain para cada splitting point e escolher os len(class)-1 melhores

    def best_split_points_of(self,attribute):  
        split_points_number=len(self.values_of(self.label))-1 
        i_attribute = self.index_of(attribute)
        i_label = self.cols-1
        lista = [(linha[i_attribute],linha[i_label]) for linha in self.dt[1:]]  #guardar valor-label em lista
        lista_ordenada = sorted(lista, key=lambda x: x[0])                      #ordenar lista pelo valor do atributo
        
        split_points = []               #percorrer a lista até encontrar os split points
    
        for i in range(1, len(lista_ordenada)):
            if lista_ordenada[i][1] != lista_ordenada[i - 1][1]:  # verificar se a label é diferente entre elementos consecutivos
                split_value = round((lista_ordenada[i][0] + lista_ordenada[i - 1][0]) / 2, 1)  # calcular o ponto de divisão como a média entre os valores
                split_points.append(split_value)  # adicionar o ponto de divisão à lista de splitting points
        
        _split_points=list(set(split_points))  #remover split points repetidos(IMPORTANTE porque vamos escolher os melhores n points de uma lista ordenada)
        _split_points.sort()  #lista com splits points ordenada
        #até aqui já temos os slplit points...
        best_split_points=[]        #lista de tuplos com point e gain correspondente, vai ser ordenada do maior para menor de acordo com gain, e escolheremos os n-1 melhores, e essa será a nossa divisão
        for point in _split_points:
            gain = self.split_gain(i_attribute, point)  # calcular o ganho de informação para o ponto de divisão
            best_split_points.append((point, gain))
        
        best_split_points = sorted(best_split_points, key=lambda x: x[1])
        best_split_points = best_split_points[-split_points_number:]
        best_points = [point for point, gain in best_split_points]

        return best_points #lista de splits
     
    def split_gain(self, index_attribute, split_point):  #inidice do atributo e o valor do ponto
        # Obtém os índices das colunas do atributo e da label
        i_attribute = index_attribute
        i_label = self.cols - 1

        #dicionario que chave é o valor da target class, e o valor da chave é a frequancia da target class
        counts_before = {}
        counts_after = {}
        for row in self.dt[1:]:
            value = row[i_attribute]      #valor do exemplo no atributo 
            label = row[i_label]          #valor da target label para o exemplo

            if value <= split_point:
                counts_before[label] = counts_before.get(label, 0) + 1   #se a chave ainda não estiver no dcit o valor padrao é 0
            else:
                counts_after[label] = counts_after.get(label, 0) + 1

        # Entropia antes/cima e depois/baixo do ponto de divisão
        entropy_before = self.splits_entropy(counts_before)
        entropy_after = self.splits_entropy(counts_after)
        # Peso(numero de exemplos before e exemplos after) em relação ao total
        weight_before = sum(counts_before.values()) / (sum(counts_before.values()) + sum(counts_after.values()))
        weight_after = sum(counts_after.values()) / (sum(counts_before.values()) + sum(counts_after.values()))
       
        
        information_gain = self.H_label() - (weight_before * entropy_before + weight_after * entropy_after)
        return information_gain

    def splits_entropy(self,counts):  #recebe um dicionario
        total = sum(counts.values())
        entropy = 0

        for count in counts.values():
            probability = count / total
            if probability != 0:  #log(0)
                entropy -= probability * math.log2(probability)

        return entropy
    
    def six_plus_attributes(self): #atributos que têm mais do que 6 diferentes float/int
        six_plus = []
        for atr in self.attributes[1:]:  
            if (len(self.values_of(atr))>6): 
                six_plus.append(atr)
        return six_plus
    
    def continuo_to_discreto(self,valor,split_list): #apenas para um exemplo
        tamanho=len(split_list)

        if valor<=split_list[0]:
            return "]-inf,"+str(split_list[0])+"]"

        for i in range(1,tamanho):
            if valor<=split_list[i]:
                return  "]"+str(split_list[i-1])+","+str(split_list[i])+"]"
        
        return "["+str(split_list[tamanho-1])+",+inf["
                
    def discretize_attribute(self, atributo, split_list):#discretiza um atributo
        index = self.index_of(atributo)
        for linha in self.dt[1:]:
            valor=linha[index]
            linha[index] = self.continuo_to_discreto(valor,split_list)
    
    def discretize(self): 
        atributos=self.six_plus_attributes()
        for atributo in atributos:
            split_list=self.best_split_points_of(atributo)
            self.discretize_attribute(atributo,split_list)