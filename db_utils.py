from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    BigInteger,
    Integer, 
    String, 
    Column, 
    Date,
)

Base = declarative_base()

# Creates user object to write a new row in database
class User(Base):
    __tablename__ = "users"

    id = Column("id", BigInteger, primary_key=True)
    language = Column("language", String)
    count_offers = Column("count_offers", Integer)
    created = Column("created", Date)

    def __init__(
            self, id: int, language: str,
            count_offers: int, created: str) -> None:
        
        self.id = id
        self.language = language
        self.count_offers = count_offers
        self.created = created

# Saves user in a database
def save_user(
    session: object,
    user_id: int, 
    language: str, 
    count_offers: int, 
    created: str) -> None:

    
    if session.query(User).filter(User.id == user_id).first() == None:

        user = User(
            id=user_id, language=language,
            count_offers=count_offers, created=created)

        session.add(user)
        session.commit()
    

# +1 after every post suggestion
def update_count_offers(session: object, id: int):
    user_data = session.query(User).filter(User.id == id).first()
    user_data.count_offers += 1
    return session.commit()

# returns the sum of all suggestions
def get_sum_of_all_count_offers(session: object) -> int:
    sum_of_all_offers = 0

    offers = session.query(User).filter(User.count_offers > 0).all()
    
    for i in offers:
        sum_of_all_offers += i.count_offers

    else:
        return sum_of_all_offers