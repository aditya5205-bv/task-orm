from sqlalchemy import BigInteger, String, DateTime, Index
from sqlalchemy.orm import DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass

class UserData(Base):
    __tablename__ = 'user_data'
    
    user_id = mapped_column(BigInteger(), primary_key=True)
    
    username = mapped_column(String(20), nullable=False)
    
    user_email = mapped_column(String(320), nullable=False)
    
    user_password = mapped_column(String(256), nullable=False)
    
    created_at = mapped_column(DateTime)
    
    updated_at = mapped_column(DateTime)
    
    # Create index
    __table_args__ = (
        Index('username_idx', 'username'),
    )
    
    def __repr__(self):
        return f"<UserData(user_id={self.user_id}, username='{self.username}', email='{self.user_email}')>"