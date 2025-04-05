from server.extensions import db
from server.config import BAN_INTERVAL
from server.config import DATE_FMT
from server.models.Users import BANNED_USERS
from datetime import datetime, timedelta
from sqlalchemy import Enum
import enum


class LockoutPeriod(enum.Enum):
    """
    Lockout Period provides the ban increments per offense
    """

    FIRST = timedelta(hours=1)
    SECOND = timedelta(days=1)
    THIRD = timedelta(days=7)
    FOURTH = timedelta(days=30)
    FIFTH = "PERMANENT"

    @staticmethod
    def get_ban(failed_login: int) -> timedelta:
        ban_map = {
            1: LockoutPeriod.FIRST.value,
            2: LockoutPeriod.SECOND.value,
            3: LockoutPeriod.THIRD.value,
            4: LockoutPeriod.FOURTH.value,
            5: LockoutPeriod.FIFTH.value,
        }
        return ban_map[failed_login]


class ATTEMPTS(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(
        db.String(40), db.ForeignKey("users.uuid"), unique=True, nullable=False
    )
    failed_logins = db.Column(db.Integer, nullable=False, default=0)
    lockout_until = db.Column(db.String(30), nullable=True)

    def reset_attempts(self) -> None:
        """
        Resets the attempts of users whenever succesful login or overwrite manually
        """
        self.failed_logins = 0
        self.lockout_until = None

    def increment_attempt(self) -> dict:
        """
        Increments internal count of failed login attempts

        """
        self.failed_logins += 1

        if self.failed_logins > 0 and self.failed_logins % BAN_INTERVAL == 0:
            offense = self.failed_logins // BAN_INTERVAL
            ban = LockoutPeriod.get_ban(offense)

            if isinstance(ban, timedelta):
                self.lockout_until = datetime.utcnow() + ban
            else:
                self.lockout_until = None  # or set a 'permanent' flag
                banned_user = BANNED_USERS(
                    uuid=self.uuid,
                    reason="Max Attempts Reached",
                    banned_at=datetime.today().strftime(DATE_FMT),
                )
                db.session.add(banned_user)
                db.session.commit()

            return {
                "failed login attempts": self.failed_logins,
                "ban": self.lockout_until or "Permanent",
            }

        return {
            "failed login attempts": self.failed_logins,
            "remaining attempts": BAN_INTERVAL - (self.failed_logins % BAN_INTERVAL),
        }

    def check_valid(self) -> bool:
        """
        Checks for banned users
        """
        if self.lockout_until:
            if self.lockout_until == "PERMANENT":
                return False
            try:
                lockout_time = datetime.strptime(self.lockout_until, DATE_FMT)
                return datetime.today() >= lockout_time
            except ValueError:
                return False
        return True

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
