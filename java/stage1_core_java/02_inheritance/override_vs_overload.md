### **Method Overriding**

**Definition:**
Method overriding occurs when a **subclass** provides its own implementation of a method that already exists in its **parent class**.
The method must have the **same name**, **return type**, and **parameters**.

**Key Points:**

* Requires **inheritance**.
* The **child class** overrides the parent’s version of the method.
* Used to **change or extend behavior** of the parent method.
* The method in the parent class can be called using `super.methodName()`.
* Usually combined with the `@Override` annotation for clarity.

**Example:**

```java
// Vehicle.java
public class Vehicle {
    public void start() {
        System.out.println("Vehicle is starting!");
    }
}

// ElectricCar.java
public class ElectricCar extends Vehicle {
    @Override
    public void start() {
        System.out.println("Electric car starts silently!");
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Vehicle v = new Vehicle();
        v.start(); // Vehicle is starting!

        ElectricCar e = new ElectricCar();
        e.start(); // Electric car starts silently!
    }
}
```

### **Method Overloading**

**Definition:**
Method overloading occurs when **multiple methods in the same class** share the same name but have **different parameter lists** (number or type of parameters).

**Key Points:**

* Does **not** require inheritance.
* Return type **can differ**, but it’s not enough to overload by return type alone.
* Used to make methods **more flexible** and **convenient** for different inputs.

**Example:**

```java
// Calculator.java
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public double add(double a, double b) {
        return a + b;
    }

    public int add(int a, int b, int c) {
        return a + b + c;
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Calculator calc = new Calculator();

        System.out.println(calc.add(2, 3));        // 5
        System.out.println(calc.add(2.5, 3.5));    // 6.0
        System.out.println(calc.add(1, 2, 3));     // 6
    }
}
```

### **Summary Table**

| Aspect      | Method Overriding                   | Method Overloading          |
| ----------- | ----------------------------------- | --------------------------- |
| Location    | Between parent and child classes    | Within the same class       |
| Parameters  | Must be identical                   | Must differ                 |
| Return Type | Must be same (or covariant)         | Can differ                  |
| Inheritance | Required                            | Not required                |
| Purpose     | Change or extend inherited behavior | Increase method flexibility |
