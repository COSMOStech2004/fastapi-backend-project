import smtplib
from email.message import EmailMessage
from app.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_FROM_EMAIL,
    FRONTEND_RESET_PASSWORD_URL,
    FRONTEND_VERIFY_EMAIL_URL
)


def send_password_reset_email(email: str, reset_token: str):
    reset_link = f"{FRONTEND_RESET_PASSWORD_URL}?token={reset_token}"

    message = EmailMessage()

    message["Subject"] = "Password Reset Request"
    message["From"] = SMTP_FROM_EMAIL
    message["To"] = email

    message.set_content(
        f"""
Hello,

We received a request to reset your password.

Click the link below to reset your password:

{reset_link}

This link will expire in 15 minutes.

If you did not request this, you can ignore this email.

Thank you.
"""
    )

    with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT)) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)



def send_email_verification_email(email: str, verification_token: str):
    verification_link = f"{FRONTEND_VERIFY_EMAIL_URL}?token={verification_token}"
    print(verification_link)
    message = EmailMessage()

    message["Subject"] = "Verify Your Email"
    message["From"] = SMTP_FROM_EMAIL
    message["To"] = email

    plain_text_content = f"""
Hello,

Thank you for registering.

Please verify your email using the link below:

{verification_link}

This link will expire in 24 hours.

If you did not create this account, you can ignore this email.

Thank you.
"""

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Email Verification</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="padding: 30px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; padding: 30px;">
                    <tr>
                        <td align="center">
                            <h2 style="color: #333333;">Verify Your Email</h2>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <p style="font-size: 16px; color: #555555;">
                                Hello,
                            </p>

                            <p style="font-size: 16px; color: #555555;">
                                Thank you for creating an account. Please verify your email address by clicking the button below.
                            </p>
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="padding: 25px 0;">
                            <a href="{verification_link}"
                               style="background-color: #16a34a; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-size: 16px; display: inline-block;">
                                Verify Email
                            </a>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <p style="font-size: 14px; color: #777777;">
                                This link will expire in 24 hours.
                            </p>

                            <p style="font-size: 14px; color: #777777;">
                                If the button does not work, copy and paste this link into your browser:
                            </p>

                            <p style="font-size: 14px; color: #16a34a; word-break: break-all;">
                                {verification_link}
                            </p>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding-top: 20px;">
                            <p style="font-size: 14px; color: #555555;">
                                Thank you,<br>
                                Backend App Team
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

    message.set_content(plain_text_content)

    message.add_alternative(
        html_content,
        subtype="html"
    )

    with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT)) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)