# eDent Backend

AWS serverless project for managing eDent's information.  
All lambdas are written in Python 3.6 and require a DynamoDB tables.  

## Quickstart
To locally run a service use on the working directory:  
```bash
pip install -r requirements.txt
chalice local
```

## Deployment

```bash
chalice deploy
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

#### Image Storage
| Method | URI Path            | Description                        |
|--------|---------------------|------------------------------------|
| GET    | /                   | Gets the service message           |
| GET    | /upload/{uid}       | Uploads an image with a unique id  |

## Component Architecture

Architecture used for the following services:
Appointments, Checkout, Contacts, Patients and Treatments
![Backend Architecture-DynamoDB services](https://user-images.githubusercontent.com/10179447/86320572-68a0bb80-bbf4-11ea-9e36-680f462aafc0.jpg)

Architecture for Image Storage
![Backend Architecture-S3 services](https://user-images.githubusercontent.com/10179447/86320510-44dd7580-bbf4-11ea-8801-63ac7ae5e062.jpg)





