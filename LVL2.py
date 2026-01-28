# LVL2.py - Topic-based chatbot module with keyword classification.
# Provides DRCteract for dynamic response context and KeyRing for intent detection.
# Loads topic-specific content from Topics/ directory.

from LVL1 import *

'''
import pyttsx3

print(MAG+"LVL2.py in"+RES)

#Voice sets
tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voice', voices[1].id)
tts.setProperty('rate', 150)
'''

def get_topic(topic):
    match topic.lower():
        case "schedule":
            return A3.read_file_content(r'Topics/HORARIO.txt')  
        case "pricing":
            return A3.read_file_content(r'Topics/TARIFAS.txt')
        case "payment":
            return A3.read_file_content(r'Topics/PAGO.txt')
        case "booking":
            return A3.read_file_content(r'Topics/HORARIO.txt')
        case "preparation":
            return A3.read_file_content(r'Topics/GENERAL.txt')
        case "services":
            return A3.read_file_content(r'Topics/SERVICIOS.txt')
        case "location":
            return A3.read_file_content(r'Topics/UBICACION.txt')
        case "contact":
            return A3.read_file_content(r'Topics/CONTACTO.txt')
        case _:
            return ""

def DRCteract(Q,H,ID):
    TPS=["services" , "schedule"  , "payment" , "agenda" , "preparation" , "location" , "pricing" , "contact" , "greeting"]
    SYS_HELP=get_topic(A3.SelFromList(TPS,Q))
    crear_registro(ID)
    update_user(Q,ID)
    User_Data=leer_registro(ID)
    #print("usuario  :",User_Data)
    #print("ayuda    :",SYS_HELP)
    SYS_GEN=("system data = ",SYS_HELP,User_Data)
    lang=A3.ObltrtNOapt("What's the language of the expression '"+Q+"' ?")
    update_sbmodel('DRC.txt')
    update_param("user_language",lang,'DRC.txt')
    DRC=A3.read_file_content(r'DRC.txt')  
    respuesta=A3.Histeract(Q,H,DRC,SYS_GEN)
    return respuesta

def KeyRing(use_imp):
    kqst =  "keyword of ("+use_imp+")"
    R=A3.Keypier(kqst)
    R_low = R.lower()

    # Diccionario estilo "case"
    cases = {
        "agenda": [r"\bschedule\b" , r"\btime\b", r"\bagenda\b" , r"\bappointment\b" , r"\bcita\b"],
        "reset": [r"\breset\b", r"\breiniciar\b", r"\badiós\b", r"\bgoodbye\b", r"\bbye\b", r"\bexit\b", r"\bsalir\b"],
        "price": [r"\bprice\b",r"\bcost\b",r"\brate\b",r"\bvalue\b",r"\bfee\b",r"\bamount\b",r"\bcharge\b",r"\bpayment\b",r"\bpay\b",r"\bprecio\b",r"\bcosto\b",r"\btarifa\b",r"\bvalor\b",r"\bpago\b"],
        "exit": [r"\bquit\b", r"\bexit\b", r"\bbye\b"]
    }

    # Recorre las claves y sus listas de patrones
    for case_value, patterns in cases.items():
        if any(re.search(pattern, R_low) for pattern in patterns):
            return case_value

    # Si no coincide con nada
    return None

#Connection with LM Studio local
def get_user_id(msg_data):
    chat_id = msg_data.get("from")        # número o grupo
    author = msg_data.get("author")       # solo existe en grupos
    if author:
        return f"{chat_id}:{author}"      # separa cada persona en un grupo
    return chat_id                         # chat privado = solo el número

hlpsw=0

while False:
    #pdate_sbmodel('DRC.txt')
    #DRC.append(read_file_content('DRC.txt'))
    usim = input("Tu: ")
    '''if hlpsw==0:
        bonus=needAgnd(usim)
        if bonus !=None:    
            DRC.insert(0,bonus)
            hlpsw=1'''
    # Get response from the model
    #reply= Cntxtract(mess,usim,False,str(DRC))
    #DRC.pop()
    print(KeyRing(usim))
    #mess.append({"role": "assistant", "content": reply})
    # Save to file


    


    
    
