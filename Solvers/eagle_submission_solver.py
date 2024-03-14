import numpy as np
from LSBSteg import decode
import requests
import random
from eagle_model import predictor

api_base_url = "http://3.70.97.142:5000/eagle"
team_id="6fKwkav"


def init_eagle(team_id):
    myparams={"teamId": team_id}
    response = requests.post(f"{api_base_url}/start", json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        response = response.json()
        print(response)
        print("init eagle response")
        return response
    else:
        print(response.status_code)
        print("init eagle response failed")
        print(response.text)
        return response
    '''
    In this fucntion you need to hit to the endpoint to start the game as an eagle with your team id.
    If a sucessful response is returned, you will recive back the first footprints.
    '''
    pass

def select_channel(footprint):
    #check if the footprint is real 
    #x['1'] is the first channel
    #spectograms need to be np arrays
    #if the spectograms are empty or fake, return 0
    #if the spectograms are real, return the channel number
    if predictor(np.array(footprint['1'])):
        return 1
    elif predictor(np.array(footprint['2'])):
        return 2
    elif predictor(np.array(footprint['3'])):
        return 3
    else:
        return 0
    
    '''
    According to the footprint you recieved (one footprint per channel)
    you need to decide if you want to listen to any of the 3 channels or just skip this message.
    Your goal is to try to catch all the real messages and skip the fake and the empty ones.
    Refer to the documentation of the Footprints to know more what the footprints represent to guide you in your approach.        
    '''
    pass
  
def skip_msg(team_id):
    myparams={"teamId": team_id}
    response = requests.post(f"{api_base_url}/skip-message", json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        try:
            response = response.json()
            print(response)
            print("init eagle response")
            return response
        except Exception as e:
            print(response)
            print(response.text)
            print("end fox response")
            return response
    else:
        print(response.status_code)
        print("init eagle response failed")
        print(response.text)
        return response
    '''
    If you decide to NOT listen to ANY of the 3 channels then you need to hit the end point skipping the message.
    If sucessful request to the end point , you will expect to have back new footprints IF ANY.
    '''
    pass
  
def request_msg(team_id, channel_id):
    myurl= f"{api_base_url}/request-message"
    myparams={
        "teamId": team_id, "channelId": channel_id
        }
    
    response = requests.post(url=myurl,json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        response = response.json()
        print(response)
        print("request msg response")
        return response
    else:
        print(response.status_code)
        print("request msg response failed")
        print(response.text)
        return None
    '''
    If you decide to listen to any of the 3 channels then you need to hit the end point of selecting a channel to hear on (1,2 or 3)
    '''
    pass

def submit_msg(team_id, decoded_msg):
    myurl= f"{api_base_url}/submit-message"
    myparams={
        "teamId": team_id, "decodedMsg": decoded_msg
        }
    
    response = requests.post(url=myurl,json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        try:
            response = response.json()
            print(response)
            print("submit msg response")
            return response
        except Exception as e:
            print(response)
            print(response.text)
            print("end fox response")
            return response
    else:
        print(response.status_code)
        print("submit msg response failed")
        print(response.text)
        return None
    '''
    In this function you are expected to:
        1. Decode the message you requested previously
        2. call the api end point to send your decoded message  
    If sucessful request to the end point , you will expect to have back new footprints IF ANY.
    '''
  
def end_eagle(team_id):
    myurl= f"{api_base_url}/end-game"
    myparams={
        "teamId": team_id
        }
    
    response = requests.post(url=myurl,json=myparams)
    if response.status_code == 200 or response.status_code == 201:
        print(response)
        print(response.text)
        print("end eagle response")
        return response
    else:
        print(response.status_code)
        print("end eagle response failed")
        print(response.text)
        return response
    '''
    Use this function to call the api end point of ending the eagle  game.
    Note that:
    1. Not calling this fucntion will cost you in the scoring function
    '''
    pass

def submit_eagle_attempt(team_id):
    '''
     Call this function to start playing as an eagle. 
     You should submit with your own team id that was sent to you in the email.
     Remeber you have up to 15 Submissions as an Eagle In phase1.
     In this function you should:
        1. Initialize the game as fox 
        2. Solve the footprints to know which channel to listen on if any.
        3. Select a channel to hear on OR send skip request.
        4. Submit your answer in case you listened on any channel
        5. End the Game
    '''
    x=init_eagle(team_id)
    flag=1
    y=select_channel(x['footprint'])
    while(flag==1):
        
        if y==0:
            z=skip_msg(team_id)

            if  not any('nextFootprint' in d for d in z):
                flag=0
            else:
                x=z
                y=select_channel(x['nextFootprint'])
                continue
            
        z=request_msg(team_id, y)
        encoded = np.array(z['encodedMsg'])
        msg=decode(encoded)
        f=submit_msg(team_id, msg)
        try:
            if not any('nextFootprint' in d for d in f):
                flag=0
                print(f.text)
            else:    
                x=f
                y=select_channel(x['nextFootprint'])
        except Exception as e:
            print(msg)
            print("here",e)
    end_eagle(team_id)
    pass


submit_eagle_attempt(team_id)
