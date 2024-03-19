import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Send email using Gmail
def send(district, locality, place):

    # Gmail account credentials
    sender_email = 'mail@domain.com'
    sender_password = 'password'

    # Recipient email address
    recipient_email = 'mail@domain.com'

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = 'mail@domain.com'
    message['To'] = 'mail@domain.com'
    message['Subject'] = 'SEF Date/Time available!'

    # Add body to the email
    body = 'District: ' + district + '\nLocality: ' + locality + '\nAtendance Place: ' + place
    message.attach(MIMEText(body, 'plain'))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:

        # Login to Gmail
        server.login(sender_email, sender_password)
        
        # Send email
        server.sendmail(sender_email, recipient_email, message.as_string())

    print("Email sent successfully!")

