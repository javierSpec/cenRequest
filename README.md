# cenRequest
Library to handle requests from CEN API.

>In order to use this package it's important to have an authorization Token provied by the Grid Operator (Coordinador Eléctrico Nacional).

## Usage
This package codificates the API documentation and handle responses to bring resources without pagination limits.

### Example
```
import cenRequest

#Get information from the resource "Costos marginales reales"
req_obj=cenRequest.get_cmgReal(token,date)
```

This function returns an object containing information about the process, such as the results or the last response. 

```
results= req_obj.results
```
