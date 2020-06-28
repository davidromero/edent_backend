# eDent Backend

AWS serverless project for managing eDent's information.  
All lambdas are written in python 3.6 and require a DynamoDB tables.  

## Quickstart
To locally run a service use:  
```bash
pip install -r requirements.txt
chalice local
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

#### Treatments
| Method | URI Path         | Description                    |
|--------|------------------|--------------------------------|
| GET    | /                | Gets the service message       |
| GET    | /treatments      | Gets a list of all treatments  |
| POST   | /treatments      | Creates a new treatment        |
| GET    | /treatments/{uid}| Gets treatments of a patient   |
| GET    | /rates           | Gets the all the rates         |

#### Checkout
| Method | URI Path        | Description                         |
|--------|-----------------|-------------------------------------|
| GET    | /               | Gets the service message            |
| GET    | /checkout       | Gets a list of all pending payments |
| POST   | /checkout       | Creates a new pending payment       |
| DELETE | /checkout/{uid} | Sets payment status to "payed"      |

#### Appointments
| Method | URI Path            | Description                        |
|--------|---------------------|------------------------------------|
| GET    | /                   | Gets the service message           |
| GET    | /appointments       | Gets a list of future appointments |
| POST   | /appointments       | Creates a new appointment          |
| GET    | /appointments/{uid} | Gets appointment of a patient      |
| DELETE | /appointments/{uid} | Sets appointment as attended       |
| PUT    | /appointments/{uid} | Updates the appointment data       |

## Component Architecture

Architecture used for the following services:
Appointments, Checkout, Contacts, Patients and Treatments
![eDent Chalice Architecture](https://user-images.githubusercontent.com/10179447/85958093-13dd1680-b950-11ea-96a7-5edd9f84c4e6.jpg)

Architecture for Image Storage
![eDent Backend Architecture-Chalice S3](https://user-images.githubusercontent.com/10179447/85958184-cc0abf00-b950-11ea-8119-498585768eaa.jpg) 

## Deployment

```bash
chalice deploy
```




