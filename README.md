# File Uploader API

This application provides a backend solution for uploading, managing, and sharing files, as well as managing users. It offers endpoints for user registration, authentication, user profile management, file upload, listing user files, listing all files (admin only), file analytics, file sharing, updating files, and deleting files.

---

## Table of Contents

- [File Uploader API](#file-uploader-api)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Features](#features)
  - [Installation](#installation)
    - [Running Locally](#running-locally)
      - [Using Docker Compose](#using-docker-compose)
      - [Using Virtual Environment](#using-virtual-environment)
      - [Configuration](#configuration)
        - [Generating the Secret Key](#generating-the-secret-key)
        - [Usage](#usage)
    - [Contributing](#contributing)
    - [License](#license)

---

## Prerequisites

Before you start, make sure you have the following prerequisites:

- **MySQL:** Install MySQL on your machine. You can download and install it from the [official MySQL website](https://www.mysql.com/downloads/).

- **Python:** Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/).

- **Docker:** Make sure Docker is installed on your machine. You can download and install it from the [official Docker website](https://www.docker.com/get-started).

---

## Features

**User Management**:

- User registration with strong password validation.
- User authentication with JWT token generation.
- Role-based access control (customers and admin).
- User profile retrieval and update.

**File Management:**

- File upload with validation for file types and size.
- Listing user files with pagination, search, and filtering.
- Listing all files (admin only) with pagination, search, and filtering.
- File analytics to calculate the total number and size of files for a specific user.
- File sharing with unique links.
- Downloading files.
- Updating file details.
- Deleting files.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

### Running Locally

#### Using Docker Compose

1. Create a .env file in the root directory of the project and define the following variables:

```bash
SECRET_KEY=...
ALGORITHM=...
ACCESS_TOKEN_EXPIRE_MINUTES=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=...
DB_NAME=...
BASE_URL=...
```

2. Start the application using Docker Compose:

```bash
docker-compose up --build
```

3. Navigate to `http://localhost:8000/docs` in your browser to access the Swagger UI for testing the API endpoints.

#### Using Virtual Environment

1. Install dependencies:

```bash
python3.9 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

---

#### Configuration

##### Generating the Secret Key

The SECRET variable is used for authentication and security purposes within the application. To generate a secure secret key, you can use Python's secrets module to generate a random hexadecimal string. Here's an example of how you can generate a secret key:

```python

import secrets

secret_key = secrets.token_hex(10)
print("Generated Secret Key:", secret_key)
```

---

##### Usage

Start the FastAPI server:

    uvicorn app.main:app --reload

    Navigate to http://localhost:8000/docs in your browser to access the Swagger UI for testing the API endpoints.

---

### Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.

2. Make your changes and test thoroughly.

3. Ensure your code follows the existing coding style.

4. Create a pull request with a clear description of your changes.

---

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/odoh-tc/repo/blob/main/LICENSE) file for details.

---
