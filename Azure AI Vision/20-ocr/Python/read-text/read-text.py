from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials


def main():

    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

       # Authenticate Azure AI Vision client
        credential = CognitiveServicesCredentials(cog_key) 
        cv_client = ComputerVisionClient(cog_endpoint, credential)
        
        # Menu for text reading functions
        print('1: Use Read API for image\n2: Use Read API for document\n3: Read handwriting\nAny other key to quit')
        command = input('Enter a number:')
        if command == '1':
            image_file = os.path.join('images','Lincoln.jpg')
            GetTextRead(image_file)
        elif command =='2':
            image_file = os.path.join('images','Rome.pdf')
            GetTextRead(image_file)
        elif command =='3':
            image_file = os.path.join('images','Note.jpg')
            GetTextRead(image_file)
                

    except Exception as ex:
        print(ex)

def GetTextRead(image_file):
    print('Reading text in {}\n'.format(image_file))
    # Use Read API to read text in image
    with open(image_file, mode="rb") as image_data:
        read_op = cv_client.read_in_stream(image_data, raw=True)

        # Get the async operation ID so we can check for the results
        operation_location = read_op.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Wait for the asynchronous operation to complete
        while True:
            read_results = cv_client.get_read_result(operation_id)
            if read_results.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                break
            time.sleep(1)

        # If the operation was successfully, process the text line by line
        if read_results.status == OperationStatusCodes.succeeded:
            for page in read_results.analyze_result.read_results:
                for line in page.lines:
                    print(line.text)
                    # Uncomment the following line if you'd like to see the bounding box 
                    print(line.bounding_box)

if __name__ == "__main__":
    main()