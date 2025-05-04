
def get_as_openai_function(query: str) -> dict:
    from ai.models.loader import Loader
    model = Loader.load_model("open_ai_chat_gpt_4o")
    from ai.agents.amadeus_hotel.tools import search_hotels
    
    tools = [ search_hotels]
    from langgraph.prebuilt import create_react_agent
    from ai.agents.amadeus_hotel.instruction import system_prompt
    langgraph_agent_executor = create_react_agent(model, tools, prompt=system_prompt)
    messages = langgraph_agent_executor.invoke({"messages": [("user", query)]})
    response = messages["messages"][-1].content
    print("response:", response)
    return response


# if __name__ == "__main__":
#     # Example usage
#     # query = "Find me a flight from New York to Los Angeles on 2025-05-01."
#     query = "what is your name"
#     response = get_as_openai_function(query)
#     print(response)