```java
// Animal.java
public class Animal {
    public void makeSound() {
        System.out.println("Some generic animal sound!");
    }
}

// Dog.java
public class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Woof!");
    }
}

// Main.java
public class Main {
    public static void main(String[] args) {
        Animal animal = new Animal();
        animal.makeSound(); // Some generic animal sound!

        Dog dog = new Dog();
        dog.makeSound();    // Woof!
    }
}
```