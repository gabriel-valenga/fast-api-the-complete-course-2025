from ..routers.todos import get_db, get_current_user
from ..main import app

app.dependency_overrides[get_db] = override_get_db 
app.dependency_overrides[get_current_user] = override_get_current_user  