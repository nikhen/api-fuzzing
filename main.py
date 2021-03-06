import requests
import argparse
import os

from concurrent.futures import ThreadPoolExecutor, as_completed
from progress.bar import Bar

def sendRequest(secret):
    target_url = args.url + secret
    if args.debugging:
        print("Sending request: " + target_url)

    try:
        response = requests.get(
            target_url,
            headers = {
                'Cache-Control': 'no-transform'
            }
        )
        if args.debugging:
            print(response.text)
            print(response.status_code)

    except ConnectionError as conn_e:
        if args.debugging:
            print("Connection error: See details below.")
            print(conn_e)
        return response.status_code

    if response.status_code < 400:
        print("\nGot response " + str(response.status_code) + " for request " + str(target_url) )
        os._exit(1)
    elif response.status_code == 429:
        print("Got status code 429 (too many requests).")
        return response.status_code
    else:
        return response.status_code


def iterateOverPermutations(str): 
     permList = [] 
     charList = list(str)
     permList = permutate(charList)
     maxElements = len(permList)

     bar = Bar("Fuzzing " + args.url, max=maxElements)
 
     for perm in list(permList): 
         processes = []
         with ThreadPoolExecutor(max_workers=args.threads) as executor:
             permutation_string = ''.join(perm)
             processes.append(executor.submit(sendRequest, permutation_string))

         if not args.debugging:
             bar.next()

     bar.finish()
     print("Finished fuzzing target " + args.url)
        
def permutate(permutationList):
    returnList = []
    bufferList = []
    elementString = ""
    permutationListLength = len(permutationList)

    if permutationListLength < 2:
        return None
    elif permutationListLength == 2:
        elementString = ''.join(permutationList)
        returnList.append(elementString)
        bufferList.append(permutationList[1])
        bufferList.append(permutationList[0])
        elementString = ''.join(bufferList)
        returnList.append(elementString)
        return returnList
    else:
        bufferChar = permutationList[0]
        if args.fuzzing:
            bufferInt = ord(bufferChar)
            bufferInt += 1
            if bufferInt < 256:
                bufferChar = chr(bufferInt)
            else:
                bufferChar = chr(bufferInt - 10)

        for s in permutate(permutationList[1:]):
            bufferList = []
            bufferList.append(bufferChar)
            bufferList.append(s)
            returnList.append(''.join(bufferList))        
            bufferList = []
            bufferList.append(s)
            bufferList.append(bufferChar)
            returnList.append(''.join(bufferList))        
       
        return returnList

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Fuzzing API secrets.')
    parser.add_argument('--url', required=True, help='The target URL. This URL should point to and enpoint. URL parameters should be such that a secret can be appended.')
    parser.add_argument('--secret', default="123456789", help='Initial API secret to start fuzzing from.')
    parser.add_argument('--fuzzing', default=True, help='Enable Fuzzing.')
    parser.add_argument('--threads', default=5, type=int, help='Number of threads calling target API simultaneously.')
    parser.add_argument('--debugging', help='Enable extended output.')

    args = parser.parse_args()

    iterateOverPermutations(args.secret)
