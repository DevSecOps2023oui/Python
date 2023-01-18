import hashlib
import paramiko
import csv
import time
from datetime import datetime
import random
import os
import shutil

while True:
    if not os.path.exists('./csv'):
        os.mkdir('./zipFile')
    
    # Current date and time for file name
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")

    # LES DIFFERENTS PATH
    local_file_txt = "./csv/weather-" + dt_string + ".txt"
    local_file_csv = './csv/weather-' + dt_string + '.csv'
    remote_path_zip = "/home/ubuntu/NodeWatcher/dist/csv/new/weather-" + dt_string + ".zip"

    # PARAMETRES DE GENERATION DE FICHIER
    duration = 5
    start_time = time.time()
    end_time = start_time + duration

    with open(local_file_csv, mode='w') as csv_file:
        fieldnames = ['temperature', 'humidity', 'wind', 'date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        while time.time() < end_time:
            date = now.strftime("%d-%m-%Y %H:%M:%S")
            temperature = random.randint(5, 25)
            humidity = random.randint(50, 80)
            wind = random.randint(10, 100)
            writer.writerow({'temperature': temperature, 'humidity': humidity, 'wind': wind, 'date': date})
            time.sleep(5)

    # Ouvrir le fichier en mode binaire
    with open(local_file_csv, "rb") as file:
        # Lire le contenu du fichier
        data = file.read()
        # Créer un objet hash
        md5 = hashlib.md5()
        # Mettre à jour le hash avec les données du fichier
        md5.update(data)
        # Obtenir la valeur hash hexadécimale
        hex_hash = md5.hexdigest()
        # Écrire le hash dans un fichier .txt
        with open(local_file_txt, "w") as hash_file:
            hash_file.write(hex_hash)

    # A FAIRE : Chiffrement RSA
    # LECTURE PUBLIC KEY

    # with open('./key/id_rsa.pub', 'rb') as key_file:
    #    key_data = key_file.read()
    #   pub_key = rsa.PublicKey.load_pkcs1(key_data)
    # Encrypt CSV
    # with open('./csv/weather-' + dt_string + '.csv', 'rb') as input_file, open('./csvEncrypted/weather-' + dt_string + '.csv.enc', 'wb') as output_file:
    #   data = input_file.read() #  ciphertext = rsa.encrypt(data, pub_key)
    # output_file.write(ciphertext)

    # Créer un objet SSHClient
    client = paramiko.SSHClient()

    # Autoriser les clés de serveurs inconnus
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Spécifiez la clé privée à utiliser pour l'authentification
    private_key = paramiko.RSAKey.from_private_key_file("./.ssh/id_rsa")

    # Connexion au serveur distant
    client.connect(hostname="141.145.211.53", username="ubuntu", pkey=private_key)

    # Ouvrir la connexion SFTP
    sftp = client.open_sftp()



    # Spécifiez les chemins des fichiers à compresser
    file1 = local_file_txt
    file2 = local_file_csv

    # Spécifiez le nom et le chemin du dossier de destination
    folder_name = 'weather-'+dt_string
    destination_path = "./zipFile/"

    # Créez le dossier
    if not os.path.exists(destination_path + folder_name):
        os.mkdir(destination_path + folder_name)

    # Déplacez les fichiers dans le dossier de destination
    shutil.move(file1, destination_path + folder_name)
    shutil.move(file2, destination_path + folder_name)

    # Utilisez la fonction make_archive de shutil pour compresser le dossier
    shutil.make_archive(destination_path + folder_name, "zip", destination_path, folder_name)

    # Transfert vers le serveur distant
    sftp.put('./zipFile/weather-'+dt_string + '.zip', remote_path_zip)
    print("transaction reussi !!!!!")

    # Fermer la connexion
    client.close()

    #sup zipFile
    shutil.rmtree('./zipFile')

    #

