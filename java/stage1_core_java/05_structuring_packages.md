## 📚 Java Project Organization Quick Guide

This guide ensures your code is correctly structured, named, and visible across packages.

### 1. The Core Rule: Structure & Naming 📂

The **physical location** on your disk **must** match the **logical package name**.

| Concept | Structure/Syntax | Purpose |
| :--- | :--- | :--- |
| **Project Root** | `src/main/java/` | Starting point for all application code. |
| **Package Mapping** | `com.myproject.module` | The dots (`.`) map directly to folders (`/`). |
| **File Naming** | `MyClass.java` | Must exactly match the single **public** class inside. |
| **Example Path** | `src/main/java/com/myproject/module/MyClass.java` | This is where the file belongs. |

***

### 2. The Code: Syntax ✍️

Every Java source file follows this order:

| Order | Syntax | Notes |
| :--- | :--- | :--- |
| **1st Line** | `package com.myproject.module;` | **Mandatory.** Declares the file's home package. |
| **2nd Line** | `import com.otherproject.AnotherClass;` | **Optional.** Creates a shortcut for the FQN. |
| **3rd Line** | `public class MyClass { ... }` | The class definition itself. |

### 3. Access Control (Visibility) 🔒

Use access modifiers to control which packages can see your classes and members.

| Modifier | Visibility | Usage |
| :--- | :--- | :--- |
| **`public`** | **Visible Everywhere** | Essential for classes and methods other packages (like your `UserService`) need to call. |
| **No Modifier (Default)** | **Package-Private** | Visible **only** within its own package. Used to hide internal helper/utility classes. |

### 4. Key Terminology 🔑

| Term | Meaning | Relation to Structure |
| :--- | :--- | :--- |
| **FQN** | **Fully Qualified Name** (e.g., `com.myproject.model.User`). | The **unique identifier** used by the compiler and JVM. |
| **Classpath** | The list of directories and JARs the JVM searches. | The **starting point** the JVM uses to resolve the FQN to a physical file. |

