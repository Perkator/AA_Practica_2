from flask import Flask, jsonify
import requests, threading, random, json, time

# Variables
numThreads = 3
threads = []
# URL para dar los valores
urlGet = "http://127.0.0.1:5000/getThing"
# URL para conseguir los valores
urlPost = "http://127.0.0.1:5000/addThing"
# Cabeceras
headers = {"Content-Type": "application/json"}

def exec():
    Ok = False
    it = 0
    recover = [ ]
    while Ok == False:
        recover = [ ]
        varSent = random.randint(1,4)
        Ok = True
        sent = requests.post(urlPost, json={"value": varSent}, headers=headers)
        while type(sent) is str:
            sent = requests.post(urlPost, json={"value": varSent}, headers=headers)
        got = requests.get(urlGet).json()
        while type(got) is str:
            got = requests.get(urlGet).json()
        for obj in got:
            recover.append(obj.get("value"))
        for v in recover:
            if v != varSent:
                Ok = False
        if Ok:
            print(f"We're OK with the results {recover}")
        else:
            print(f"We disagree with the results {recover}")

def main():
    for i in range(numThreads):
        t = threading.Thread(target=exec)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()