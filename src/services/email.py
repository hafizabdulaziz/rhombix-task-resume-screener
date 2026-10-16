import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import structlog

from src.core.config import settings

logger = structlog.get_logger()

SHORTLISTED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Inter', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; }
        .header { text-align: center; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 20px; }
        .logo { font-size: 24px; font-weight: bold; color: #10b981; }
        .content { font-size: 16px; line-height: 1.6; color: #cbd5e1; }
        .button { display: inline-block; background-color: #10b981; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin-top: 20px; font-weight: bold; }
        .footer { margin-top: 30px; font-size: 12px; text-align: center; color: #64748b; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Rhombix ResumeScreener Pro</div>
        </div>
        <div class="content">
            <p>Dear <strong>{{ candidate_name }}</strong>,</p>
            <p>We are thrilled to inform you that your application for the position of <strong>{{ job_title }}</strong> has successfully passed our AI screening evaluation and you have been <strong>SHORTLISTED</strong>!</p>
            <p>Our recruitment team will review your profile and reach out to you shortly regarding the next interview steps.</p>
            <a href="{{ portal_url }}" class="button">View Application Status</a>
        </div>
        <div class="footer">
            <p>&copy; 2026 Rhombix ResumeScreener Pro. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

HR_DIGEST_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Inter', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; }
        .header { text-align: center; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 20px; }
        .logo { font-size: 24px; font-weight: bold; color: #10b981; }
        .content { font-size: 16px; line-height: 1.6; color: #cbd5e1; }
        .footer { margin-top: 30px; font-size: 12px; text-align: center; color: #64748b; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Rhombix HR Digest</div>
        </div>
        <div class="content">
            <p>Hello Recruiter,</p>
            <p>Batch screening for job position <strong>{{ job_title }}</strong> has been completed successfully.</p>
            <p>Total candidates screened: <strong>{{ total_screened }}</strong></p>
            <p>Top candidate matched: <strong>{{ top_candidate }}</strong> (Score: {{ top_score }}%)</p>
        </div>
        <div class="footer">
            <p>&copy; 2026 Rhombix ResumeScreener Pro. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, html_content: str) -> bool:
        """
        Sends an HTML email using configured SMTP server or logs it if in mock/development mode.
        """
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.smtp_from_email
            message["To"] = to_email

            part = MIMEText(html_content, "html")
            message.attach(part)

            if settings.smtp_host == "smtp.example.com" or (settings.environment == "development" and not settings.smtp_user):
                logger.info("mock_email_sent", to=to_email, subject=subject)
                return True

            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                if settings.smtp_user and settings.smtp_password:
                    server.starttls()
                    server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.smtp_from_email, to_email, message.as_string())
            
            logger.info("email_sent_successfully", to=to_email, subject=subject)
            return True
        except Exception as e:
            logger.error("email_dispatch_failed", error=str(e), to=to_email)
            return False

    @staticmethod
    async def send_shortlisted_notification(candidate_name: str, candidate_email: str, job_title: str, portal_url: str = "http://localhost:8000") -> bool:
        template = Template(SHORTLISTED_TEMPLATE)
        html = template.render(candidate_name=candidate_name, job_title=job_title, portal_url=portal_url)
        return await EmailService.send_email(candidate_email, f"Congratulations! Shortlisted for {job_title}", html)

    @staticmethod
    async def send_hr_digest(hr_email: str, job_title: str, total_screened: int, top_candidate: str, top_score: float) -> bool:
        template = Template(HR_DIGEST_TEMPLATE)
        html = template.render(job_title=job_title, total_screened=total_screened, top_candidate=top_candidate, top_score=top_score)
        return await EmailService.send_email(hr_email, f"Batch Screening Digest: {job_title}", html)
