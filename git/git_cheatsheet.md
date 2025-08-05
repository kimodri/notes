# Git Cheatsheet: Commands by Workflow Stage

## 1. Repository Setup & Cloning
These commands are used when you're first starting a project with Git or getting a copy of an existing one.

| Command                                      | Function                                                |
| :------------------------------------------- | :------------------------------------------------------ |
| `git init`                                   | Initializes a new Git repository in the current directory. |
| `git clone <repository_url>`                 | Creates a local copy of a remote Git repository.        |
| `git config --global user.name "Your Name"`  | Sets your global Git username for all repositories.     |
| `git config --global user.email "your_email@example.com"` | Sets your global Git email address for all repositories. |

## 2. Checking Status & Viewing History
These commands help you understand the current state of your repository and review past changes.

| Command                        | Function                                                                                                 |
| :----------------------------- | :------------------------------------------------------------------------------------------------------- |
| `git status`                   | Shows the current state of the working directory and the staging area, including which changes have been staged, unstaged, and untracked files. |
| `git log`                      | Shows the commit history for the current branch.                                                         |
| `git log --oneline`            | Shows a condensed commit history, one commit per line.                                                   |
| `git log --graph --oneline --all` | Shows a graphical representation of all branch histories.                                                |

## 3. Comparing Changes (Diffing)
These commands are crucial for seeing what modifications have been made.

| Command                              | Function                                                               |
| :----------------------------------- | :--------------------------------------------------------------------- |
| `git diff`                           | Shows changes between all unstaged files and the latest commit.        |
| `git diff <file_name>`               | Shows changes between an unstaged file and the latest commit.          |
| `git diff --staged`                  | Shows changes between all staged files and the latest commit.          |
| `git diff --staged <file_name>`      | Shows changes between a staged file and the latest commit.             |
| `git diff <commit_hash1> <commit_hash2>` | Shows changes between two specific commits using their hashes.         |
| `git diff HEAD~1 HEAD~2`             | Shows changes between two commits using HEAD (relative to the current commit) instead of commit hashes. |

## 4. Branching and Merging
Essential for collaborative work and managing different lines of development.

| Command | Function |
| :--- | :--- |
| `git branch` | Lists all local branches. |
| `git branch <new_branch_name>` | Creates a new branch. |
| `git checkout <branch_name>` | Switches to an existing branch. |
| `git checkout -b <new_branch_name>` | Creates a new branch and immediately switches to it. |
| `git branch -m <old_branch_name> <new_branch_name>`| Renames a local branch. |
| `git merge <branch_to_merge>` | Merges the specified branch into the current branch. |
| `git branch -d <branch_name>` | Deletes a local branch (only if it's already merged). |
| `git branch -D <branch_name>` | Forcibly deletes a local branch (even if not merged). |

## 5. Remote Operations (Beyond Push)
Commands for interacting with the remote repository that aren't just pushing your commits.

| Command                        | Function                                                                                                                              |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| `git remote -v`                | Lists all remote repositories.                                                                                                        |
| `git pull`                     | Fetches changes from the remote repository and merges them into the current branch (equivalent to git fetch followed by git merge).   |
| `git fetch`                    | Fetches changes from the remote repository but does not merge them into your current branch. Useful for seeing what's new without affecting your local work. |
| `git remote add origin <remote_url>` | Adds a new remote repository with the name 'origin' and a specified URL.                                                              |
| `git remote set-url origin <new_url>` | Changes the URL for an existing remote (e.g., 'origin').                                                                              |

## 6. Undoing Changes and Stashing
Commands for correcting mistakes or temporarily setting aside work.

| Command                        | Result                                          |
| :----------------------------- | :---------------------------------------------- |
| `git revert HEAD`              | Revert all files from a given commit            |
| `git revert HEAD --no-edit`    | Revert without opening a text editor            |
| `git revert HEAD -n`           | Revert without making a new commit              |
| `git checkout HEAD~1 -- report.md` | Revert a single file from the previous commit   |
| `git restore --staged report.md` | Remove a single file from the staging area      |
| `git restore --staged`         | Remove all files from the staging area          |                                                                                                                                                               |

## 7. Tagging
Used to mark specific points in the commit history as important

| Command                                 | Function                                                                 |
| :-------------------------------------- | :----------------------------------------------------------------------- |
| `git tag <tag_name>`                    | Creates a lightweight (non-annotated) tag at the current commit.         |
| `git tag -a <tag_name> -m "Tag message"` | Creates an annotated tag with a message. Annotated tags are generally preferred for releases. |
| `git tag`                               | Lists all tags.                                                          |
| `git show <tag_name>`                   | Shows details about a specific tag.                                      |
| `git push origin <tag_name>`            | Pushes a specific tag to the remote repository.                          |
| `git push origin --tags`                | Pushes all local tags to the remote repository.                          |