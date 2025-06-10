import streamlit as st
import smtplib
from email.message import EmailMessage
import ssl


EMAIL_SENDER = st.secrets.get("email_sender")
EMAIL_PASSWORD = st.secrets.get("email_password")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def send_report_email_interface(pdf_buffer):
    st.subheader("📤 Email Report")
    recipient = st.text_input("Enter recipient email")
    subject = st.text_input("Email Subject", value="Your MRI Report from MedMRI AI")
    body = st.text_area("Message Body", value="Please find your MRI analysis report attached.")

    if st.button("Send Report", key="email_submit_btn"):
        if not EMAIL_SENDER or not EMAIL_PASSWORD:
            st.error("Missing sender credentials in secrets.toml")
            return

        if not recipient:
            st.warning("Please enter a recipient email address.")
            return

        if "@" not in recipient or "." not in recipient:
            st.warning("Please enter a valid email address.")
            return

        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = EMAIL_SENDER
            msg["To"] = recipient
            msg.set_content(body)

            # Attach PDF
            msg.add_attachment(
                pdf_buffer.read(),
                maintype="application",
                subtype="pdf",
                filename="MRI_Report.pdf"
            )

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(msg)

            st.success(f"✅ Email sent to {recipient}")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
