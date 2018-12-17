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
    IADD    ,   # int add
    ISUB    ,
    IMUL    ,
    IDIV    ,
    IREM    ,
    IPOW    ,
    ILT     ,   # int less than
    IEQ     ,   # int equal
    BR      ,   # branch
    BRT     ,   # branch if true
    BRF     ,   # branch if true
    ICONST  ,   # push constant integer
    LOAD    ,  # load from local context
    GLOAD   ,  # load from global memory
    STORE   ,  # store in local context
    GSTORE  ,  # store in global memory
    PRINT   ,  # print stack top
    POP     ,  # throw away top of stack
    CALL    ,  # call function at address with nargs,nlocals
    RET     ,  # return value from function
    STORE_RESULT,
    LOAD_RESULT,
    HALT    
)=range(24)
listKstrK_opcodes=[
        ["NOOP",0]    ,
        ["IADD",0]    ,   # int add
        ["ISUB",0]    ,
        ["IMUL",0]    ,
        ["IDIV",0]    ,
        ["IREM",0]    ,
        ["IPOW",0]    ,
        ["ILT",0]     ,   # int less than
        ["IEQ",0]     ,   # int equal
        ["BR",1]      ,   # branch
        ["BRT",1]     ,   # branch if true
        ["BRF",1]     ,   # branch if true
        ["ICONST",1]  ,   # push constant integer
        ["LOAD",1]    ,  # load from local context
        ["GLOAD",1]   ,  # load from global memory
        ["STORE",1]   ,  # store in local context
        ["GSTORE",1]  ,  # store in global memory
        ["PRINT",1]   ,  # print stack top
        ["POP",0]     ,  # throw away top of stack
        ["CALL",2]    ,  # call function at address with nargs,nlocals
        ["RET",0]     ,  # return value from function
        ["STORE_RESULT",1],
        ["LOAD_RESULT",0],
        ["HALT",0]        
] 
def func_vmPrintStack_SvectorKfloatKI(par_vectorKfloatK_stack, par_I_count) :
    print("stack=[");
    for  i in range(0,par_I_count):
        print(" {0}".format(par_vectorKfloatK_stack[i]));
    
    print(" ]\n");

            
def func_vmPrintInstr_SvectorKintKIrV(vectorKintK_opCode, int_ip) :
    int_opcode =vectorKintK_opCode[int_ip];
    listKstrYintK_instr = listKstrK_opcodes[int_opcode];
    int_nargs=listKstrYintK_instr[1]
    if (int_nargs==0) :

            print("%d:  %s\n"%( int_ip,listKstrYintK_instr[0] ));

    elif (int_nargs==1 and int_opcode!=ICONST) :
            print("%d:  %s %f\n" %(int_ip, listKstrYintK_instr[0],vectorKintK_opCode[int_ip+1]) )
    elif (int_nargs==1 and int_opcode==ICONST):
        bytearray_bAr=bytearray([vectorKintK_opCode[int_ip+1],vectorKintK_opCode[int_ip+2],vectorKintK_opCode[int_ip+3],vectorKintK_opCode[int_ip+4]])
        print("ICONST",unpack('>f',bytearray_bAr)[0])       
        

    elif (int_nargs==2) :
        print("%d:  %s %d %d\n"%(int_ip, listKstrYintK_instr[0],vectorKintK_opCode[int_ip+1],vectorKintK_opCode[int_ip+2] ) )

    elif (int_nargs==3) :
        print("%d:  %s %d %d %d\n"%(int_ip, listKstrYintK_instr[0],vectorKintK_opCode[int_ip+1],vectorKintK_opCode[int_ip+2],vectorKintK_opCode[int_ip+3] ))
    

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
def from_file(coContent):
  """
  """ 
  obj_LispMach=LispMach()  
  obj_LispMach.method_recurs_evalPerList_LrV(parse(coContent))
  return obj_LispMach.method_retB_C_VrL()
#class Context:
#    classIvokingContext_invokingContext=None
#    metadata=None
#    returnIp=0
#    locals_=[]
    
#    def __init__(self,
#        int_returnip):
#        self.int_returnip=int_returnip
#        self.locals_=[0]*(26)
#    def __str__(self):
#        return "locals:" + str(self.locals_)
        
  
#class Vm:
    #code=[]
    #steck=[]
    #ip=0
    #sp=-1
    #fp=0
    #trace=False
    #globals_=[]
    #metadata=None
    ##ctx=None

    #def __init__(self,code,nglobals,trace=False):
        #self.code=code
        #self.globals_=[0]*nglobals
        #self.steck=[0]*100
        #self.pole_vectorKclassContextK_funcCont=[Context(0)]*40
        #print("vector<Context>:",self.pole_vectorKclassContextK_funcCont[0])
        #self.trace=trace
        #self.pole_float_registrThatRetFunc=0.0
        
    #def exec_(self,startip):
        ##self.ctx=Context(None,0,26)
        #self.ip=startip
        #self.cpu() 

    #def cpu(self):
        #opcode=-1
        #I_callSp=-1

        #while (self.ip<len(self.code) and opcode!=HALT):
            #opcode=self.code[self.ip] #fetch 

            #if self.trace:
                #print("number opcode:",opcode)
                #func_vmPrintInstr_SvectorKintKIrV(self.code,self.ip)
                #func_vmPrintStack_SvectorKfloatKI(self.steck,10)
            #if (opcode==ICONST):#switch
               
                #self.sp+=1
                #bytearray_bAr=bytearray([self.code[self.ip+1],self.code[self.ip+2],self.code[self.ip+3],self.code[self.ip+4]])
                #self.steck[self.sp]=unpack('>f',bytearray_bAr)[0]
                #self.ip+=4
            #elif opcode==GSTORE:
                #v=self.steck[self.sp]
                ##print('v',v)
                #self.sp-=1
                #self.ip+=1
                #addr=self.code[self.ip]
                #self.globals_[addr]=v 

            #elif opcode==GLOAD:
                #self.ip+=1
                #addr=self.code[self.ip]
                #v=self.globals_[addr]
                #self.sp+=1
                #self.steck[self.sp]=v 
            #elif opcode==NOOP:
                #pass
           
            #elif opcode==HALT:
                #return
            #elif opcode==BR:
                #self.ip+=1
                #self.ip=self.code[self.ip]
                #continue
            #elif opcode==BRT:
                #self.ip+=1
                #addr=self.code[self.ip]
                #if self.steck[self.sp]==TRUE:
                    #self.ip=addr
                    #self.sp-=1 
                    #continue  
            #elif opcode==BRF:
                #self.ip+=1
                #addr=self.code[self.ip]
                #if self.steck[self.sp]==FALSE:
                    #self.ip=addr
                    #self.sp-=1 
                    #continue
            #elif opcode==IADD:
                #b=self.steck[self.sp]
                #self.sp-=1
                #a=self.steck[self.sp]
                #self.sp-=1
                #self.sp+=1
                #self.steck[self.sp]=a+b
            #elif opcode==ISUB:
                #b=self.steck[self.sp]
                #self.sp-=1
                #a=self.steck[self.sp]
                #self.sp-=1
                #self.sp+=1
                #self.steck[self.sp]=a-b 
            #elif opcode==IMUL:
                #b=self.steck[self.sp]
                #self.sp-=1
                #a=self.steck[self.sp]
                #self.sp-=1
                #self.sp+=1
                #self.steck[self.sp]=a*b 
            #elif opcode==IDIV:
                #b=self.steck[self.sp]
                #self.sp-=1
                #a=self.steck[self.sp]
                #self.sp-=1
                #self.sp+=1
                #self.steck[self.sp]=a/b  
            ##elif opcode==LES:
                ##b=self.steck[self.sp]
                ##self.sp-=1
                ##a=self.steck[self.sp]
                ##self.sp-=1
                ##if a<b:
                    ##self.sp+=1 
                    ##self.steck[self.sp]=TRUE#True 
                ##else:
                    ##self.sp+=1
                    ##self.steck[self.sp]=FALSE#False 
            #elif opcode==PRINT:   
                #self.ip+=1
                #int_chisloIzLocalnihKakParametr=self.code[self.ip]
                #if int_chisloIzLocalnihKakParametr!=25:
                  #print("print loc:",self.pole_vectorKclassContextK_funcCont[I_callSp].locals_[int_chisloIzLocalnihKakParametr])
                #else:
                  #print("print ret reg:",self.pole_float_registrThatRetFunc)  
                    

            #elif opcode==LOAD:
                #self.ip+=1
                #regnum=self.code[self.ip]
                #print("Load regnum",regnum,type(regnum))
                #self.sp+=1
                #print("Load I_callSp",I_callSp,type(I_callSp))
                #print("self.pole_vectorKclassContextK_funcCont[I_callSp]",self.pole_vectorKclassContextK_funcCont[I_callSp])
                #print("len(self.pole_vectorKclassContextK_funcCont[I_callSp].locals_)",len(self.pole_vectorKclassContextK_funcCont[I_callSp].locals_))
                #self.steck[self.sp]=self.pole_vectorKclassContextK_funcCont[I_callSp].locals_[regnum]
                #print("Load I_callSp",I_callSp,type(I_callSp))
     
            #elif opcode==STORE:
                #self.ip+=1
                #regnum=self.code[self.ip]
                #self.pole_vectorKclassContextK_funcCont[I_callSp].locals_[regnum]=self.steck[self.sp]
                ##print(self.pole_vectorKclassContextK_funcCont[I_callSp].locals_[regnum])
                #self.sp-=1 
            #elif opcode==STORE_RESULT:
                #self.ip+=1
                #regnum=self.code[self.ip]
                #self.pole_float_registrThatRetFunc=self.pole_vectorKclassContextK_funcCont[I_callSp].locals_[regnum]
                #self.sp-=1   
            #elif opcode==LOAD_RESULT:
                ##self.ip+=1
                ##regnum=self.code[self.ip]
                #self.sp+=1
                #self.steck[self.sp]=self.pole_float_registrThatRetFunc                                
            #elif opcode==CALL:

                #self.ip+=1

                #I_findex=self.code[self.ip]

                #self.ip+=1
                #I_nargs=self.code[self.ip]
                #I_callSp+=1
                #classContext_curContext=self.pole_vectorKclassContextK_funcCont[I_callSp]
                #classContext_curContext.returnIp=self.ip+1
                

                #I_firstarg=self.sp-I_nargs+1

                #for i in range(0,I_nargs):
                    #classContext_curContext.locals_[i]=self.steck[I_firstarg+i]
                #self.sp-=I_nargs
                #self.ip=I_findex
                #continue
            #elif opcode==RET:
                #self.ip=self.pole_vectorKclassContextK_funcCont[I_callSp].returnIp
                #I_callSp-=1
                #continue
            ##elif opcode==INC:
                ##v=self.steck[self.sp]
                ##v+=1
                ##self.steck[self.sp]=v
            ##elif opcode==DEC: 
                ##v=self.steck[self.sp]
                ##v-=1
                ##self.steck[self.sp]=v
            ##elif opcode==MOD:
                ##b=self.steck[self.sp]
                ##self.sp-=1
                ##a=self.steck[self.sp]
                ##self.sp-=1
                ##self.sp+=1
                ##self.steck[self.sp]=a%b 
            ##elif opcode==ABI:
                ##v=self.steck[self.sp]
                ##self.steck[self.sp]=abs(v)
            ##elif opcode==NEQ:#a != b ?
                ##b=self.steck[self.sp]
                ##self.sp-=1
                ##a=self.steck[self.sp]
                ##self.sp-=1
                ##if a!=b:
                    ##self.sp+=1 
                    ##self.steck[self.sp]=TRUE#True 
                ##else:
                    ##self.sp+=1
                    ##self.steck[self.sp]=FALSE#False   
            ##elif opcode==LEQ:#a <= b ?
                ##b=self.steck[self.sp]
                ##self.sp-=1
                ##a=self.steck[self.sp]
                ##self.sp-=1
                ##if a<=b:
                    ##self.sp+=1 
                    ##self.steck[self.sp]=TRUE#True 
                ##else:
                    ##self.sp+=1
                    ##self.steck[self.sp]=FALSE#False    
            ##elif opcode==EQU:#a == b ?
                ##b=self.steck[self.sp]
                ##self.sp-=1
                ##a=self.steck[self.sp]
                ##self.sp-=1
                ##if a==b:
                    ##self.sp+=1 
                    ##self.steck[self.sp]=TRUE#True 
                ##else:
                    ##self.sp+=1
                    ##self.steck[self.sp]=FALSE#False  
            ##elif opcode==GEQ:#a == b ?
                ##b=self.steck[self.sp]
                ##self.sp-=1
                ##a=self.steck[self.sp]
                ##self.sp-=1
                ##if a>=b:
                    ##self.sp+=1 
                    ##self.steck[self.sp]=TRUE#True 
                ##else:
                    ##self.sp+=1
                    ##self.steck[self.sp]=FALSE#False         
            #else:
                #raise Exception("invalid opcode:",opcode," at ip=",(self.ip))

            #self.ip+=1

#repl()
#str_fileName=sys.argv[1]
#f='./code.lisp' 
str_fileName="./code_Arifm.lisp"
obj_fileDescr=open(str_fileName,"r")
obj_LispMach=LispMach()
str_textProgram=obj_fileDescr.read()
print(str_textProgram)
obj_LispMach.method_recurs_evalPerList_LrV(parse(str_textProgram))
vectorKintK_opCode=obj_LispMach.method_retB_C_VrL()
vectorKintK_opCode.append(HALT)
print(obj_LispMach)
#obj_vm=Vm(vectorKintK_opCode,10,trace=True)
#obj_vm.exec_(obj_LispMach.pole_int_startIp)
float_retVal=vt.eval(vectorKintK_opCode,obj_LispMach.pole_int_startIp,0) 
print(float_retVal)
