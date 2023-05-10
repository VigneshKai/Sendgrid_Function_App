import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        # Retrieve the required information from the request payload
        employee_name = req_body.get('employee_name')
        employee_email = req_body.get('employee_email')
        sending_email = req_body.get('sending_email')
        password = req_body.get('Password')

        # Retrieve the template ID and from_email from environment variables
        template_id = os.environ.get('SENDGRID_TEMPLATE_ID')
        from_email = os.environ.get('SENDGRID_FROM_EMAIL')

        # Set the dynamic template data
        template_data = {
            'Employee_Name': employee_name,
            'Employee_EAddress': employee_email
        }

        # Create the email message
        message = Mail(
            from_email=from_email,
            to_emails=sending_email,
        )
        message.template_id = template_id
        message.dynamic_template_data = template_data

        # Send the email using SendGrid API
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        if sendgrid_api_key:
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)
            logging.info("Email sent successfully!")
        else:
            logging.error("Please set the SENDGRID_API_KEY environment variable.")

        return func.HttpResponse("Email sent successfully!", status_code=200)

    except Exception as e:
        logging.error("Error sending email:", str(e))
        return func.HttpResponse("Error sending email", status_code=502)
