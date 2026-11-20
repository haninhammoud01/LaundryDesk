
# LaundryDesk

*A Desktop Application for Managing Laundry Operations*

**Tech Stack:** Python · PyQt6 · SQLite

> "Good software starts with understanding how data moves, not how fancy the UI looks."

LaundryDesk is a desktop application for laundry management, developed as a final examination project for Desktop Programming.

The project follows a **product-oriented engineering approach**, focusing on clear structure, practical data flow, and essential application functionality.

It explores how to build software that is easy to understand, maintain, and demonstrate, while applying fundamental principles of desktop application development.

## Design Priorities

The development of LaundryDesk focuses on four key areas:

- **Clear data ownership:** Separating customer, package, and transaction data.
- **Relational database design:** Applying Primary Key and Foreign Key constraints.
- **Separation of concerns:** Keeping the user interface, application logic, and database operations organized.
- **Predictable user flow:** Designing interactions that are straightforward and easy to demonstrate.

The goal was not to introduce unnecessary complexity, but to establish a solid foundation for a functional desktop application.

## Database Design

LaundryDesk uses **SQLite** as its relational database, with three primary entities:

- `customers`
- `packages`
- `transactions`

Relationships between these tables ensure that:

- Every transaction is associated with a valid customer.
- Every transaction references an available laundry package.

This structure reinforces the importance of **data integrity** and relational database design in application development.

## Application Features

### Table View

Users can browse transaction records in a structured table.

Available filtering options include:

- Customer name
- Transaction status

This feature supports efficient record retrieval and provides a clear overview of ongoing transactions.

### Record View

Individual transactions can be inspected through record navigation.

Available navigation controls:

- First
- Previous
- Next
- Last

This implementation provides practical experience with state management and navigation flow in desktop applications.

### Add and Edit Records

Users can:

- Create new transactions.
- Edit existing transaction records.

All changes are stored directly in the SQLite database without mock data or intermediate files.

## UAS Requirements

LaundryDesk was developed to fulfill the requirements of the Desktop Programming final examination.

| Requirement | Status |
|---|---|
| Create and populate at least two tables using SQL, with a minimum of five records | Completed |
| Run the application through a single Python file during the demonstration | Completed |
| Implement relational database relationships using Primary Keys and Foreign Keys | Completed |
| Provide a Table View with two filtering inputs | Completed |
| Provide individual record views with navigation controls | Completed |
| Implement record creation and editing functionality | Completed |

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

Install the required dependency:

```bash
pip install PyQt6
```

### Run the Application

```bash
python laundry_uas.py
```

## Project Context

**Course:** Desktop Programming  
**Project Type:** Final Examination Project  
**Application:** Desktop Laundry Management System

LaundryDesk demonstrates the implementation of a relational database, structured application logic, and interactive desktop interfaces using Python.

The project serves as a practical exercise in building software with clear responsibilities and maintainable data flow.
