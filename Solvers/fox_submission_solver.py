import requests
import numpy as np
from riddle_solvers import riddle_solvers
import string_divider
import LSBSteg

api_base_url = "http://3.70.97.142:5000/fox"
team_id="6fKwkav"

def init_fox(team_id):
    myparams={"teamId": team_id}
    response = requests.post(f"{api_base_url}/start", json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        response = response.json()
        print(response)
        print("init fox response")
        return response
    else:
        print(response.status_code)
        print("init fox response failed")
        print(response.text)
        return response
'''
    In this fucntion you need to hit to the endpoint to start the game as a fox with your team id.
    If a sucessful response is returned, you will recive back the message that you can break into chunkcs
      and the carrier image that you will encode the chunk in it.
    '''
    # pass

def generate_message_array(chunk, image_carrier):  
   
    
    empty=np.array(image_carrier)
    
    steg1 = np.array(image_carrier).copy()
    encoded_image1 = LSBSteg.encode(steg1,chunk)

    steg2 = np.array(image_carrier).copy()
    encoded_image2 = LSBSteg.encode(steg2,"fake")
    
   
    
    imgs=[]
    imgs.append(empty.tolist())
    imgs.append(encoded_image2.tolist())
    imgs.append(encoded_image1.tolist())
    msgentities=['E', 'F', 'R']
    '''
    In this function you will need to create your own startegy. That includes:
        1. How you are going to split the real message into chunkcs
        2. Include any fake chunks
        3. Decide what 3 chuncks you will send in each turn in the 3 channels & what is their entities (F,R,E)
        4. Encode each chunck in the image carrier  
    '''
    return imgs,msgentities
    pass 

def get_riddle(team_id, riddle_id):
    myurl= f"{api_base_url}/get-riddle"
    myparams={
        "teamId": team_id, "riddleId": riddle_id
        }
    
    response = requests.post(url=myurl,json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        response = response.json()
        print(response)
        print("get riddle response")
        return response
    else:
        print(response.status_code)
        print("get riddle response failed")
        print(response.text)
        return None
    '''
    In this function you will hit the api end point that requests the type of riddle you want to solve.
    use the riddle id to request the specific riddle.
    Note that: 
        1. Once you requested a riddle you cannot request it again per game. 
        2. Each riddle has a timeout if you didnot reply with your answer it will be considered as a wrong answer.
        3. You cannot request several riddles at a time, so requesting a new riddle without answering the old one
          will allow you to answer only the new riddle and you will have no access again to the old riddle. 
    '''
    pass

def solve_riddle(team_id, solution):
    myurl= f"{api_base_url}/solve-riddle"
    myparams={
        "teamId": team_id, "solution": solution
        }
    
    response = requests.post(url=myurl,json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        response = response.json()
        print(response)
        print("solve riddle response")
        return response
    else:
        print(response.status_code)
        print("solve riddle response failed")
        print(response.text)
        return None
    '''
    In this function you will solve the riddle that you have requested. 
    You will hit the API end point that submits your answer.
    Use te riddle_solvers.py to implement the logic of each riddle.
    '''
    pass

def send_message(team_id, messages, message_entities=['F', 'E', 'R']):
    myurl= f"{api_base_url}/send-message"
    myparams={"teamId": team_id, "messages": messages, "message_entities": message_entities}
    response = requests.post(url=myurl,json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        response = response.json()
        print(response)
        print("send message response")
        return response
    else:
        print(response.status_code)
        print("send message response failed")
        print(response.text)
        return response
    '''
    Use this function to call the api end point to send one chunk of the message. 
    You will need to send the message (images) in each of the 3 channels along with their entites.
    Refer to the API documentation to know more about what needs to be send in this api call. 
    '''
    pass
   
def end_fox(team_id):
    myurl= f"{api_base_url}/end-game"
    myparams={
        "teamId": team_id
        }
    
    response = requests.post(url=myurl,json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        print(response)
        print(response.text)
        print("end fox response")
        return response
    else:
        print(response.status_code)
        print("end fox response failed")
        print(response.text)
        return response
    
    '''
    Use this function to call the api end point of ending the fox game.
    Note that:
    1. Not calling this fucntion will cost you in the scoring function
    2. Calling it without sending all the real messages will also affect your scoring fucntion
      (Like failing to submit the entire message within the timelimit of the game).
    '''
    pass

def submit_fox_attempt(team_id):
    
    
    x=init_fox(team_id)
    
    riddles=['problem_solving_easy', 'problem_solving_hard','problem_solving_medium',
             'sec_hard','ml_easy','cv_easy']
    
        
    for r in riddles:
        try:
            y=get_riddle(team_id, r)
            print(y['test_case'])
            solution=riddle_solvers[r](y['test_case'])
            z=solve_riddle(team_id, solution)
            if z['status']=="success":
                print(r, "solved")
                print(z['total_budget'])
            else:
                print(r, "failed")
                print(z['total_budget'])
          
        except Exception as e:
            print("Failed to solve", r, "due to exception:", e)
            # Continue to the next riddle
            continue   
        
    try:  
        message_array = string_divider.divide_string(x['msg'],6)
    except Exception as e:
        print("Failed to make msg array due to exception:", e)
        message_array=x['msg']
    try:
        
        for chunk in message_array:
            msgs,entities=generate_message_array(chunk, x['carrier_image'])
            status=send_message(team_id, msgs,entities)
            print(status['status'])
    except Exception as e:
        print("Failed to send due to exception:", e)
        empty=np.array(x['carrier_image'])
        steg1 = np.array(x['carrier_image']).copy()
        encoded_image1 = LSBSteg.encode(steg1,x['msg'])
        msgs=[empty.tolist(),empty.tolist(),encoded_image1.tolist()]
        send_message(team_id, msgs,['E', 'E', 'R'])

    
    end_fox(team_id)
   
        
        
    
    
    '''
     Call this function to start playing as a fox. 
     You should submit with your own team id that was sent to you in the email.
     Remeber you have up to 15 Submissions as a Fox In phase1.
     In this function you should:
        1. Initialize the game as fox 
        2. Solve riddles 
        3. Make your own Strategy of sending the messages in the 3 channels
        4. Make your own Strategy of splitting the message into chunks
        5. Send the messages 
        6. End the Game
    Note that:
        1. You HAVE to start and end the game on your own. The time between the starting and ending the game is taken into the scoring function
        2. You can send in the 3 channels any combination of F(Fake),R(Real),E(Empty) under the conditions that
            2.a. At most one real message is sent
            2.b. You cannot send 3 E(Empty) messages, there should be atleast R(Real)/F(Fake)
        3. Refer To the documentation to know more about the API handling 
    '''
    pass 


submit_fox_attempt(team_id)