from enums import Guardrail as grd
# not in use
class Guardrail:
    def __init__(self) -> None:
        pass
    
    def check_all(self):
        greeting_status, greeting_response = self.check_greeting()
        if greeting_status:
            return grd.TYPE_GREETING,greeting_status, greeting_response
        relevance_status, relevance_response = self.check_relevance()
        if relevance_status:
            return grd.TYPE_RELEVANCE, relevance_status, relevance_response
    
    def check_greeting(self):
        response = "Hey, how can I help you today?" #sample
        return True,response
    
    def check_relevance(self):
        response = "I am sorry, I can not respond to that."
        return False, response