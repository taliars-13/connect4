import requests
import random
import threading
import numpy as np

base = "https://connect4.minsky.co"
headers = {
    "api-key": "491d5f67-5c1d-4f56-a5ca-db053394cd8c"
}


#hello

def checkwin(board):
    for col in range(0, 7): 
        tboard = np.array(board)
        print(board)
        for row in range(5, -1, -1):
            if tboard[row, col] == 0:
                tboard[row, col] = 37
                break
        #print(tboard)
        result = check_victory(tboard)
        print(result, "result of check")
        if result != 0: 
            go= str(col)
            print(result, "hello")
            return go
    
    return False

def checklose(board, opp):
    for col in range(0, 7): 
        tboard = np.array(board)
        for row in range(5, -1, -1):
            if tboard[row, col] == 0:
                tboard[row, col] = opp
                break
        result = check_victory(tboard)
        print(result, "result of opp check")
        if result != 0: 
            go= str(col)
            print(result, "hellowe")
            return go
    return False


def play(board):
    response2 = requests.get(base + "/api/status", headers=headers)
    if response2.json()['code'] == 6:
        opp = response2.json()["opponent_id"]
    result = 0
    board = np.array(board)
    win = checkwin(board)
    lose = checklose(board, opp)
    if win: 
        go=win
    elif lose:
        go =lose

        # elif result != 37 and result != 0: 
        #     headers["column"]= str(col)
        #     break
    else: 
        rand = random.randrange(0,6)
        while rand in playable(board): 
            rand = random.randrange(0,6)
        print("hola", rand)
        go = str(rand)

    headers["column"] = go
    print(go)
    response = requests.post(base + "/api/play", headers=headers)
    response2 = requests.get(base + "/api/status", headers=headers)
    print(response.json())
    if response.json()['code'] == 18 and response2.json()['code'] == 6:
        threading.Timer(0, full_game).start()

def playable(board): 
    notplay = []
    for col in range(0,6):
         if board[0][col] != 0: 
             notplay.append(col)
    return notplay

def check_victory(board: np.array) -> int:
    for row in range(7 - 4):
        for col in range(8 - 4):
            v = check_subfield(board[row:row + 4, col:col + 4])
            if v > 0:
                return v
    return 0



def check_subfield(field: np.array) -> int:
    # check diagonal.
    v = same_number(np.diagonal(field))
    if v > 0:
        return v
    

    for i in range(4):
        # check column
        v = same_number(field[i, :])
        if v > 0:
            return v
        # check row
        v = same_number(field[:, i])
        if v > 0:
            return v

            
    v = same_number(np.diagonal(np.fliplr(field)))
    if v > 0:
        return v
    return 0

def same_number(values: list) -> int:
    return int((values == values[0]).all() * values[0])


# response = requests.get(base + "/api/status", headers=headers)

# if response.status_code == 200:
#     resp = response.json()
#     if resp["code"] == 9:
#         response = requests.post(base + "/api/join_game", headers=headers)
#         #print(response.json())
#     elif resp["code"] == 6 or resp["code"] == 5:
#         while resp["code"]==6 or resp["code"]==5:
#             if resp["code"] == 6:
#                 if resp["your turn"] != False:
#                     play(resp["board"])
#             response = requests.get(base + "/api/status", headers=headers)
#             resp = response.json()
#     else:
#         print(resp["text"])

# else:
#     print("rah")
#     print(response.status_code)
#     print(response.content)


def full_game():
    response = requests.get(base + "/api/status", headers=headers)
    if response.status_code == 200:
        resp = response.json()
        if resp["code"] == 9:
            response = requests.post(base + "/api/join_game", headers=headers)
            print(response.json())
            threading.Timer(1, full_game).start()
        elif resp["code"] == 6:
            if resp["your turn"] == False:
                # print("Not your turn.")
                threading.Timer(5, full_game).start()
            else:
                play(resp["board"])
        elif resp['code'] == 5:
            print(resp["text"])
            threading.Timer(5, full_game).start()
        else:
            print(resp["text"])


full_game()