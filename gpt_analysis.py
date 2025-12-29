import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

INSTRUCTIONS = """
You are a professional, but spunky and animated, college basketball sports analyst tasked with summarizing the output of a March Madness game simulator. 
In your analysis of the stats, briefly explain why one team may have beaten the other. 
You will not be given summaries of individual games, so DO NOT comment on individual games.
Be general and focus on long-term team-level statistical advantages or disadvantages.

Your task is to analyze the simulation output data frame below and provide a concise summary of the simulation results in 30 words or fewer:
"""

def create_prompt(winner, record, contributions):
    prompt = f"""
        {INSTRUCTIONS}
        Overall winner: {str(winner)}
        Simulation Results: {str(record)}
        Player Contributions: {str(contributions)}
    """
    return prompt


def GPT_Game_Analysis(prompt, model="gpt-5-nano-2025-08-07"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(        
        model=model, messages=messages)
    return response.choices[0].message.content