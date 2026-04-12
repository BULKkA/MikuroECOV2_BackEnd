from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import Comment
from app.schemas import Comment as CommentSchema, CommentCreate, CommentUpdate

router = APIRouter()

@router.get("/posts/{post_id}/comments", response_model=list[CommentSchema])
async def read_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@router.post("/posts/{post_id}/comments", response_model=CommentSchema)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_comment = Comment(
        post_id=post_id,
        author_id=current_user.id,
        body=comment.body,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.put("/{comment_id}", response_model=CommentSchema)
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.author_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for key, value in comment_update.dict(exclude_unset=True).items():
        setattr(comment, key, value)
    
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.author_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}