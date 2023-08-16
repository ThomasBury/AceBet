# Let's import all the magical stuff we need!
from datetime import datetime, timedelta  # For handling time
from typing import Annotated  # For fancy type hints
from pathlib import Path  # For handling file paths

# Time for FastAPI to shine!
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)  # For authentication
from jose import JWTError, jwt  # For dealing with tokens
from passlib.context import CryptContext  # For password hashing
from pydantic import BaseModel  # For fancy data validation

# Importing the super cool prediction function
from acebet.api.predict_winner import make_prediction

# Let's have some secret sauce for encryption (shhh, it's a secret)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# Fasten your seatbelts, we're using the HS256 algorithm for tokens
ALGORITHM = "HS256"

# Tokens are like magical spells, but they last only for a short while (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Prepare a database of imaginary users, because we love imagination
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# Our secret token class to make life easier
class Token(BaseModel):
    access_token: str
    token_type: str


# Token data for the wise ones
class TokenData(BaseModel):
    username: str | None = None


# A user model that defines the heroes of our story
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# The secret agent version of a user
class UserInDB(User):
    hashed_password: str


# The oracle's predictions are in!
class PredictionRequest(BaseModel):
    p1_name: str
    p2_name: str
    date: str
    testing: bool = False


# And the answer is...
class PredictionResponse(BaseModel):
    player_name: str | None = None
    prob: float | None = None
    class_: int | None = None


# The secret code to lock and unlock passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# The VIP pass to enter with style
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Our superhero FastAPI app is here!
app = FastAPI()

# Now, let's define our superpowers (functions)


# The trusty password checker
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# The magical password hasher
def get_password_hash(password):
    return pwd_context.hash(password)


# The user detective
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# The secret agent
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# The token creator
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# The security guard checking your identity
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # Oops, who's that trying to sneak in?
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # The bearer of this token has a story to tell
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # The guardian checks the database of heroes
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# The gatekeeper checking your access rights
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# The authentication booth for the bold ones
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# The user profile display area
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


# The user's item collection
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


# The prediction
# async  to facilitate efficient handling of multiple operations
# happening simultaneously, enhancing the responsiveness and performance of the API.
# although the performance is not really important here
@app.post("/predict/", response_model=PredictionResponse)
async def predict_match_outcome(request: PredictionRequest):
    p1_name = request.p1_name
    p2_name = request.p2_name
    date = request.date
    testing = request.testing

    # The data and model paths are crucial for predictions
    if testing:
        data_file = (
            Path(__file__).resolve().parents[1] / "data" / "atp_sample_data.feather"
        )
        model_path = Path(__file__).resolve().parents[1] / "data"
    else:
        data_file = (
            Path(__file__).resolve().parents[3] / "data" / "atp_data_production.feather"
        )
        model_path = Path(__file__).resolve().parents[3]

    # Let's gaze into the future (predict using the make_prediction function)
    prob, class_, player_1 = make_prediction(
        data_file=data_file,
        model_path=model_path,
        p1_name=p1_name,
        p2_name=p2_name,
        date=date,
    )
    # Let's round off the probability for neatness
    prob = round((100 * prob[0]), 1)

    # The prediction is here, folks!
    return PredictionResponse(player_name=player_1, prob=prob, class_=class_)
