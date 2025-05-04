from langchain_openai import ChatOpenAI
import os
class Loader(object):
    
    @classmethod
    def _open_ai_chat_gpt_4o(this,**kwargs):
        api_key = os.getenv("OPENAI_API_KEY", None)
        model = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)
        return model
    
    @classmethod
    def load_model(this,model, **kwargs):
        print("Loading model : " + str(model))
        model_method = getattr(this, "_" + model, None)
        if model_method is None:
            raise ValueError(f"Model {model} not found.")
        
        llm = model_method(**kwargs)
        
        return llm
    
    