from ninja import Schema
import datetime

class Error(Schema):
    message: str


class UserSchema(Schema):
    id: int
    username: str
    email: str  # Required, as per REQUIRED_FIELDS
    first_name: str | None = None
    last_name: str | None = None
    is_staff: bool
    is_active: bool
    date_joined: datetime.datetime  # or use datetime.datetime if you prefer


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema