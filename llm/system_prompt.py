from llm.prompts import get_prompt

def get_system_prompt( scenario, mode, correction ):
    content=get_prompt(scenario)
    content+=f"\nMode: {mode} \nCorrection: {correction}"
    return {"role": "system", "content": content}
    

