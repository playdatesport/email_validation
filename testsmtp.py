import smtplib
import dns.resolver
import re

# Function to check if an email address is valid by SMTP
def validate_email_smtp(email):
    # Check if email format is correct using regex
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(regex, email):
        return False, "Invalid email format."

    # Extract domain from email address
    domain = email.split('@')[-1]

    # Perform DNS lookup for MX records
    try:
        dns.resolver.resolve(domain, 'MX')
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False, "No MX records found for domain."

    # Connect to SMTP server
    smtp_server = None
    for mx_record in dns.resolver.resolve(domain, 'MX'):
        smtp_server = str(mx_record.exchange)
        break

    try:
        # Establish connection with SMTP server
        with smtplib.SMTP(smtp_server) as server:
            server.set_debuglevel(0)  # Turn off debug messages
            server.connect(smtp_server)

            # Say hello to the server
            server.helo()

            # Send MAIL FROM command (simulate sender address)
            server.mail('test@example.com')  # Sender address can be arbitrary

            # Send RCPT TO command (check recipient address)
            code, message = server.rcpt(email)

            # Check server's response code
            if code == 250:
                return True, "Valid email address."
            else:
                return False, f"Invalid email address. Server response: {message.decode()}"

    except smtplib.SMTPException as e:
        return False, f"SMTP Error: {str(e)}"

# Example usage
email = "test@example.com"
is_valid, message = validate_email_smtp(email)
print(is_valid, message)
