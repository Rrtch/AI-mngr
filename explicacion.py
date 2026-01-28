# crear funcion de suma
def interact(system_input,system_prompt=P3):    
     
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": system_input},
    ]

    output = ephemer(prompt)
    return output