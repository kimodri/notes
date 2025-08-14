Much like flask you go to the `models.py` inside of an app to create classes representing a table:

`flights/models.py`
```python
class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()
```

- But this still does not do anything, you still do not have a database.
- Tell django you should update the database to include information about the models that you have created (migration)
    - `python manage.py makemigrations`: to migrate
    - `python manage.py migrate`: to apply the migration
    - Now you will have a database here

## Inserting data to the table:
```python
from flights.model import Flight
f = Flight(origin="New York", destination="London", duration=415)
f.save()

# query the class/flight
flights = Flight.objects.all()
```
That will return:
- `QuerySet [<Flight: Flight object (1)>]`
That is not a very good representation of an instance of the table so in the class: `Flight`, you can add:
```python
def __str__(self):
    return f"{self.id}: {self.origin} to {self.destination}"
```
### Getting a specific instance
But if you want to assign a specific instance to a bvariable, you can do that:
```python
flight = flights.first()
```
Now you can do `flight.id`, `flight.destination`, ...

---
## Relationships
Unfortunately, the above model is not the best model for this app, instead we could:
```python
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"
```
Now, the Fligth class will have to change:
```python
class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="") # so that when the 
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()
```
