class TestFrame:

    def __init__(self,dt,atributos,dicionario):  #tenho os atributos e a lista dos split points
        self.dt = dt
        self.atributos = atributos
        self.dicionario = dicionario
    
        
    def _continuo_to_discreto(self,valor,split_list): #apenas para um exemplo
        tamanho=len(split_list)

        if valor<=split_list[0]:
            return "]-inf,"+str(split_list[0])+"]"

        for i in range(1,tamanho):
            if valor<=split_list[i]:
                return  "]"+str(split_list[i-1])+","+str(split_list[i])+"]"
        
        return "["+str(split_list[tamanho-1])+",+inf["
    
    def _discretize_attribute(self, atributo, split_list):#discretiza um um atributo
        index = self._index_of(atributo)
        for linha in self.dt[1:]:
            valor=linha[index]
            linha[index] = self._continuo_to_discreto(valor,split_list)
    
    def _discretize(self):   #final
        atributos=self.atributos
        for atributo in atributos:
            split_list=self.dicionario[atributo]
            self._discretize_attribute(atributo,split_list)

    def _index_of(self,atributo):                #retorna o indice correspondente a um atributo na matriz 
        indice=0
        while self.dt[0][indice]!=atributo:
            indice+=1
        return indice
    
    def get_frame(self):
        return self.dt