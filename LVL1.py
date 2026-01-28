import A3
import os,re
from FuncionesTime import *
from XLSXmanag import *
import inspect

YEL = "\x1b[33m"
RES = "\x1b[0m"
print(YEL+"A3.py in"+RES)
MAG = "\x1b[35m"
RED = "\x1b[31m"
GRE = "\x1b[32m"
RNG = "\x1b[38;5;166m"
BLU = "\x1b[34m"

A3.load_model()

print(RNG+"LVL1.py in"+RES)
date=str(time.asctime(time.localtime()))

def getXfrom(X,qst):
    xp="is there "+X+" in the expression '"+qst+"' ?"
    #print (xp)
    A=A3.ObltrtNObooL(xp)
    print(A)
    if A:return(A3.ObltrtNOapt("from '"+qst+"' output the "+X))
    else:return(A)

def update_param(param, new_value, file_path="UsrFrm.txt"):
    # Ubicación absoluta del archivo respecto a este script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, file_path)
    param = param.lower()
    lines = []
    # update_param debug print
    print(param+RNG+" actualized to "+RES+new_value+RNG+" in "+RES+file_path) 
    with open(abs_path, "r", encoding="utf-8") as f:
        for line in f:
            key, sep, val = line.partition(":")
            if key.lower().strip() == param:
                lines.append(f"{key}:{new_value}\n")
            else:
                lines.append(line)

    with open(abs_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def Memorize(param, Q, file_path="UsrFrm.txt"):
    # Ubicación absoluta del archivo respecto a este script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, file_path)

    param = param.lower()
    lines = []

    with open(abs_path, "r", encoding="utf-8") as f:
        for line in f:
            clave, _, valor = line.partition(":")
            if clave.lower().strip() == param:
                if valor.strip().upper() == "UNKNOWN":
                    new_value=getXfrom(param,Q)
                    lines.append(f"{clave}:{new_value}\n")
                    print(+f"✅ {param} actualizado a {new_value}")
                else:
                    lines.append(line)
                    print(f"⚠️ {param} ya tiene valor '{valor.strip()}', no se cambia")
            else:
                lines.append(line)

    with open(abs_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def update_sbmodel(sbmdlpath):
    date=str(time.asctime(time.localtime()))
    update_param("time_info",date,sbmdlpath)

def update_user(cont,id):
    FirstName=getXfrom("first name",cont)
    LastName=getXfrom("last name",cont)
    Email=getXfrom("email",cont)
    if FirstName:actualizar_registro_si_vacio(id, {"First_Name":FirstName})
    if LastName:actualizar_registro_si_vacio(id, {"Last_Name":LastName})
    if Email:actualizar_registro_si_vacio(id, {"Email":Email})

def writer(cont):
    with open("archivo.txt", "w", encoding="utf-8") as f:
        f.write(cont)

def fix_path(p):
    return p.strip().replace("\\", "/")  # opcional: normaliza las barras

def V_Nm(var):
    frame = inspect.currentframe().f_back
    nombres = [name for name, val in frame.f_locals.items() if val is var]
    return nombres[0] if nombres else None

def verify00(inipt,aiopt,sbmdl1):
    quest="bool ¿the response:("+aiopt+"), responds acordly and precise to the query("+inipt+")? bool"
    return A3.interact(quest)

def verify01(inipt,aiopt,sbmdl1,sbmdl2):
    quest="bool ¿the response:("+aiopt+"), responds acordly to the query("+inipt+"), under the model conditions("+sbmdl2+")? bool"
    return A3.interact(sbmdl1,quest,True)

def needAgnd(q):
    Sckeywords= ["schedule" , "time", "agenda" , "appointment" , "cita"]
    R=A3.Keypier(q)
    R_low = R.lower()
    if any(word in R_low for word in Sckeywords):
        return str(" sys_ElaguAgenda: "+A3.read_file_content('ElaguAgenda.txt'))
    else:return("")

def Rflx(use_imp):
    extra=None
    #acondicionar, adaptar , interpolar , pulir , 
    bqst00 = "¿Are you formated to "+use_imp+"?"
    bqst01 = "¿Are you informated to "+use_imp+"?"
    #bqst02 = "¿can you answer with just 1 word to "+use_imp+"?"
    kqst00 = "¿an action for "+use_imp+"?"
    kqst01 = "¿whats the missing information keyword of ("+use_imp+")?"
    kqst02 = "¿whats doing th user when says (¿"+use_imp+"?)"
    #Flkeywords= ["file", "open", "read", "metadata"]
    #Dtkeywords= ["date", "today", "time" , "current" , "actual"]
    Sckeywords= ["schedule" , "time", "agenda" , "appointment" , "cita"]
    SVkywords= ["save" , "guardar", "write" , "escribir" ]
    #print(". . .KlqltngDfqltyLvL. . .") 
    S0=A3.Surelias(bqst00,5)
    #print(bqst00," ;lvl: ",10-S0)
    S1=A3.Surelias(bqst01,5)
    #print(bqst01," ;lvl: ",10-S1)
    #S2=Surelias(bqst02)
    #print(bqst02," ;lvl: ",10-S2)
    if ((S0+S1)/2)<=2: 
        print("AI : ¡iAskng4HLP! , qstlvl:",5-((S0+S1)/2))
        R=A3.Keypier(kqst00)+A3.Keypier(kqst01)
        #print(R)
        R_low = R.lower()
        if any(word in R_low for word in Sckeywords):
            extra=str(" sys_ElaguAgenda: "+A3.read_file_content('ElaguAgenda.txt'))
    #print(user_imput)
    #AI_R=interact(B1W,user_Rqst,True)
    #print(AI_R)
        #print(extra)
        #print(R)
    return(extra)

while False:
    user_imput = input("Tu: ")
    #update_sbmodel("DRC.txt")
    if user_imput.lower() in ["salir", "exit", "bye"]:
        print("autoexit")
        break
    #update_sbmodel("UsrFrm.txt")
    #Memorize("first_name",user_imput)
    #Rflx(user_imput)
    #test00_qst = "ready to ("+user_imput+")"
    #test01_qst = f"Are you informated to ({user_imput})"
    #print((test00_qst),"AiBooL:",ObltrtNObooL(test00_qst))
    #print((test01_qst),"AiBooL:",ObltrtNObooL(test01_qst))
    #print("B1Ai: ",ObltrtNOapt(user_imput))
       
    #verify01(user_imput+str(extra),AI_R,B1W,B1W)
    #verify00(user_imput+str(extra),AI_R,B1W)
    
    interact(user_imput,True)
    