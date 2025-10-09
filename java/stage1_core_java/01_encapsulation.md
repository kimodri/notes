# Encapsulation

**Definition:**
Encapsulation is the process of bundling data (fields) and methods that operate on that data into a single unit, usually a class. It hides the internal details of how an object works and only exposes what is necessary through public methods. This protects the object’s internal state and enforces controlled access.

---

## Access Modifiers

Access modifiers define where a class, method, or variable can be accessed from.

| Modifier    | Description                                           | Accessibility                    |
| ----------- | ----------------------------------------------------- | -------------------------------- |
| `public`    | Accessible from anywhere.                             | Within all classes and packages. |
| `private`   | Accessible only within the same class.                | Only inside the class.           |
| `protected` | Accessible within the same package and by subclasses. | Package + subclasses.            |
| *(default)* | No modifier. Accessible only within the same package. | Package only.                    |

In encapsulation, fields are usually declared **`private`** to restrict direct access, and **`public`** methods (getters/setters) are used to control how data is read or modified.


## Setters and Getters

**Purpose:**

* Getters provide read-only access to private fields.
* Setters provide controlled write access and can include validation logic.

**Example:**

```java
// Car.java
public class Car {
    private float speed;
    private float fuel;

    public float getSpeed() {
        return this.speed;
    }

    public float getFuel() {
        return this.fuel;
    }

    public void setSpeed(float speed) {
        if (speed < 0) {
            System.out.println("Speed cannot be negative!");
        } else {
            this.speed = speed;
        }
    }

    public void setFuel(float fuel) {
        if (fuel < 0) {
            System.out.println("Fuel cannot be negative!");
        } else {
            this.fuel = fuel;
        }        
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Car myCar = new Car();

        myCar.setFuel(11.1f);
        myCar.setSpeed(20.5f);
    }
}
```


## Setters and Getters with Constructors

**Purpose:**
Constructors can be used to initialize fields when an object is created.
To maintain encapsulation, constructors should call **setters** instead of assigning values directly, ensuring that validation rules still apply.

**Example:**

```java
// Car.java
public class Car {
    private float speed;
    private float fuel;

    public Car(float fuel, float speed) {
        setSpeed(speed);
        setFuel(fuel);
    }

    public void setFuel(float fuel) {
        if (fuel < 0) {
            System.out.println("Fuel cannot be negative");
            return;
        }
        this.fuel = fuel;
    }

    public void setSpeed(float speed) {
        if (speed < 0) {
            System.out.println("Speed cannot be negative");
            return;
        }
        this.speed = speed;
    }

    public float getSpeed() {
        return this.speed;
    }

    public float getFuel() {
        return this.fuel;
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Car myCar = new Car(10.5f, 25.0f);
        System.out.println("Speed: " + myCar.getSpeed());
        System.out.println("Fuel: " + myCar.getFuel());
    }
}
```
