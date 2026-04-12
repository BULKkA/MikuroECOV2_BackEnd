from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CaptchaRequest
from app.schemas import CaptchaVerify, CaptchaResponse
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/verify", response_model=CaptchaResponse)
async def verify_captcha(
    captcha: CaptchaVerify,
    db: Session = Depends(get_db)
):
    # In a real implementation, you would verify with a captcha service
    # For now, we'll just check if the token exists in our database
    captcha_request = db.query(CaptchaRequest).filter(
        CaptchaRequest.token == captcha.token
    ).first()
    
    if not captcha_request:
        return {"verified": False}
    
    # Mark as verified
    captcha_request.verified_at = datetime.utcnow()
    db.commit()
    
    return {"verified": True}

# Helper function to generate captcha token
def generate_captcha_token(user_ip: str, db: Session):
    token = str(uuid.uuid4())
    captcha_request = CaptchaRequest(token=token, user_ip=user_ip)
    db.add(captcha_request)
    db.commit()
    return token