from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from app_user.schema import UserCreate, UserInfo
from app_user.model import User


router = APIRouter()


"""
接口：User 用户表增删改查

POST   /api/users            ->  create_user  ->  创建用户
GET    /api/users            ->  get_users    ->  获取所有用户
GET    /api/users/{user_id}  ->  get_user     ->  获取单个用户
PUT    /api/users/{user_id}  ->  update_user  ->  更新单个用户
DELETE /api/users/{user_id}  ->  delete_user  ->  删除单个用户
"""

# 新建用户
@router.post("/", response_model=UserInfo, name="新建用户")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return User.create(db, email=user.email, hashed_password=user.password + "fakefake")


# 获取所有用户
@router.get("/", response_model=List[UserInfo], name="获取所有用户")
async def get_users(db: Session = Depends(get_db)):
    return User.all(db)


# 通过id查询用户
@router.get("/{user_id}", response_model=Union[UserInfo, Any], name="查询用户 by user_id")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = User.get_or_404(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 通过id更改用户
@router.put("/{user_id}", name="更改用户 by user_id")
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return User.update_by(db, user_id, {"hashed_password": user.password, "email": "嘿嘿"})


# 通过id删除用户
@router.delete("/{user_id}", name="删除用户 by user_id")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    User.remove_by(db, id=user_id)
    return 0
