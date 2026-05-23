to make init like "npm init -y" :
python -m venv venv

to run terminal based on venv :
source venv/Scripts/activate

to install like npm i :
pip install -r requirements.txt

to run server :
uvicorn app.main:app --reload

to extract the package used :
pip freeze > requirements.txt