# **Welcome to DegreeFlow 📚 – Your AI-Powered College Schedule Builder/Sidekick\!**

Congratulations, Emory student\! You have found DegreeFlow, the AI-powered app that builds your college semester for you without worry\! It utilizes all your taken courses, your major, and, most importantly, your preferences to build your semester schedule perfectly so that you don’t lose your sanity (or miss out on Taco Tuesdays 🌮).

## **The setup of the app includes the setup of its main technologies: React.js, FastAPI, Python, and MongoDB.**

First of all download our app from GitHub by pulling through the command line or installing it from [https://github.com/jacky030214/Emory-CS-370](https://github.com/jacky030214/Emory-CS-370) and cd into the project folder:  
```
git clone https://github.com/jacky030214/Emory-CS-370.git  
cd Emory-CS-370
```

Then install python 3.13 for the backend using the [python installer](https://www.python.org/downloads/) (any OS) or the following command (mac only) with Homebrew installed from [https://brew.sh/](https://brew.sh/).  
```
brew install python@3.13
```

Next, install FastAPI (and its supporting package uvicorn), the link between the frontend and the backend:  
```
pip install fastapi uvicorn
```

Now we will install React JS \+ Vite for the frontend using the following instructions for React: [https://www.geeksforgeeks.org/how-to-install-reactjs-on-macos/](https://www.geeksforgeeks.org/how-to-install-reactjs-on-macos/) and the following command for Vite:  
```
npm install \--save-dev vite
```

Finally you need to install MongoDB (use [this link](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/) for windows and the instructions below for mac/linux) and then the MongoDB Compass app and set up a database called “my\_database”:  
```
brew tap mongodb/brew  
brew install mongodb-community  
brew services start mongodb/brew/mongodb-community  
# install Compass from [www.mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass)
```

## **Great\! Now you have installed all technologies needed for DegreeFlow. Now it's time to set them up\!**

Install the backend’s dependencies by using the project’s requirements.py file and pip:  
```
pip install \-r requirements.txt
```

Collect the data files from the github code folder and import them as separate collections under “my\_database” from the following paths and using the specified collection names:

| Collection Name | Path |
| :---- | :---- |
| Class | backend/app/Data/class.csv AND web\_scraping/course\_data/all\_courses.csv |
| all\_courses | web\_scraping/course\_data/all\_courses.csv |
| fall\_2025 | web\_scraping/course\_data/all\_fall\_2025\_courses.csv |
| spring\_2025 | web\_scraping/course\_data/all\_spring\_2025\_courses.csv |
| rmp\_ratings | web\_scraping/course\_data/professor\_ratings.csv |
| Major\_Req | backend/app/Data/emory\_all\_majors\_combined \- emory\_all\_majors\_combined.csv.csv |

To see how this data was gathered please explore the web\_scraping folder and its two main scripts: web\_scraper.py and rmp\_scraper.py.

## **Congrats, all the setup is now complete and the app is ready to be run.**

To run the app all you need to do now is start the MongoDB database from the Compass app by pressing “Connect” (localhost:27017) start FastAPI, and then start Vite \+ React in separate terminals:  
```
fastapi dev backend/app/main.py # http://127.0.0.1:8000   
# OR uvicorn main:app --reload from the backend/app folder  
npm run dev # localhost:5173
```

Go to [http://localhost:5173/](http://localhost:5173/) to see the running app!

## **Using the app**

To use DegreeFlow you need to create an account or log in. You can click on Google, Apple, etc. login icons to avoid having to create an account.

In the Class Search tab you can search for any Emory course using its course code (prefix \+ number).

Under the Major Schedule tab you can select your major and your starting semester \+ year and click on “View Schedule” to generate a schedule based off your major requirements.

Then, under the GER Schedule tab you can select similar options to generate a schedule that takes into consideration your major and the college’s GER requirements.

Additionally under the Personalized Schedule and Top Course Reccomendations tab you could insert your desired course attributes and a description of the content you would like to learn to get an AI-powered schedule and course recommendations. *This is a feature we were not able to connect with the frontend in time and thus is only available for use through the terminal, using the following instructions:*  
```
cd backend/app/Functions  
python generate\_personalized\_schedule.py
```

Finally, under the Future Schedule tab you can enter your major and starting year \+ semester and specify taken courses by entering their course codes one by one to get a generated schedule that entails major requirements and also takes into consideration your taken courses.
