from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import Reaction
from app.schemas import Reaction as ReactionSchema, ReactionCreate

router = APIRouter()

@router.get("/posts/{post_id}/reactions", response_model=list[ReactionSchema])
async def read_reactions(post_id: int, db: Session = Depends(get_db)):
    reactions = db.query(Reaction).filter(Reaction.post_id == post_id).all()
    return reactions

@router.post("/posts/{post_id}/reactions", response_model=ReactionSchema)
async def create_reaction(
    post_id: int,
    reaction: ReactionCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user already reacted to this post
    existing_reaction = db.query(Reaction).filter(
        Reaction.post_id == post_id,
        Reaction.user_id == current_user.id
    ).first()
    
    if existing_reaction:
        # Update existing reaction
        existing_reaction.type = reaction.type
        db.commit()
        db.refresh(existing_reaction)
        return existing_reaction
    else:
        # Create new reaction
        db_reaction = Reaction(
            post_id=post_id,
            user_id=current_user.id,
            type=reaction.type
        )
        db.add(db_reaction)
        db.commit()
        db.refresh(db_reaction)
        return db_reaction

@router.delete("/posts/{post_id}/reactions")
async def delete_reaction(
    post_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reaction = db.query(Reaction).filter(
        Reaction.post_id == post_id,
        Reaction.user_id == current_user.id
    ).first()
    
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    
    db.delete(reaction)
    db.commit()
    return {"message": "Reaction deleted"}