# crear funcion de suma
def interact(system_input,system_prompt=P3):    
     
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": system_input},
    ]

    output = ephemer(prompt)
    return output


 # crear funcion de resta
def ObltrtNOapt(q):     #No 1 word? No return cicle - filter
    brk=0
    while brk!=1:
        I=interact(q+" return a word.",B1)
        brk=len(I.split())
        #print(q,YEL+"ObltrtNOapt:"+RES,I)  #DEBUG
    return I