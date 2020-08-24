# dynamic_db

1.Clone from the git repository

	-url - https://github.com/upadhyayanshul/dynamic_db.git

At the path dynamic_db/sysdemo/mysite/ in repository [I have just created a sample of django project setup ]

main [mysite] contains following folders ==>

installation requirements : 
	-virtualenv is used to manage Python packages for different projects with version amangement.
	-below commands  will create a virtual Python installation in the env folder.

COMMANDS
	-python -m pip install --user virtualenv [install virtual env]
	-python -m virtualenv env (for windows)

Activation of virtualenv
	-Everytime we need to use application we activate virtual env and perform action on it

COMMANDs:
	- .\env\Scripts\activate (windows)
	- pip install -r requirements.txt (to install all the dependencies with version mentioned in requirements.txt file in env)
	

a) CONFIG - which contains the configuration of the production and development.

	-1.We have setup the debug and secrete variables env in config folder for both development and production 

	-2. We can define the databse env varibales for the different environments to increase the functionality independently.
	but for the demo purpose i have define common setting for such environments

	-3.To run as developement server (need to define DJANGO_DEVELOPMENT=True) in the os env otherwise application will run in production


COMMANDS -
	windows machine
	-set DJANGO_DEVELOPMENT=True

	linux machine
	-export DJANGO_DEVELOPMENT=True

Define other dependent settings in corresponding env files in config folder [above points]

b) SETTING - which contains development.py,production.py and base.py ==>

	-1.base contains the common settings for both development and production
	-2.production.py contains the production constants (settings) and dependency 
	-3.development.py contains the development constants (settings) and dependency 

c) DATABASES - 

	''' WE HAVE DEFINED MULTIPLE DATABASES SETTING
	    == PGSQL==
	        DATABASE_1,DATABASE_2,DB_DEFAULT
	    == MYSQL==
	        DATABASE_3,DATABASE_4,DATABASE_5
	'''
so just create the databases before using for the application with your credentioals

d) DATABASE TABLES [for now we have not restricted the table , we can restrict to migrate in the env setup defined above]

	-1. For now we are migrating everything for each database as we are using the same installed variable in different setup

COMMANDS [use table create commands]  - 
	-1.python manage.py makemigrations
	-2.python manage.py migrate
	-3.python manage.py migrate --database=database_1
	-4.python manage.py migrate --database=database_2
	-5.python manage.py migrate --database=database_3
	-6.python manage.py migrate --database=database_4
	-7.python manage.py migrate --database=database_5

Check all the tables migrated successfully in the databases mentioned in command above

e) Default admin User:
	- System require a default admin user to proceed next in system
	- Just follow the setps mentioned below to initial the application setup (use django admin panel)

DEFAULT Admin Command
	- python manage.py createsuperuser (enter credentials)
		username-systangoadmin
		password-systangoadmin@123
		email-systangoadmin@mailinator.com
	- Login to admin panel of django (http://127.0.0.1:8000/admin/)
	- update the above created user with details of user in profile extend  (set all credentials is_staff,is_superuser,is_active to true)
	- Try To login with username and password in the dyanmic_db projrct application will render the dashboard (on success)


2.Define urls of site

	-1.Main project directory [mysite] contains the url for app and admin

	-2.For the django task we have just named the app as [polls]

Demo Appname  = polls

a).Root url config 
	/polls/ ==> points to polls app
	/admin/ ==> points to admin app 


3.App[For illustration we named the application as polls]
	- 1.Polls app contains the views,urls,templates,templatetages,helper middleware etc..(as per requirement)

4.Models
	-1. USER
	-2. PROFILE
	-3. PRODUCT

5.App endpoints:

	-1./polls/home/
	Description - We have login option as admin or as user ,also has a small description about task assigned

	-2./polls/login/
	Description -Allows the active users to login into site with correct credentials

	-3./polls/logout/
	Description -Clear the user session and logout from the account of the user

	-4./polls/dashboard/
	Description -Allows to show all the database  with their type as a link to see
				-include the logout,login user detail,profile,signup,permission table,product options

	-5./polls/products/
	Description - Render the product form with the helper texts

	-6./polls/product/db_name/
	Description - To add product with the databse option by the user

	-7./polls/permission_table/
	Description - contains list of all the user with the database access allowed option (on for admin)

	-8./polls/edit_permission/profile_id/
	Description - Admin can update the database permission by checking or unchecking the checkboxes in table

	-9./polls/show_db/db_name/
	Description - When clicking any of the database listing all the tables in sidebar with a default table data


	-10./polls/show_db/db_name/db_table/
	Description - one can see data from any table of the databse by clicking into table option

	-11./polls/forget_password/
	Description - Forget password email on forgetting password

	-12./polls/reset_password/uid/token
	Description - Check the reset  password link and render the template with basic details of user to reset password

	-13./polls/reset_password_confirm/
	Description - Once user request to password reset validate and response accordingly

	-14./polls/signup/
	Description -Opens the signup form with help text and the validations and email sending for verification

	-15./activate/uid/token
	Description -To track the user account to activate using the email

	-16.defult path to handle other paths

6.MutiUser model
	- As we are just using admin and user so using inbuilt auth model flag to identify the user
	- For more users we can make the role model seperatly to handle all condition 

7. Views
	- We just have used the functional view [we can define them in generic view as well]
	- We choosed function as database operation need more queries but it is possible with functional view

8. Login Requirement
	-Login,home,forget_password_reset_password,confirm_password such urls can be accessed without login 
	- dashboard and other sensitive data required login 

9. Permission restriction 
	- The permission and signup table is restricted to the user not who is not admin
	- For non admin userpermission of any user can be changed

10. Product description 
	- When we are creating a product choosing database product goes into relative database 
	- For example when i craete a product to database_1 then it is saved in that database 
	- For now i have not restricted the product details on user basis in the database 
	- I handle the condition on the database level 
	- We can extend the functionality by filter query for the product url in specific database to add restriction to see others products



