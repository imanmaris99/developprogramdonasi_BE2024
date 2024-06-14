# Program Donasi API (- BackEnd Section)

Program Donasi is a backend application built using Flask to help manage users, contact_us, program donasi, donatur and donasi in support of the DevelopProgramDonasi campaign.

## Features

- **User**: Register, log in, update, and delete users.
- **Contact_us**: Create messages and get list messages.
- **Program Donasi**: Add, update, and delete programs.
- **Donatur**: Add, view, update, and delete donature.
- **Donasi**: Add, view, update, and delete donasi.
- **Authentication**: Uses JWT for user authentication.



<h4>Web Display and Menu Flow</h4>
<h4>Frontend application for which I tried to design the website planning layout in Figma.</h4>
   <img  src="/documentation/Content Planning.png">
    <p>Here is a screenshot of the application:</p>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
        <p><b>Login and Register Menu</b></p>
        <img src="/documentation/Component 2 (1).png" alt="Component register">
        <p><b>About and Contact Menu</b></p>
        <img src="/documentation/Component about.png" alt="Component about">
         <p><b>Program and Donate Menu</b></p>
        <img src="/documentation/Componenet donate.png" alt="Component donate">
    </div>

#
<h4>Web Database and Relationship Flow</h4>
<h4>I tried to design the website planning layout in Figma.</h4>
    <p>Here is a screenshot of the relationship flow:</p>
<div align="center">
   <img width="500" src="/documentation/Program Donasi Database.png">
</div>

#

## My API

### Overview

This API allows users to interact with our service to manage their profiles, authenticate, and more.

### Base URL

The base URL for the API is: https://developprogramdonasi-be-2024.vercel.app



### Endpoints

#### User Profile

- **GET /profile**: Retrieve the profile of the currently logged-in user.
  - Requires a valid JWT token.
  - Returns the user’s ID, email, name, role, and timestamps.

For more detailed information on API endpoints and their usage, please refer to our [API Documentation](https://documenter.getpostman.com/view/32137902/2sA3QqgspG).

### Setup and Installation

To set up the project locally, follow these steps:

1. Clone the repository.
2. Install the dependencies using Poetry.
3. Configure the environment variables.
4. Run the application.

#### Steps to Run:

1. Ensure your environment variables are set correctly. Example of `DATABASE_URI` for MySQL:
   ```plaintext
   DATABASE_URI=mysql+pymysql://user:password@host:port/dbname
   ```

2. Install the required packages using "poetry add":
   ```bash
   poetry add flask sqlalchemy pymysql
   ```

3. Run your Flask application:
   ```bash
   poetry run flask --app app run
   ```

By following these steps, you should be able to resolve successfully connect to your MySQL database using SQLAlchemy in your Flask application.


#### Connecting to Aiven MySQL

- Configure your database settings in the `.env` file:
  ```plaintext
  DB_NAME=your_database_name
  DB_USER=your_user
  DB_PASSWORD=your_password
  DB_HOST=your_host
  DB_PORT=your_port
  DATABASE_URI=mysql://your_user:your_password@your_host:your_port/your_database_name

- Connect MySQL Workbench to Aiven MySQL using the provided connection details.
...

## License

This project is licensed under the MIT License - see the LICENSE file for details.  

    By following these steps, you can integrate Aiven for MySQL with your Flask application and manage your database using MySQL Workbench. The provided code snippets and documentation structure ensure that your project is well-organized and easy to set up.

... 
#

<p align="center"><b>still under development by Iman</b></p>
<p align="center"><i>copyright &copy; 2024 by Iman</i></p>
