import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send2():
    print('Sending email...')

# Send email using Gmail
def send(district, locality, place):

    # Gmail account credentials
    sender_email = 'zagadelha@gmail.com'
    sender_password = 'wezc urmu rcih gefd'

    # Recipient email address
    recipient_email = 'zagadelha@gmail.com'

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = 'zagadelha@gmail.com'
    message['To'] = 'zagadelha@gmail.com'
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

