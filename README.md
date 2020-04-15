# eDent Backend

AWS serverless project for managing eDent's information in JSON format.  
All lambdas are written in python 3.6 and require a DynamoDB tables.  

## Quickstart
Run locally using:  
```bash
chalice local
```

#### Environment variables
```text
TABLE_NAME=edent_contacts_dev
AWS_DEFAULT_REGION=us-east-1
```

### Routes and methods

#### Patients
| Method | URI Path        | Description                    |
|--------|-----------------|--------------------------------|
| GET    | /               | Gets the service message       |
| GET    | /patients       | Gets a list of all patients    |
| POST   | /patients       | Creates a new patient          |
| GET    | /patients/{uid} | Gets a patient by id           |
| DELETE | /patients/{uid} | Inactivates a patient by id    |
| PUT    | /patients/{uid} | Replaces a patient by id       |

#### Contacts
| Method | URI Path        | Description                    |
|--------|-----------------|--------------------------------|
| GET    | /               | Gets the service message       |
| GET    | /contacts       | Gets a list of all contacts    |
| POST   | /contacts       | Creates a new contact          |
| GET    | /contacts/{uid} | Gets a specific contact        |
| DELETE | /contacts/{uid} | Inactivates a specific contact |
| PUT    | /contacts/{uid} | Updates the data of a contact  |

## Component Architecture



## Deployment

 






