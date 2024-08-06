# qRaphael - Advanced Personal AI Assistant

<!-- align center -->
[![License](https://img.shields.io/github/license/Into-The-Grey/qRaphael)](https://github.com/Into-The-Grey/qRaphael/blob/main/LICENSE)

[![CodeQL](https://github.com/Into-The-Grey/qRaphael/actions/workflows/codeql.yml/badge.svg)](https://github.com/Into-The-Grey/qRaphael/actions/workflows/codeql.yml)

[![GitHub issues](https://img.shields.io/github/issues/Into-The-Grey/qRaphael)](https://github.com/Into-The-Grey/qRaphael/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Into-The-Grey/qRaphael)](https://github.com/Into-The-Grey/qRaphael/pulls)

[![GitHub contributors](https://img.shields.io/github/contributors/Into-The-Grey/qRaphael)](https://github.com/Into-The-Grey/qRaphael/graphs/contributors)
[![GitHub forks](https://img.shields.io/github/forks/Into-The-Grey/qRaphael)](https://github.com/Into-The-Grey/qRaphael/network/members)
[![GitHub stars](https://img.shields.io/github/stars/Into-The-Grey/qRaphael)](https://github.com/Into-The-Grey/qRaphael/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/Into-The-Grey/qRaphael)](https://github.com/Into-The-Grey/qRaphael/watchers)

[![GitHub last commit](https://img.shields.io/github/last-commit/Into-The-Grey/qRaphael)](https://github.com/Into-The-Grey/qRaphael/commits/main)
</p>

## Introduction

Welcome to the qRaphael project! This is an advanced personal AI assistant designed to push the boundaries of AI capabilities in natural language processing and understanding. The qRaphael model is based on the latest AI models and technologies, aiming to provide personalized and intelligent assistance.

## Table of Contents

- [qRaphael - Advanced Personal AI Assistant](#qraphael---advanced-personal-ai-assistant)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Features](#features)
  - [Database Schema](#database-schema)
    - [Users Table](#users-table)
    - [User Details Table](#user-details-table)
    - [User Preferences Table](#user-preferences-table)
    - [User Memory Table](#user-memory-table)
    - [Medical Information Tables](#medical-information-tables)
    - [Financial Information Tables](#financial-information-tables)
    - [Professional Information Table](#professional-information-table)
    - [Educational Information Table](#educational-information-table)
    - [Preferences and Interests Table](#preferences-and-interests-table)
    - [Social Connections Table](#social-connections-table)
    - [Security Information Table](#security-information-table)
    - [Miscellaneous Information Table](#miscellaneous-information-table)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Project Structure

The repository is organized as follows:

    qRaphael/
    ├── data/
    ├── src/
    ├── notebooks/
    ├── scripts/
    ├── models/
    │   └── qraphael/
    ├── tests/
    ├── requirements.txt
    └── README.md

- **data/**: Directory for storing datasets.
- **src/**: Pre-trained and fine-tuned models.
- **notebooks/**: Jupyter notebooks for experimentation and analysis.
- **scripts/**: Utility scripts for data processing, model training, etc.
- **models/qraphael/**: Core library code.
- **tests/**: Unit and integration tests.
- **requirements.txt**: Python dependencies.
- **README.md**: Project documentation.

## Installation

To get started with the qRaphael project, follow these steps:

1. **Clone the repository:**

        ```bash
        git clone https://github.com/yourusername/qRaphael.git
        cd qRaphael
        ```

2. **Set up a virtual environment:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. **Install dependencies:**

        ```bash
        pip install -r requirements.txt
        ```

## Usage

Detailed usage instructions will be added as the project develops. For now, you can start by exploring the Jupyter notebooks in the `notebooks/` directory and running the example scripts in `scripts/`.

## Features

- **Personalized Responses**: qRaphael tailors its responses based on user-specific data.
- **Memory Storage**: Stores detailed conversation history and user information.
- **Interactive Capabilities**: Can answer questions about its own identity and capabilities, provide suggestions, and adapt based on user preferences.
- **Scalable Data Management**: Uses PostgreSQL to manage and retrieve user data efficiently.
- **Dynamic User Interaction**: Adjusts its responses and interactions based on the user's inputs and stored data.

## Database Schema

The database schema for managing user data in PostgreSQL includes several tables to store different types of user information.

### Users Table

    ```sql
    CREATE TABLE users (
        user_id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(50),
        birthday DATE
    );
    ```

### User Details Table

    ```sql
    CREATE TABLE user_details (
        detail_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        detail_type VARCHAR(255),
        detail_value TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### User Preferences Table

    ```sql
    CREATE TABLE user_preferences (
        preference_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        preference_type VARCHAR(255),
        preference_value TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### User Memory Table

    ```sql
    CREATE TABLE user_memory (
        memory_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        memory_text TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### Medical Information Tables

    ```sql
    CREATE TABLE medical_conditions (
        condition_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        condition_name VARCHAR(255),
        diagnosis_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE medications (
        medication_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        medication_name VARCHAR(255),
        dosage VARCHAR(255),
        start_date DATE,
        end_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE immunizations (
        immunization_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        immunization_name VARCHAR(255),
        immunization_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE doctor_visits (
        visit_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        doctor_name VARCHAR(255),
        visit_date DATE,
        reason TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE insurance_info (
        insurance_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        provider_name VARCHAR(255),
        policy_number VARCHAR(255),
        coverage_details TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE health_metrics (
        metric_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        metric_type VARCHAR(255),
        metric_value VARCHAR(255),
        metric_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### Financial Information Tables

    ```sql
    CREATE TABLE investments (
        investment_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        investment_type VARCHAR(255),
        amount DECIMAL(15, 2),
        start_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE retirement_accounts (
        account_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        account_type VARCHAR(255),
        balance DECIMAL(15, 2),
        last_contribution_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE tax_information (
        tax_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        tax_year INT,
        tax_amount DECIMAL(15, 2),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE expense_tracking (
        expense_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        expense_type VARCHAR(255),
        amount DECIMAL(15, 2),
        expense_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE cards (
        card_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        card_type VARCHAR(255),
        card_number VARCHAR(255),
        expiration_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE bank_accounts (
        account_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        account_type VARCHAR(255),
        balance DECIMAL(15, 2),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE loans (
        loan_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        loan_type VARCHAR(255),
        loan_amount DECIMAL(15, 2),
        loan_start_date DATE,
        loan_end_date DATE,
        FOREIGN KEY (user_id) REFERENCES users

    (user_id)
    );

    CREATE TABLE salaries (
        salary_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        salary_amount DECIMAL(15, 2),
        pay_frequency VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE debts (
        debt_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        debt_type VARCHAR(255),
        debt_amount DECIMAL(15, 2),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### Professional Information Table

    ```sql
    CREATE TABLE professional_info (
        professional_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        job_title VARCHAR(255),
        company_name VARCHAR(255),
        start_date DATE,
        end_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### Educational Information Table

    ```sql
    CREATE TABLE educational_data (
        education_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        institution_name VARCHAR(255),
        degree VARCHAR(255),
        field_of_study VARCHAR(255),
        graduation_year INT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### Preferences and Interests Table

    ```sql
    CREATE TABLE preferences_interests (
        preference_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        preference_name VARCHAR(255),
        preference_value TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### Social Connections Table

    ```sql
    CREATE TABLE social_connections (
        connection_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        connection_name VARCHAR(255),
        relationship VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### Security Information Table

    ```sql
    CREATE TABLE security_info (
        security_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        security_question VARCHAR(255),
        security_answer VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

### Miscellaneous Information Table

    ```sql
    CREATE TABLE miscellaneous_info (
        info_id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        info_type VARCHAR(255),
        info_value TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

## Contributing

We welcome contributions from the community! Please fork the repository and create a pull request with your changes. Make sure to follow the coding guidelines and run tests before submitting your pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries or feedback, please contact [ncacord@protonmail.com](mailto:ncacord@protonmail.com).

---
[Back to top](#qraphael---advanced-personal-ai-assistant)

---
