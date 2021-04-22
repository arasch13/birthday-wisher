##################### Happy birthday wisher project ######################

import os
import random
import pandas
import datetime as dt
import smtplib

# -------------------------------------------- load csv data ------------------------------------------------------
data = pandas.read_csv("./birthdays.csv", ).to_dict(orient='records')

# ------------------------------------- collect all birthday people -----------------------------------------------
birthday_people = []
today = dt.datetime.today()
for person in data:
    is_birthday = today.month == person['month'] and today.day == person['day']
    if is_birthday:
        birthday_people.append(
            {
                'name': person['name'],
                'email': person['email']
            }
        )

# ------------------------------------- generate email letter text -----------------------------------------------
NAME_TAG = "[NAME]"
for person in birthday_people:
    letter_directory = "./letter_templates"
    letter_templates = os.listdir(letter_directory)
    letter_templates = [f"{letter_directory}/{template}" for template in letter_templates]
    random_letter_template = random.choice(letter_templates)
    with open(random_letter_template) as letter_template:
        raw_text = letter_template.read()
    email_text = raw_text.replace(NAME_TAG, person['name'])
    person['email_text'] = email_text

# -------------------------------------------- send email ------------------------------------------------------
def send_mail(smtp_server, sender_email, sender_email_password, recipient_email, email_text, email_subject=""):
    with smtplib.SMTP(smtp_server) as connection:
        connection.starttls()
        connection.login(user=sender_email, password=sender_email_password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=recipient_email,
            msg=f"Subject:{email_subject}\n\n{email_text}"
        )

my_email = "arasch.lakghomi@googlemail.com"
my_email_password = "Nin.64.tendo"
smtp_server = "smtp.gmail.com"

for person in birthday_people:
    recipient_email = person['email']
    email_subject = f"Happy birthday {person['name']}!"
    email_text = person['email_text']
    send_mail(smtp_server, my_email, my_email_password, recipient_email, email_text, email_subject)
