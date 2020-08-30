from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
# [END vision_face_detection_tutorial_imports]
import os, io
import argparse
import pyautogui
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'google_creds.json'
# [START vision_face_detection_tutorial_send_request]
def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.
    Args:
        face_file: A file-like object containing an image with faces.
    Returns:
        An array of Face objects with information about the picture.
    """
    # [START vision_face_detection_tutorial_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_face_detection_tutorial_client]

    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(
        image=image, max_results=max_results).face_annotations
# [END vision_face_detection_tutorial_send_request]

def mostlikely(face):

   

    d= {0:'UNKNOWN', 1:'VERY_UNLIKELY', 2:'UNLIKELY', 3:'POSSIBLE',4:'LIKELY', 5:'VERY_LIKELY'}                
    d2 = {'anger':face.anger_likelihood,'joy':face.joy_likelihood,'sorrow':face.sorrow_likelihood,'surprise':face.surprise_likelihood,'headwear':face.headwear_likelihood}
    likely = []
    maxNumber = 0
    for num in d2.values():
        maxNumber = max(maxNumber,num)
    
    for state, num2 in d2.items():
        if num2 == maxNumber:
            likely.append(state)
    
    
    #print("maxNumber: ", maxNumber)
    likely.append(" Certain: "+d[maxNumber])
    print(likely)
    return likely

# [START vision_face_detection_tutorial_process_response]
def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.
    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    print()
    # Sepecify the font-family and the font-size
    for face in faces:
        mostlikely(face)
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 30),
                  str(format(face.detection_confidence, '.3f')) + '%',
                  fill='#FF0000',)
    im.save(output_filename)
    
# [END vision_face_detection_tutorial_process_response]

def take_ss(search_filename,faces_filename):
    zoomcent = pyautogui.locateCenterOnScreen('zoomblurr.png')

    if zoomcent==None:
        print('not zoom logo found')
    else:
        pyautogui.click(zoomcent)
       
    cent = pyautogui.locateCenterOnScreen(search_filename)

    if cent==None:
        print('center not found')
    elif zoomcent==None and cent==None:
        pyautogui.click(1000,500)
        time.sleep(2)
        im1 = pyautogui.screenshot()
        im1.save(faces_filename)
        #take_ss(search_filename,faces_filename)
    else:
        pyautogui.click(cent)
        time.sleep(2)
        im1 = pyautogui.screenshot()
        im1.save(faces_filename)

# [START vision_face_detection_tutorial_run_application]
def mainzoomlabel(input_filename, output_filename, max_results):
    time.sleep(5)
    take_ss('gall5.png',input_filename)

    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)
# [END vision_face_detection_tutorial_run_application]

#print(main("forframes.jpg","response.jpg",5))

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         description='Detects faces in the given image.')
#     parser.add_argument(
#         'input_image', help='the image you\'d like to detect faces in.')
#     parser.add_argument(
#         '--out', dest='output', default='out.jpg',
#         help='the name of the output file.')
#     parser.add_argument(
#         '--max-results', dest='max_results', default=4,
#         help='the max results of face detection.')
#     args = parser.parse_args()

#     main(args.input_image, args.output, args.max_results)