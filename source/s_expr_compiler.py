#-*-coding: utf-8-*-
"""
Этот модуль - компилятор s-выражений выражений,
symbolic-expression просто говоря 2 скобки с данными,
данные это атомы т е числа и строки.
Числа на этапе разделения на лексемы приводятся к типу float,
я решил,что виртуальная машина будет оперировать контейнером с
float.Строки из букв в исходном тексте становятся литералами
строк Python.Интерприттируются такие выражения так,первая
строка идет как название функции,в ветках if-elif определяется
что делать с такой функцией.Параметры ее -другие s-выражения могут
передаваться рекурсивно компилятору,формируя байт-код для виртуальной машины.


"""
import libTestPydModuleFloat as vt
from struct import pack,unpack
(   NOOP    ,
    IADD    ,  
    ISUB    ,
    IMUL    ,
    IDIV    ,
    IREM    ,
    IPOW    ,
    ILT     ,  
    IEQ     ,   
    BR      ,   
    BRT     ,   
    BRF     ,   
    ICONST  ,   
    LOAD    ,  
    GLOAD   ,  
    STORE   ,  
    GSTORE  ,  
    PRINT   ,  
    POP     ,  
    CALL    ,  
    RET     ,  
    STORE_RESULT,
    LOAD_RESULT,
    HALT    
)=range(24)
    

#import pdb
#pdb.set_trace()
import sys
import re
isa = isinstance
Symbol = str
def load_file(fName):
    """
    Считывает файл -исходнй текст проги,возвращает строку-выражение
    """ 
    fContent=open(fName).read()
    return fContent
def op_prior(str_char_op):
    """
    Приоритет арифметической операции
    """
    if str_char_op=="^":
        return 6
    elif str_char_op=="*":
        return 5
    elif str_char_op=="/":
        return 5
    elif str_char_op=="%":
        return 3
    elif str_char_op=="+":
        return 2
    elif str_char_op=="-":
        return 2 
def isOp(c):
    """
    Это арифметическая операция? 
    """ 
    if c=="-" or c=="+" or c=="*" or c=="/" or c=="%"or c=="^" :return True
    return False
def opn(str_code): 
    """
    Перевод в обратную польскую запись str_code-строка инфиксного выражения Ret список
    """
    int_ptr=0
    listKstrK_OpStack=[]
    listKintOrStr_resOpnZapis=[]
    while (int_ptr<len(str_code)): 
        v=str_code[int_ptr]
        int_ptr+=1
        if isa(v,float):
            listKintOrStr_resOpnZapis.append(v)
        elif re.match("[A-Za-z]+",str(v)): 
            listKintOrStr_resOpnZapis.append(v)            
        elif isOp(v):
                while(len(listKstrK_OpStack)>0 and 
                listKstrK_OpStack[-1]!="[" and 
                op_prior(v)<=op_prior(listKstrK_OpStack[-1]) ):
                    listKintOrStr_resOpnZapis.append(listKstrK_OpStack.pop())
                 
                listKstrK_OpStack.append(v)       
        elif v==']':
            while len(listKstrK_OpStack)>0:
                x=listKstrK_OpStack.pop()
                if x=='[':
                    break
                listKintOrStr_resOpnZapis.append(x)
        elif v=="[":
            listKstrK_OpStack.append(v)                                                          
    while len(listKstrK_OpStack)>0 :
           listKintOrStr_resOpnZapis.append(listKstrK_OpStack.pop())
    return listKintOrStr_resOpnZapis 
def floatToBytes_SfloatRbytes(float_val):
    """
    запаковать число как набор байт
    """
    return pack('>f',float_val)
class LispMach:
 """
 Компилятор
 """
 def __init__(self):
  """
  заводим карту для функций- <имя функции:индекс ее байткода>,индекс первой команды,которую нужно исполнять 
  """   
  self.pole_dictKstrYintK_funcTable={}
  self.pole_vectorKintK_b_c=[]
  self.pole_int_startIp=0
  self.pole_int_nargs=0
 def method_genB_C_IrV(self,int_command):
     """"
     генерация байткода-int_command-опкод который нужно добавить для результирующего списка,для Vm
     """
     self.pole_vectorKintK_b_c.append(int_command)
 def method_recurs_evalPerList_LrV(self,vectorKintOrStrK):
    """
    рекурсивный разбор s-выражения vectorKintOrStrK -список с числами и строками 
    как именами того какой байт-код генерировать
    смотря на аргумент self.method_genB_C_IrV можно понять синтаксис языка 
    """
    #print(vectorKintOrStrK)
    
    if not isa(vectorKintOrStrK, list):
        self.method_genB_C_IrV(ICONST)
        self.method_genB_C_IrV(vectorKintOrStrK) 
    elif vectorKintOrStrK[0] == '//':#комментарии
        pass
    elif vectorKintOrStrK[0] == 'set!':  #переменная         
        (_, var, exp) = vectorKintOrStrK
        self.method_recurs_evalPerList_LrV(exp)
        self.method_genB_C_IrV(STORE)
        int_ordLocToStore=ord(var)-ord("a")
        self.method_genB_C_IrV(int_ordLocToStore)
    elif vectorKintOrStrK[0] == 'setResult!': #значение от функции          
        (_, var) = vectorKintOrStrK
        self.method_genB_C_IrV(STORE_RESULT)
        int_ordLocToStoreRegistr=ord(var)-ord("a")
        self.method_genB_C_IrV(int_ordLocToStoreRegistr)                
    elif vectorKintOrStrK[0] == 'defun':   #определить функцию-заносим в карту имя функции и ее позицию в байт коде
                                           #запоминаем индекс байт-кода функции main      
        (_,str_nameFunc, list_arg,list_expr) = vectorKintOrStrK
        if str_nameFunc=='main':
            self.pole_int_startIp=len(self.pole_vectorKintK_b_c)
        else:  
            self.pole_dictKstrYintK_funcTable[str_nameFunc]=len(self.pole_vectorKintK_b_c)
        self.method_recurs_evalPerList_LrV(list_arg)    
        self.method_recurs_evalPerList_LrV(list_expr)
        
           
    elif vectorKintOrStrK[0] == '$': #выполняем s-выражений слева направо       
        for exp in vectorKintOrStrK[1:]:
            val = self.method_recurs_evalPerList_LrV(exp)
        return val
    elif vectorKintOrStrK[0]=='return': #выход из функции
        self.method_genB_C_IrV(RET)       
        
    elif vectorKintOrStrK[0] == 'arif': #выполняем арифметическое выражение
        listKintOrStr_resOpnZapis=opn(vectorKintOrStrK[1:])
        for i in listKintOrStr_resOpnZapis:
            if isOp(i):
                if i=="+": 
                    self.method_genB_C_IrV(IADD)
                if i=="-":
                    self.method_genB_C_IrV(ISUB)
                if i=="*":
                    self.method_genB_C_IrV(IMUL)
                if i=="/": 
                    self.method_genB_C_IrV(IDIV)  
                if i=="%":
                    self.method_genB_C_IrV(IREM)
                if i=="^": 
                    self.method_genB_C_IrV(IPOW)     
            elif re.match("[A-Za-z]+",str(i)):
                if str(i)!='z':
                  self.method_genB_C_IrV(LOAD)
                  self.method_genB_C_IrV(ord(i)-ord("a"))
                else:
                    self.method_genB_C_IrV(LOAD_RESULT)
            elif isa(i,float):
                self.method_genB_C_IrV(ICONST)
                for i1 in floatToBytes_SfloatRbytes(i):
                    self.method_genB_C_IrV(i1)
    elif vectorKintOrStrK[0] == 'print': #печатаем локальную переменную
        for str_temp_BukvaKakChislo in vectorKintOrStrK[1:]:  
          self.method_genB_C_IrV(PRINT)
          self.method_genB_C_IrV(ord(str_temp_BukvaKakChislo)-ord('a'))
    elif vectorKintOrStrK[0] == 'call': #вызываем функцию
        (_,str_nameFunctionToCallFromMainFunction,list_args)=vectorKintOrStrK
        int_nameFunctionToCallFromMainFunction=self.pole_dictKstrYintK_funcTable[str_nameFunctionToCallFromMainFunction]
        print(int_nameFunctionToCallFromMainFunction)
        self.method_recurs_evalPerList_LrV(list_args)
        self.method_genB_C_IrV(CALL)
        self.method_genB_C_IrV(int_nameFunctionToCallFromMainFunction)
        self.method_genB_C_IrV(self.pole_int_nargs)
    elif vectorKintOrStrK[0]=='<': #сравнение на меньше
        (_,list_arif1,list_arif2)=vectorKintOrStrK
        self.method_recurs_evalPerList_LrV(list_arif1)
        self.method_recurs_evalPerList_LrV(list_arif2)
        self.method_genB_C_IrV(ILT)
    elif vectorKintOrStrK[0]=='=':#сравнение на равенство
        (_,list_arif1,list_arif2)=vectorKintOrStrK
        self.method_recurs_evalPerList_LrV(list_arif1)
        self.method_recurs_evalPerList_LrV(list_arif2)
        self.method_genB_C_IrV(IEQ)        
    elif vectorKintOrStrK[0]=='if':#if
        (_,list_test,list_trueEpr,list_falseExpr)=vectorKintOrStrK
        self.method_recurs_evalPerList_LrV(list_test)
        self.method_genB_C_IrV(BRF)
        int_addr1=len(self.pole_vectorKintK_b_c)
        self.method_genB_C_IrV(0)
        self.method_recurs_evalPerList_LrV(list_trueEpr)
        self.method_genB_C_IrV(BR)
        int_adr2=len(self.pole_vectorKintK_b_c)
        self.method_genB_C_IrV(0)
        self.pole_vectorKintK_b_c[int_addr1]=len(self.pole_vectorKintK_b_c)
        self.method_recurs_evalPerList_LrV(list_falseExpr)
        self.pole_vectorKintK_b_c[int_adr2]=len(self.pole_vectorKintK_b_c)
    elif vectorKintOrStrK[0]=='while':#while
        (_,list_test,list_whileBody)=vectorKintOrStrK
        int_addr1=len(self.pole_vectorKintK_b_c)
        self.method_recurs_evalPerList_LrV(list_test)
        self.method_genB_C_IrV(BRF)
        int_addr2=len(self.pole_vectorKintK_b_c)
        self.method_genB_C_IrV(0)
        self.method_recurs_evalPerList_LrV(list_whileBody)
        self.method_genB_C_IrV(BR)
        self.method_genB_C_IrV(int_addr1)
        self.pole_vectorKintK_b_c[int_addr2]=len(self.pole_vectorKintK_b_c)
        
    elif vectorKintOrStrK[0] == 'params':#формальные параметры
        j=0
        for i in vectorKintOrStrK[1:]:
            self.method_genB_C_IrV(LOAD)
            self.method_genB_C_IrV(j)
            self.method_genB_C_IrV(STORE)
            self.method_genB_C_IrV(ord(i)-ord('a'))
            j+=1
    elif vectorKintOrStrK[0] == 'args':#фактические параметры
        j=0
        for i in vectorKintOrStrK[1:]:
            if  isa(i,float): 
                self.method_genB_C_IrV(ICONST)
                for i1 in floatToBytes_SfloatRbytes(i):
                    self.method_genB_C_IrV(i1)                
            elif isa(i,str):
                self.method_genB_C_IrV(LOAD)
                self.method_genB_C_IrV(int(ord(i)-ord("a")))
            j+=1
        self.pole_int_nargs=j
    elif vectorKintOrStrK[0]=='pass':#ничего не делать
        self.method_genB_C_IrV(NOOP)
            
   
        
 def method_retB_C_VrL(self):  
    """
    Возвращает результирующий байт код для ВМ 
    """ 
    return self.pole_vectorKintK_b_c
 def __str__(self):
     """
     Возвращает строковое представление обьекта компилятора
     """
     return "func_table:"+str(self.pole_dictKstrYintK_funcTable)+"\nvectorKintOrStrK:"+\
      "\nvector<int>_b_c:"+str(self.pole_vectorKintK_b_c)+"\nstart_ip:"+str(self.pole_int_startIp)    
     
        
def read(s):
    #"Read  expression from a string."
    """
    Читает lisp подобное выражение из строки и лексемазирует его 
    """ 
    return read_from(tokenize(s))
 
def tokenize(s):
    """
     Ковертирует строку в питон список токенов
    """
    #"Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()
 
def read_from(tokens):
    """
    Читает выражение,создает 'атомы' -float или строки
    """
    #"Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)
 
def atom(token):
    """
    Числа становятся числами float,остальное символами,строками 
    """
    #"Numbers become numbers; every other token is a symbol."
    try: return float(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)
 

 
  
parse=read        


str_fileName="./code_Arifm.lisp"
obj_fileDescr=open(str_fileName,"r")
obj_LispMach=LispMach()
str_textProgram=obj_fileDescr.read()
print(str_textProgram)
obj_LispMach.method_recurs_evalPerList_LrV(parse(str_textProgram))
vectorKintK_opCode=obj_LispMach.method_retB_C_VrL()
vectorKintK_opCode.append(HALT)
print(obj_LispMach)

float_retVal=vt.eval(vectorKintK_opCode,obj_LispMach.pole_int_startIp,0) 
print(float_retVal)
