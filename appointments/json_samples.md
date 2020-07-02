
## POST body

```json
{
    "start_time": "2020-06-26T09:00:00",
    "duration": "30",
    "first_name": "asdf",
    "last_name": "gatica",
    "patient_uid": "1234",
    "treatment_name": "idk",
    "clinic_location": "chiquimula"
}
```

## GET body

```json
{
    "status": 200,
    "payload": [
        {
            "id": "6sq36db374r3abb464rj2b9k6cs30b9ocdh6cb9jc8s32db564rj8p9gco",
            "link": "https://www.google.com/calendar/event?eid=NnNxMzZkYjM3NHIzYWJiNDY0cmoyYjlrNmNzMzBiOW9jZGg2Y2I5amM4czMyZGI1NjRyajhwOWdjbyBhbGRvZ2F0aWNhMTIzQG0",
            "title": "Something",
            "start": {
                "dateTime": "2020-06-04T08:00:00-06:00",
                "timeZone": "America/Guatemala"
            },
            "end": {
                "dateTime": "2020-06-04T09:00:00-06:00",
                "timeZone": "America/Guatemala"
            }
        }
    ]
}
```
