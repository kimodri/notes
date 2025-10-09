## **`toString()`, `equals()`, and `hashCode()` Overrides**

### 1. **`toString()`**

* Defined in the `Object` class and returns a string representation of an object.
* The **default** implementation returns something like:

  ```
  ClassName@HexadecimalHashCode
  ```
* **Purpose of overriding:** to provide a more readable and meaningful description of the object.
* **Example:**

  ```java
  @Override
  public String toString() {
      return "Car{brand='" + brand + "', model='" + model + "'}";
  }
  ```
* When you call `System.out.println(car);`, Java automatically calls `car.toString()`.


### 2. **`equals()`**

* Also comes from the `Object` class.
* The default implementation compares **memory addresses**, meaning two objects are only equal if they are the same instance.
* **Overriding** allows comparison based on **content** instead.
* **Example:**

  ```java
  @Override
  public boolean equals(Object obj) {
      if (this == obj) return true;           // same reference
      if (obj == null || getClass() != obj.getClass()) return false;
      Car car = (Car) obj;
      return brand.equals(car.brand) && model.equals(car.model);
  }
  ```
* Usually overridden when you need **logical equality** (e.g., two different objects with the same field values).


### 3. **`hashCode()`**

* Returns an integer hash value used in **hash-based collections** (like `HashMap` and `HashSet`).
* When you override `equals()`, you **must also override `hashCode()`** to maintain consistency.
* Two equal objects **must have the same hash code**, though two different objects can share one.
* **Example:**

  ```java
  @Override
  public int hashCode() {
      return Objects.hash(brand, model);
  }
  ```

---

### **Key Relationship**

* `equals()` defines **when two objects are equal**.
* `hashCode()` ensures **equal objects produce the same hash**.
* `toString()` provides a **human-readable form** of the object.

