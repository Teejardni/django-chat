A quick test to see how django can be used for async chats

Run guide:
1. Clone repo
2. create venv 
3. pip install -r requirements.txt
4. cd chatig
5. python -m daphne -b 127.0.0.1 -p 8000 chatig.asgi:application