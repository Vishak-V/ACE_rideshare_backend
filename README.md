# ACE - Ridesharing App for College Students

ACE is a backend ridesharing application designed to help college students find and share rides with their peers. Built using Python FastAPI, ACE ensures a seamless and efficient experience for students looking to connect for carpooling or ridesharing within their campus community.

## Features

- **User Registration and Authentication**: Secure user sign-up and login processes with JWT-based authentication.
- **Verification to Ensure Safe Travel**: Only allow users who are a student to sign up.

## Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **APIs**: RESTful APIs built with FastAPI

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ACE.git
   cd ACE
   ```
2. Set up a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Set up the PostgreSQL database:

   Create a new PostgreSQL database.
   Update the database connection details in config.py or the environment variables. 
