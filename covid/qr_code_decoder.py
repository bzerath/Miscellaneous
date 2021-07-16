"""
https://blog.callicode.fr/post/2021/covid_pass.html
"""

import os
import zlib
from datetime import datetime

import PIL.Image
import base45
import cbor2
import pyzbar.pyzbar


class Payload:
    """
    Juste pour rendre l'analyse et le print plus buvables.
    """
    def __init__(self, payload: dict):
        self.raw_payload = payload

        self.payload_origin = payload[1]
        self.raw_emission_date = payload[6]
        self.emission_date = datetime.strftime(datetime.fromtimestamp(self.raw_emission_date),
                                               "%d/%m/%Y, %H:%M:%S")
        self.raw_expiration_date = payload[4]
        self.expiration_date = datetime.strftime(datetime.fromtimestamp(self.raw_expiration_date),
                                                 "%d/%m/%Y, %H:%M:%S")

        self.payload_content = payload[-260][1]
        self.raw_date_of_birth = self.payload_content["dob"]
        self.date_of_birth = datetime.strftime(datetime.strptime(self.raw_date_of_birth,
                                                                 "%Y-%m-%d"),
                                               "%d/%m/%Y")
        self.nom = self.payload_content["nam"]["fn"]
        self.prenom = self.payload_content["nam"]["gn"]

        self.vaccine_certificat_id = self.payload_content["v"][0]["ci"]
        self.vaccine_certificat_country = self.payload_content["v"][0]["co"]
        self.vaccine_target = self.payload_content["v"][0]["tg"]
        self.vaccine_type = self.payload_content["v"][0]["vp"]
        self.vaccine_medicinal_product = self.payload_content["v"][0]["mp"]
        self.vaccine_marketing_authorization = self.payload_content["v"][0]["ma"]
        self.vaccine_number_of_doses_given = self.payload_content["v"][0]["dn"]
        self.vaccine_number_of_doses_needed = self.payload_content["v"][0]["sd"]
        self.raw_vaccination_date = self.payload_content["v"][0]["dt"]
        self.vaccination_date = datetime.strftime(datetime.strptime(self.raw_vaccination_date,
                                                                    "%Y-%m-%d"),
                                                  "%d/%m/%Y")
        self.vaccination_certificate_issuer = self.payload_content["v"][0]["is"]

    def __repr__(self):
        return """Les données contenues sont les suivantes :
    Origine du document : {payload_origin}
    Date d'émission du document : {emission_date}
    Date d'expiration du document : {expiration_date}
    
    {prenom} {nom}, né(e) le {date_of_birth}
    Identifiant du présent certificat : {vaccine_certificat_id}
    Origine du présent certificat : {vaccine_certificat_country}
    Nom de l'organisme gérant la dernière vaccination : {vaccination_certificate_issuer}
    Date de la dernière vaccination : {vaccination_date}
    Nombre de doses nécessaires : {vaccine_number_of_doses_needed}
    Nombre de doses injectées : {vaccine_number_of_doses_given}
    
    Vaccine target : {vaccine_target}
    Vaccine type : {vaccine_type}
    Vaccine medicinal product : {vaccine_medicinal_product}
    Vaccine marketing authorization : {vaccine_marketing_authorization} 
        """.format(payload_origin=self.payload_origin,
                   emission_date=self.emission_date,
                   expiration_date=self.expiration_date,
                   prenom=self.prenom,
                   nom=self.nom,
                   date_of_birth=self.date_of_birth,
                   vaccine_certificat_id=self.vaccine_certificat_id,
                   vaccine_certificat_country=self.vaccine_certificat_country,
                   vaccination_certificate_issuer=self.vaccination_certificate_issuer,
                   vaccination_date=self.vaccination_date,
                   vaccine_number_of_doses_needed=self.vaccine_number_of_doses_needed,
                   vaccine_number_of_doses_given=self.vaccine_number_of_doses_given,
                   vaccine_target=self.vaccine_target,
                   vaccine_type=self.vaccine_type,
                   vaccine_medicinal_product=self.vaccine_medicinal_product,
                   vaccine_marketing_authorization=self.vaccine_marketing_authorization
                   )


if __name__ == "__main__":
    for path in (os.path.join("Fichiers", "qrcode.png"),
                 os.path.join("Fichiers", "qrcode_anneclaire.jpeg")):
        # Ouverture de l'image...
        img = PIL.Image.open(path)

        # Décodage du QR code...
        data = pyzbar.pyzbar.decode(img)
        cert = data[0].data.decode()

        # Retrait du préfixe 'HC1' ('Health Certificate Version 1')...
        b45data = cert.replace("HC1:", "")

        # Décodage (base 45) et décompression (zlib) de l'objet CBOR ('Concice Binary Objet Representation')...
        zlibdata = base45.b45decode(b45data)
        cbordata = zlib.decompress(zlibdata)

        # Lecture de l'objet CBOR...
        decoded = cbor2.loads(cbordata)

        # Header (morceau n°1)
        header = cbor2.loads(decoded.value[0])

        # Morceau n°2 -> en général vide

        # Payload (morceau n°3)
        raw_payload = cbor2.loads(decoded.value[2])
        payload_tranformed = Payload(raw_payload)

        # Signature numérique (morceau n°4)
        sign = decoded.value[3]

        print("\n------------------------------------------------\n")
        print(payload_tranformed)
