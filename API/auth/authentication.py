from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import DbUsers
from db.hashing import Hash
from auth.oauth2 import create_access_token



router = APIRouter(
    tags = ['authentication']
)


@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(DbUsers).filter(DbUsers.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials')
    if user.password != request.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect password')
    
    # if not Hash.verify(user.password, request.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail='Incorrect password')
    
    access_token = create_access_token(data={'email':user.email})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        # 'user_id': user.id,
        # 'email': user.email,
        'user': {
            'name':user.name,
            'surname':user.surname,
            'id':user.id,
            'email':user.email,
            'image_url':user.image_url,
            'access_level':user.access_level
        }
    }
