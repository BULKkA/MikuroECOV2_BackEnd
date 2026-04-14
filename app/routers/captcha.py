from fastapi import APIRouter
from app.schemas import CaptchaVerify, CaptchaResponse

router = APIRouter()

@router.post("/verify", response_model=CaptchaResponse)
async def verify_captcha(captcha: CaptchaVerify):
    # Captcha disabled — always return verified
    return {"verified": True}