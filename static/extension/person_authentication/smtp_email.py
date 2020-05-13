#!/usr/bin/python3
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Libraries for file attached to email
from email import encoders
from email.mime.base import MIMEBase
from itsdangerous import URLSafeTimedSerializer

class SMTPEmail():
    def __init__(self):
        """
        This function set the variables related to the SMTP Server.

        Variables:
            - host: This variable will be used to set the SMTP Server for sending email
            - email_from: This variable represents the email that the class is going to use to send email
            - password: The password for the email account
            - port: The port that will be used to send email in this case is 465 to use a SSL communication
            - context: This variable will load the system's trusted CA certificates, enabled host name checking
            and certificate validation, and try to choose a secure protocol and cipher settings
        """
        self.email_to=''
        self.host = "smtp.gmail.com"
        self.email_from = os.environ['EMAIL_ADRESS']
        self.password = os.environ['EMAIL_PASSWORD']
        self.port = 465
        self.context = ssl.create_default_context()
    
    def send_email(self, email_to, email_subject, msg, files=None):
        """
        This function does the whole process of creating the SMPT Server connection, generating the message
        and finally sends the email.

        Parameters:
            - email_to (String): The receiver of the email
            - email_subject (String): The subject of the email
            - msg (String): The message to be included in the email
            - files (list of strings -> Ej: ["test.txt", "test2.txt"]): The files that we want to attach
                - Default: None 
        """
        server = self.start_smtp_server()
        message = self.create_message(email_from=self.email_from, email_to=email_to, email_subject=email_subject, msg=msg, files=files)

        try:
            server.send_message(msg=message)
        except Exception as e:
            print("Error sending email " + str(e))

        server.quit()

    def start_smtp_server(self):
        """
        This function creates the SMTP Server using the configuration previously mentioned
        int the __init__ function.
        
        Parameters: None
        """
        server = None
        try:
            server = smtplib.SMTP_SSL(host=self.host, port=self.port, context=self.context)
            server.login(self.email_from, self.password)
        except Exception as e:
            print("Error starting SMTP server " + str(e))
        
        return server

    def create_message(self, email_from, email_to, email_subject, msg, files=None):
        """
        This function will generate the body of the email, who sends the email, the receiver
        and if it has any attachment.

        Parameters:
            - email_from (string): Who sends the email
            - email_to (string): The receiver of the email
            - email_subject (string): The subject of the email
            - msg (string): The message to be included in the email
            - files (list of strings -> Ej: ["test.txt", "test2.txt"]): The files that we want to attach
                - Default: None 
        """
        message = None
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = email_subject
            message["From"] = email_from
            message["To"] = email_to

            if files is not None:
                for file in files:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(open(file, "rb").read())
                    
                    encoders.encode_base64(part)

                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {file}",
                    )

                    message.attach(part)

            html = """\
            <html>
            <body>
                <p>Hi,<br>
                """+msg+"""<br>
                Regards,<br>
                EOEPCA Team<br>
                </p>
            </body>
            </html>
            """
            message_body = MIMEText(html, "html")
            message.attach(message_body)
        except Exception as e:
            print("Error creating email message " + str(e))
        
        return message

    
    def set_email(self, email):
        self.email_to=email

    def send_confirmation(self):

        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        confirm_url = url_for('confirmation', token=confirm_serializer.dumps(self.email, salt='email-confirmation-salt'), _external=True)
        html = render_template('activate.html',confirm_url=confirm_url)
        subject = 'Delete Account Confirmation'
        smtp_client.send_email(self.email, subject, html) # Here is to use the smtp client for sending the mail to the user
        print('A new confirmation email has been sent.', 'success')

    def getConfirmation(self,token):
        try:
            confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            mail = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
            return mail
        except:
            print('The confirmation link is invalid or has expired.', 'error')
            
 