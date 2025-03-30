
from server import db
from server.config import DATE_FMT
from sqlalchemy import Enum
import enum
from datetime import datetime,timedelta


class Tiers(enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    
    @staticmethod
    def get_expiration( tier:str) -> timedelta:
        expiration_map = {
            Tiers.FREE.value : None,
            Tiers.PRO.value  : timedelta(days=365),
            Tiers.ENTERPRISE.value : timedelta(days=365)
        }
        return expiration_map[tier]
    
    @staticmethod
    def get_tier_rank(tier:str) -> int:
        tier_map = {
            Tiers.FREE.value : 0,
            Tiers.PRO.value  : 1,
            Tiers.ENTERPRISE.value : 2
        }
        return tier_map[tier]

class SUBSCRIPTIONS(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    uuid = db.Column(db.String(40), db.ForeignKey('users.uuid'), unique=True, nullable=False)
    tier = db.Column(Enum(Tiers), nullable= False ,default = Tiers.FREE)
    expiration = db.Column(db.String(40), nullable=True, default=None )

    def __init__(self, uuid:str) -> None:
        self.uuid = uuid
        self.tier = Tiers.FREE

    def reset_to_default(self) -> None:
        self.tier = Tiers.FREE

    def subscribe_tier(self,tier:str) -> dict:
        
        if tier not in [Tiers.FREE.value,
                        Tiers.PRO.value,
                        Tiers.ENTERPRISE.value]:
            
            return {'error': 'Invalid Tier'}
        
        free_member = self.tier == Tiers.FREE
        expired_membership = datetime.strptime(self.expiration,DATE_FMT) < datetime.today()

        if free_member or expired_membership:
            self.tier = tier
            self.expiration = datetime.strftime(datetime.today() + Tiers.get_expiration(self.tier),
                                                DATE_FMT)

            return {'success': f'{self.uuid} is now subscribed to {self.tier}',
                    'expiration': self.expiration}
        return {'error': f'{self.uuid} is still subscribed with a {self.tier} license'}



        

  


