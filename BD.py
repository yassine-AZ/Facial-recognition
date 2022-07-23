import mysql.connector
from datetime import datetime
# start connection
from PIL._imaging import convert

try:
    db =mysql.connector.connect(
        host ='localhost',
        user ='root',
        passwd ='',
        database ='pfe'
    )
except:
    print("erreur")


def enregistrer(nom,reconnaissance,image):
    try:
        cursor = db.cursor()
        val = (nom, datetime.now().strftime("%H:%M:%S"), datetime.now().strftime("%Y-%d-%m"),reconnaissance,image)
        cursor.execute("insert into  historique_general(personne,heure,date_entree,reconnaissance,image) values(%s,%s,%s,%s,%s)", val)
        db.commit()
        cursor.close();
        db.close
    except Exception as e:
        print("erreur" + str(e))


# enregistrer("yassine","connue",file)
