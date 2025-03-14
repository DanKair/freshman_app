# University Freshman &amp; Applicant Guide App.
## A web & mobile app that:

✅ Guides applicants through the admission process with a step-by-step checklist. \
✅ Helps freshmen navigate campus, find resources, and connect with mentors.\
✅ Provides an interactive chatbot for FAQs about university life. \
✅ Notifies users about deadlines, events, and academic resources. \

### To install required dependenciese, use this command: 

```pip install -r requirements.txt```

## Installation & Get Started
### 1. Cloning the Repository
```
git clone https://github.com/DanKair/freshman_app.git
cd freshamn_app
```
### 2. Installation of dependencies
```
pip install -r requirements.txt
```

### 3. Environment Variable Configuration ( Copies the .env.sample content into .env)
```
cp .env.sample .env
```
### 4. Apply the migrations
**For Windows / MacOS users:**
```
python manage.py migrate
```
**For Linux users:**
```
python3 manage.py migrate
```
### 5. Run the server
```
python manage.py runserver
```
