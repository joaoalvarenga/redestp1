# Simulador da Redes
## Code-style  
Nome para funções e variáveis:  
nome_da_funcao  
nome_da_variavel  
Nome para classes(CamelCase):  
NomeDaClasse

## Design Pattern
Não use "else", "elif", evite ao máximo usar, use funções para isso.  
Exemplo:
Com else
```
a = raw_input()
b = raw_input()
if b == 0:
    print("Não é possível dividir por zero")
else:
    print("O resultado da divisão {}/{}={}".format(a,b,a/float(b)))
```
Sem else
```
a = raw_input()
b = raw_input()

def divisao(a,b):
    if b == 0:
        print("Não é possível dividir por zero")
        return
    print("O resultado da divisão {}/{}={}".format(a,b,a/float(b)))
```