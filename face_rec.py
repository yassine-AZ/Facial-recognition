import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
# from pfe import emailler,BD
from pfe import emailler


def get_encoded_faces():

    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    
    return encoded
def classify_face(im):

    faces = get_encoded_faces() #1-attribuer le resultat de la fonction  get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())


    img = cv2.imread(im,1) #2-lire la photo entrez dans les parametres :

 
    face_locations = face_recognition.face_locations(img)#3-la detection des yeux,nez,bouche  en le mettre dans la variable 'face_locations'
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_names = []
    for face_encoding in unknown_face_encodings:

        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"


        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):

            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)


            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)

    while True:
        cv2.imwrite("personne_detecter.png",img)
        return face_names


cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) == ord('q'):
        im=cv2.imwrite("image_capturer.jpg", frame)
        break

cap.release()
cv2.destroyAllWindows()

#remplir lles personnes detectees
list_valide=[]
list_Unknown=[]

print(classify_face("image_capturer.jpg"))

for  per in classify_face("image_capturer.jpg"):
    print(per)
    if per.__eq__("Unknown"):
        list_Unknown.append("unknown")
    elif per != "Unknown":
        list_valide.append(per)


#affiche des resultat
list=",".join(list_valide)


print("list unknown : "+str(list_Unknown) +" sa longeur est : "+ str(len(list_Unknown)))
print("list_connu : "+str(list_valide)+" sa longeur est : "+ str(len(list_valide)))


def convertToBinaryData():

    with open("image_capturer.jpg", 'rb') as file:
        binaryData = file.read()
    return binaryData

image=convertToBinaryData()

if len(list_valide) != 0:
    print("i find  these people: "+list)
    BD.enregistrer(list,"connue",image)
    if len(list_Unknown) ==0:
        emailler.sendemail("sender", "", "receiver",
                       "important","i find these people  : "+list)
    elif len(list_Unknown) !=0:
        emailler.sendemail("sender", "", "receiver",
                           "important", "i find these people  : "+ list+" with  "+str(len(list_Unknown))+" people not known")
elif len(list_Unknown) !=0:
    print("Wearning !! there are people not known ")
    emailler.sendemail("abouhir14@gmail.com", "", "chhiwatetv@gmail.com", "important",
                       "Warning  there are   "+str(len(list_Unknown))+" people not known : ")
    BD.enregistrer("unknown","nonconnue",image)













