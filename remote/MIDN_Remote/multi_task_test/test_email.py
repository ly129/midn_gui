from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email_alert ( email, sessoion_id):
        # create message osinstance
        msg = MIMEMultipart()
        # setup the parameters of the message
        msg['From'] = "alert@sbbdmaplp001"
        msg ['To'] =   email
        msg['Subject'] = "CTA Detection job"

        message_text = """

        This is the link to your submitted CTA dection job:
        http://129.106.31.45:7790/status/{}


        """.format ( sessoion_id)

        msg.attach(MIMEText(message_text, 'plain'))
        server = smtplib.SMTP('smtp.uth.tmc.edu')
        server.starttls()
        server.sendmail(msg['From'], email, msg.as_string())
        server.quit()

        return

send_email_alert ('luyao.chen@uth.tmc.edu','20220311-eef6fb6a-a183-11ec-b0c5-0242ac110003')
