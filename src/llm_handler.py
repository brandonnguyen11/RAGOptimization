# ============================================
# FILE: src/llm_handler.py
# ============================================
"""LLM API handler for OpenAI and Groq"""
from typing import Optional
from config import MODELS, TEMPERATURE

class LLMHandler:
    """Handles calls to LLM APIs"""
    
    def __init__(self, api_choice: str, api_key: str):
        """
        Initialize LLM handler
        
        Args:
            api_choice: Either "OpenAI" or "Groq"
            api_key: API key for the selected provider
        """
        self.api_choice = api_choice
        self.api_key = api_key
        self.model = MODELS[api_choice]
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate response from LLM
        
        Args:
            system_prompt: System instruction
            user_prompt: User query with context
            
        Returns:
            str: LLM response
        """
        if self.api_choice == "OpenAI":
            return self._call_openai(system_prompt, user_prompt)
        elif self.api_choice == "Groq":
            return self._call_groq(system_prompt, user_prompt)
    
    def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API"""
        from openai import OpenAI
        
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=TEMPERATURE
        )
        
        return response.choices[0].message.content
    
    def _call_groq(self, system_prompt: str, user_prompt: str) -> str:
        """Call Groq API"""
        from groq import Groq
        
        client = Groq(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=TEMPERATURE
        )
        
        return response.choices[0].message.content
