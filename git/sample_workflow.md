# Example Git WorkFlow: Developing a New Feature
Let's imagine you're a developer working on a web application. Your task is to add a new "User Profile" page.

## Scenario 1: Starting a Brand New Project (or Clong an Existing One)
### (If starting new)

### 1. Initialize a new repository:
```bash
mkdir my-web-app
cd my-web-app
git init
```
### 2. Configure your Identity:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### (If joining an existing project)
### 1. Clone the existing reposistory
```bash
git clone https://github.com/your-org/my-web-app.git
cd my-web-app
```
## Scenario 2: Getting Ready for Feature Dev
Youu are ready to start working on the "User Profile" page.

### 1. Check your current status
`git status`

### 2. Ensure your local main branch is up-to-date withh the remote
This ensures you start your new feature from the latest stable version of the project.
```bash
git checkout main # Switch to main if not already there
git pull          # Fetch and merge changes from remote main
```
### 3. Create a new branch for your feature
Naming convention feature/ is common. Always work on a separate branch for new features or bug fixes.

`git checkout -b feature/user-profile`
