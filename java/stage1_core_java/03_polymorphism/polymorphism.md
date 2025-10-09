# **Polymorphism in Java**

### **1. Definition**

Polymorphism (“many forms”) is a core concept in Java OOP that allows **one reference variable** to behave differently depending on the **actual object it points to**.

* **Compile-time polymorphism (Method Overloading)**: same method name, different parameters.
* **Runtime polymorphism (Method Overriding)**: parent reference calls child methods dynamically at runtime.

### **2. Runtime Polymorphism**

Occurs when a **parent class reference points to a child class object**, and **overridden methods** behave according to the **actual object type**.

**Example: Basic Animal Sounds**

```java
// Animal.java
class Animal {
    void makeSound() {
        System.out.println("Some generic animal sound");
    }
}

// Dog.java
class Dog extends Animal {
    @Override
    void makeSound() {
        System.out.println("Woof!");
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Animal a = new Animal();
        Animal b = new Dog(); // parent reference, child object

        a.makeSound(); // Some generic animal sound
        b.makeSound(); // Woof! → runtime chooses Dog's method
    }
}
```

**Key points:**

1. **Reference type** → determines **what methods can be called** at compile time.
2. **Actual object type** → determines **which method implementation executes** at runtime.
3. Fields are **not polymorphic**; only **methods** are dynamically dispatched.


### **3. Practical Example with Vehicles**

```java
// Vehicle.java
class Vehicle {
    void start() {
        System.out.println("Vehicle is starting!");
    }
}

// ElectricCar.java
class ElectricCar extends Vehicle {
    @Override
    void start() {
        System.out.println("Electric car starts silently!");
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Vehicle v = new Vehicle();
        Vehicle e = new ElectricCar(); // parent reference, child object

        v.start(); // Vehicle is starting!
        e.start(); // Electric car starts silently!
    }
}
```

* Even though `e` is of type `Vehicle`, the **actual object is ElectricCar**, so the overridden method runs.

### **4. Why Use Parent References**

1. **Code Generalization:** handle **any subclass** with one reference type.

```java
Vehicle[] vehicles = {new Vehicle(), new ElectricCar()};
for (Vehicle v : vehicles) {
    v.start(); // dynamic dispatch calls correct start()
}
```

2. **Flexibility & Extensibility:** adding new subclasses doesn’t require changing existing code.
3. **Polymorphic Behavior:** **one reference → many behaviors**, depending on the object.


### **5. Compile-time vs Runtime**

| Stage        | Checks                                                                |
| ------------ | --------------------------------------------------------------------- |
| Compile-time | Can this method be called? Checked using **reference type**           |
| Runtime      | Which method implementation executes? Checked using **actual object** |

---

### **6. Summary**

* **Polymorphism** allows **one reference to take many forms**.
* **Parent reference → child object** enables **dynamic behavior** at runtime.
* Makes code **flexible, reusable, and easy to maintain**.
