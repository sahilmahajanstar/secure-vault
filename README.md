# secure-vault
Secret File transfer platform

Frontend app runs on https://localhost:3000

Backend app runs on https://localhost:8000

### 1. Edit .env file in backend/.env
change variable to receive email to mail. Follow steps to generate app passward for your email https://support.google.com/mail/answer/185833?hl=en

- `EMAIL_HOST_USER=your email`
- `EMAIL_HOST_PASSWORD=your app password`

### 2. Run command `docker compose up`
Once app run ./setup.bash will be executed for backend application which is located in backend/setup.bash

### 3. create_superuser.py contain 4 users which created default you can refer for login purpose 1 is super user and 3 is normal user
* `username: admin and password: Admin@123`
* `username: testuser and passward: test@123`
* `username: testuser2 and passward: test@123`
* `username: testuser3 and passward: test@123`

### 3. login into application https://localhost:3000/users/login

### 4. For otp verification connect databse to sqlite which is located at backend/data/db.sqlite3. you can refer SQL query below
`select * from otp_email_emaildevice oee where email = 'email'` change email for specified 
