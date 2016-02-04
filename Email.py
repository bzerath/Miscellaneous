#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import smtplib
import sys, os
import base64

from time import strftime, localtime, sleep

from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from mimetypes import guess_type


class Email:
    """
    Classe pour la création d'un email à envoyer.
    :param sender: email de l'expéditeur (peut être différent de l'email du serveur SMTP)
        --> C'est lui qui s'affichera dans l'en-tête du mail
    :param receiver: email du destinataire
    :param objet: objet du mail
    :param corps: corps du mail
    :param format: facultatif, format du corps ('plain' ou 'html')
    :param attachments: facultatif, liste des chemins de fichiers.

    >>>     mail = Email (sender = sender,
    >>>            receiver = receiver,
    >>>            objet = "test pièce jointe",
    >>>            corps = '''Ceci est un teste de corps àvèc dés âccent$
    >>>            et des retours à la ligne
    >>>            '''

    """

    sender = ""
    receiver = ""
    objet = ""
    corps = ""
    pause = 0.1
    attachments = []
    msg = MIMEMultipart('alternative')

    def __init__(self, sender, receiver, objet, corps, cc_receiver=[],
                    bcc_receiver=[], format='html', attachments=[]):
        self.sender = sender
        self.receiver = receiver
        self.cc_receiver = cc_receiver
        self.bcc_receiver = bcc_receiver
        self.objet = objet
        self.corps = corps
        self.attachments = attachments
        self.format = format

        self.formatMessage(self.format)

    def attach(self, attachments):
        for fichier in attachments:
            mimetype, encoding = guess_type(fichier)
            mimetype = mimetype.split('/', 1)
            part = MIMEBase(mimetype[0], mimetype[1])
            part.set_payload( open(fichier, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(fichier))
            self.msg.attach(part)

    def formatMessage(self, format):
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = self.objet.decode("utf-8")
        self.msg['From'] = self.sender
        if isinstance(self.receiver, basestring):
            self.msg['To'] = self.receiver
        else:
            self.msg['To'] = ";".join(self.receiver)
        if isinstance(self.cc_receiver, basestring):
            self.msg['CC'] = self.cc_receiver
        else:
            self.msg['CC'] = ";".join(self.cc_receiver)

        self.msg.attach(MIMEText(self.corps,
                                 format,
                                 "utf-8"))

        self.attach(self.attachments)

    def __str__(self):
        return self.msg.as_string()


class Serveur:
    """
    Classe pour l'accès à un serveur smtp.
    :param smtp: adresse smtp du serveur
    :param sender: adresse pour se connecter
    :param password: mot de passe pour se connecter

    >>>     serveur = Serveur(smtp=smtp,
    >>>                       sender=sender,
    >>>                       password="pimousse123")
    >>>     serveur.send(mail)

    """

    smtp = ""
    timeout = 60
    sender = ""
    receiver = ""
    password = ""

    def __init__(self, smtp, sender, password):
        self.smtp = smtp
        self.sender = sender
        self.password = password

    @staticmethod
    def _add_receiver(self, dest, addresses=None):
        """
        Add to email recipients the address(es) contained in addresses.
        Addresses can be either a single email address or a list of email
        addresses.
        :param dest: current list of email recipients.
        :param addresses: single email address or list of email addresses.
        """
        if addresses:
            try:
                dest = dest + addresses
            except TypeError:
                dest.append(addresses)

        return dest

    def send(self, email):
        """
        :param email: instance de classe Email
        :param bcc: liste d'adresses mail à mettre en copie cachée

        Envoie le mail donné à aux adresses dans les champs destinataire, cc et
        bcc de l'instance email.
        """

        dest = []
        dest = self._add_receiver(dest, email.receiver)
        dest = self._add_receiver(dest, email.cc_receiver)
        dest = self._add_receiver(dest, email.bcc_receiver)
        print(dest)

        try:
            smtpserver = smtplib.SMTP(self.smtp, timeout=self.timeout)
#            smtpserver.set_debuglevel(1)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(self.sender, self.password)
            import ipdb; ipdb.set_trace()
            smtpserver.sendmail(from_addr=email.sender,
                                to_addrs=dest,
                                msg=email.msg.as_string())
            smtpserver.close()
            for receiver in dest:
                print ("Email envoyé à {receiver} de la part de {sender}.".format(receiver=receiver,
                                                                                  sender=email.sender))
        except smtplib.SMTPException:
            sys.stderr.write("Error: unable to send email\n")
            raise


if __name__ == "__main__":

    """
    Exemple prêt à l'emploi (sauf les identifiants du serveur SMTP)


    """

    # Déclaration des identifiants
    sender = 'noreply@coucou.fr'
    password = ''
    smtp = "mail.gandi.net"

    # Déclaration du destinataire
    receiver = 'francois.hollande@elysee.fr'

    # Déclaration du chemin vers la pièce jointe (à ignorer s'il n'y a pas de
    #  pièce jointe)
    fichiers = ["output.pdf"]

    # Déclaration du corps de mail. Dans cet exemple, il en HTML.
    # Enlever les balises HTML si on veut du plain text.
    html = """
Bonjour, je vous préviens que nous allons réaliser un vol à vue avec les caractéristiques suivantes :<br/>
<br/><br/>
<b>Lieu-dit du vol :</b> {lieu}<br/>
<b>Coordonnées géographiques :</b> {lat} {lon}<br/>
</br>
<b>Nom du télépilote :</b> {nom_pil}<br/>
<b>Téléphone :</b> {numero}<br/>
<br/>
<u><b>Caractéristiques du drone : </b></u><br/>
<b>Aéronef :</b> senseFly eBee<br/>
<b>Voilure fixe.</b><br/>
<b>Envergure :</b> 94 cm<br/>
<b>Masse maximale au décollage :</b> 0.7 kilogrammes<br/>
<b>Hauteur maximum du drone :</b> 150 m<br/>
"""
    # Déclaration du serveur SMTP qu'on va utiliser.
    serveur = Serveur(smtp=smtp,
                      sender=sender,
                      password=password)

    # Déclaration de l'email à envoyer.
    mail = Email(sender="operations@coucou.fr",
                 receiver=receiver,
                 cc_receiver=['bz@airinov.fr', 'benjamin.xeroth@coucou.fr'],
                 bcc_receiver=['bg_du_93@yahoo.fr'],
                 objet="{date} / {CP} / {nom_expl}".format(date=strftime("%Y-%m-%d",localtime()),
                                                           CP="75018",
                                                           nom_expl="Coucou"),
                 corps=html.format(
                       lieu="Paris",
                       lat="""48°53'37.21"N""",
                       lon="""2°21'14.52"E""",
                       nom_pil="Peter Parker",
                       numero="0102030405"),
                 format='html',
                 attachments=[])

    # Envoi du mail
    serveur.send(mail)











