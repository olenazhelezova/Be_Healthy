# **Be_Healthy**

#### **Video Demo:** <>

#### **Description:**

Using the **"Be healthy"** web application, the user can easily find out nutritional facts about any product, find recipes and keep his own food diary.
On **home.html**(**index.html**) page, the user can input one or more food products about which he wants to know the nutritional facts and get data on each indicated food product per 100 grams. Also, the user can specify the weight of the product and receive data from the conversion to the specified weight.
On **bmi.html** by entering body weight (in kilograms or pounds) and height (in centimeters or inches), the user can find out the body mass index and weight status.
On **recipes.html** the user can get up to ten recipes by entering the name of a dish or food name in the search field.
The user can register on **register.html** and log in on **login.html** to the web application. A logged-in user can keep his own food diary on **diary.html**.

#### **Component**:

This project contains next documents:

1. **app.py** runs the program.
2. **requirements.txt** contains Python modules needed for project.py.
3. **README.md** is a Markdown file with instructions.
4. **application** folder contains:
   - **routes.py** contains the main code for executing the program.
   - in **static** folder images for **recipy.html**, **styles.css** and JS code;
   - **templates** conteins **includes** folder with templates for **footer** and **nav**, and templates for **apology.html**, **bmi.html**, **diary.html**, **index.html**, **layouut.html**, **login.html**, **recipes.html**,**register.html**;
   - **init.py** initializes application creating a Flask app instance.
   - **helpers.py** contains the declared functions necessary to execute the program.
   - **config.py.template** contains information about the keys needed to access the API.
   - **database.db** contains configuration for database.
   - **search.py** contains functions to perform data retrieval in the API.
