
## POST body

```json
{
    "checkout": [
        {"id": 0, "name": "coronas ", "price": "1500"},
        {"id": 1, "name": "relleno blanco en cápsula ", "price": "300"},
        {"id": 2, "name": "limpieza con detrartraje ", "price": "300"}
    ],
    "treatment_type": "operatoria",
    "patient": {
    "address": "-",
    "birthday": "-",
    "clinic_location": "Jocotan",
    "email": "-",
    "first_name": "Andrea Isabel",
    "last_name": "Lopez Gutierrez",
    "sex": "Mujer",
    "visit_reason": "Operatoria"
    }
}
```

## GET body

```json
{
    "status": 200,
    "payload": [
        {
            "patient": {
                "birthday": "-",
                "address": "-",
                "visit_reason": "operatoria",
                "sex": "mujer",
                "last_name": "mendoza",
                "clinic_location": "jocotan",
                "first_name": "ana gladis",
                "email": "-"
            },
            "treatment_type": "operatoria",
            "created_by": "local",
            "checkout": [
                {
                    "name": "coronas",
                    "uid": "o016",
                    "price": "1500"
                },
                {
                    "name": "prótesis total acrílico chiquimula",
                    "uid": "o028",
                    "price": "0"
                }
            ]
        }
    ]
}
```
