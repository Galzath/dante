from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import json
import asyncio
from sse_starlette.sse import EventSourceResponse
import httpx

from . import auth, database, models, classifier

app = FastAPI()

# A simple in-memory cache for SSE clients
sse_clients = []

@app.on_event("startup")
def on_startup():
    database.init_db()
    # This is where you might add some default rules to the database
    # For now, we'll use the sample rules from the classifier
    db = next(database.get_db())
    if not database.get_rules(db):
        sample_rules = classifier.get_sample_rules()
        for rule in sample_rules:
            db_rule = models.Rule(category=rule.category, field=rule.field, condition=rule.condition, value=rule.value)
            db.add(db_rule)
        db.commit()


async def send_sse_update():
    db = next(database.get_db())
    rules = database.get_rules(db)
    categories = {rule.category: 0 for rule in rules}
    unread_emails = db.query(models.UnreadEmail).all()
    for email in unread_emails:
        if email.category in categories:
            categories[email.category] += 1

    for client in sse_clients:
        await client.put(json.dumps(categories))

async def process_notification(notification, db: Session):
    user = database.get_user(db, email="user@example.com") # Placeholder for actual user management
    if not user:
        return

    token_data = json.loads(database.decrypt_token(user.encrypted_token))
    access_token = token_data.get("access_token")

    message_id = notification['resourceData']['id']

    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{auth.GRAPH_API_ENDPOINT}/me/messages/{message_id}", headers=headers)
        if response.status_code == 200:
            email_data = response.json()
            rules = database.get_rules(db)
            category = classifier.classify_email(email_data, rules)
            if category:
                database.add_unread_email(db, message_id=message_id, category=category)
                await send_sse_update()

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    if 'validationToken' in (body := await request.json()):
        return body['validationToken']

    for notification in body.get('value', []):
        background_tasks.add_task(process_notification, notification, db)

    return {"status": "success"}

@app.get("/dashboard-stream")
async def dashboard_stream():
    queue = asyncio.Queue()
    sse_clients.append(queue)

    async def event_generator():
        try:
            while True:
                data = await queue.get()
                yield {"event": "update", "data": data}
        except asyncio.CancelledError:
            sse_clients.remove(queue)

    # Send initial state
    await send_sse_update()

    return EventSourceResponse(event_generator())

@app.post("/mark-as-read")
async def mark_as_read(data: dict, db: Session = Depends(database.get_db)):
    category = data.get("category")
    if not category:
        raise HTTPException(status_code=400, detail="Category not provided.")

    user = database.get_user(db, email="user@example.com") # Placeholder
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    token_data = json.loads(database.decrypt_token(user.encrypted_token))
    access_token = token_data.get("access_token")

    unread_emails = database.get_unread_emails_by_category(db, category)

    patch_body = {"isRead": True}
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        for email in unread_emails:
            await client.patch(f"{auth.GRAPH_API_ENDPOINT}/me/messages/{email.message_id}", headers=headers, json=patch_body)

    database.delete_unread_emails_by_category(db, category)
    await send_sse_update()

    return {"status": "success"}

@app.get("/login")
def login():
    return RedirectResponse(url=auth.get_auth_url())

@app.get("/callback")
def callback(request: Request, db: Session = Depends(database.get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found.")

    token_data = auth.get_token_from_code(code)
    if "error" in token_data:
        raise HTTPException(status_code=400, detail=token_data.get("error_description"))

    account_info = token_data.get('id_token_claims')
    if not account_info or 'preferred_username' not in account_info:
        user_email = "user@example.com"
    else:
        user_email = account_info['preferred_username']

    encrypted_token = database.encrypt_token(json.dumps(token_data))

    user = database.get_user(db, email=user_email)
    if not user:
        database.create_user(db, email=user_email, encrypted_token=encrypted_token)
    else:
        user.encrypted_token = encrypted_token
        db.commit()

    response = RedirectResponse(url="/")
    response.set_cookie(key="dante-auth", value="true") # Simple cookie to indicate auth
    return response
