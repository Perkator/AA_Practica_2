from flask import Flask, request, jsonify
import random, threading
#Based on: https://realpython.com/api-integration-in-python/

app = Flask(__name__)

it = 0
things = [ ]
clients = 3
sent = 0
sem = threading.Semaphore(1)

def accessPost(thing):
    global sent, things
    if len(things) < clients:   # You can only access to "post" if we're getting the "things"
        things.append(thing)
        return True
    return False

def accessGet():
    global sent, things
    if len(things) == clients:  # You can only acces "things" if it's completely full
        sent = sent + 1 # ++ to "things" i sent
        # If sent values are 3 we've to send the last "things" and reset the variable
        if sent == clients:
            sent = 0
            return "reset"
        else:
            return "pass"
    return "w8"

@app.post("/addThing")
def add_thing():
    global sem
    sem.acquire()
    if request.is_json:
        thing = request.get_json()  # Get the value
        if accessPost(thing):    # Ask for acces
            sem.release()
            return thing, 201
        else:
            sem.release()
            return jsonify("w8")
    return {"error": "Request must be JSON"}, 415

@app.get("/getThing")
def get_thing():
    global sem, things, it
    sem.acquire()
    ans = accessGet()   # Ask for acces
    if ans == "pass": 
        sem.release()
        return jsonify(things)
    elif ans == "reset":
        temp = things
        things = [ ]
        it = it + 1
        print(f"Iteration nº: {it}")
        sem.release()
        return jsonify(temp)
    else:
        sem.release()
        return jsonify("w8")






# Save the file as: app.py  #or: export FLASK_APP=app.py
# Run: python -m flask run
# With curl or browser: http://127.0.0.1:5000/random    
# curl -i http://127.0.0.1:5000/addThing -X POST -H 'Content-Type: application/json' -d '{"seed":2022}'