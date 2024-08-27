
# Employee Management System API

## Overview

This repository contains the backend implementation for an employee management system using Django REST Framework (DRF). The API provides endpoints for managing employees and their associated reviews.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
   - [Employees](#employees)
   - [Reviews](#reviews)
4. [Data Models](#data-models)
5. [Authentication](#authentication)
6. [Error Handling](#error-handling)
7. [Contributing](#contributing)

## Installation

To set up the project locally:

1. Clone the repository:

   ```
   git clone https://github.com/pipthablack/employee-management-api.git
   cd employee-management-api
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```
   python manage.py migrate
   ```

5. Start the development server:

   ```
   python manage.py runserver
   ```

API-DOCUMENTATION: <https://documenter.getpostman.com/view/31639947/2sAXjGdZuS>

## Usage

### Employees

#### List Active Employees

GET `/api/employees/`

Returns a list of all active employees.

#### Create New Employee

POST `/api/employees/`

Request body should contain employee details.

#### Get Individual Employee

GET `/api/employees/{id}/`

Retrieves a specific employee by ID.

#### Update Existing Employee

PUT/PATCH `/api/employees/{id}/`

Updates an existing employee's details.

#### Deactivate Employee

DELETE `/api/employees/{id}/`

Deactivates an employee without removing them from the database.

### Reviews

#### Create New Review

POST `/api/reviews/`

## Data Models

The application uses two main models:

1. `Employee`: Represents an employee with attributes like name, email, etc.
2. `Review`: Represents a review left by an employee about another employee.

Both models have relationships defined to represent associations between employees and reviews.

## Authentication

This API doesn't implement authentication out-of-the-box. In a production environment, you'd want to add proper authentication mechanisms like JWT tokens or session-based authentication.

## Error Handling

The API implements custom error handling:

- 404 Not Found: Returned when trying to access deactivated employees or non-existent reviews.
- 400 Bad Request: Used for validation errors in request bodies.
- 500 Internal Server Error: May occur due to unexpected issues during processing.
