## Copying Files and Directories in Shell

### Copy a single file

```bash
cp file1.csv file2.csv
```
> Creates a copy of `file1.csv` named `file2.csv`. Overwrites `file2.csv` if it exists.

### Copy multiple files into a directory
```bash
cp file1.csv file2.csv directory1/
```

### Copy a directory
```bash
cp -r folder1/ folder2/
```
- If `folder2/` does not exist, creates a copy of `folder1/` named `folder2/`.
- If `folder2/` exists, copies `folder1/` into `folder2/` (results in `folder2/folder1/`).

| Action                          | Command Example                                         |
| ------------------------------- | ------------------------------------------------------- |
| Copy a single file              | `cp file1.csv file2.csv`                                |
| Overwrite an existing file      | `cp file1.csv file2.csv`                                |
| Copy multiple files to a folder | `cp file1.csv file2.csv directory1/`                    |
| Copy a folder (rename)          | `cp -r folder1/ folder2/` (if `folder2/` doesn't exist) |
| Copy a folder into a folder     | `cp -r folder1/ folder2/` (if `folder2/` exists)        |

## How can I move a file?
`mv` does the same thing. It handles its parameters the same way as cp, so the command:

`mv file.csv file2.csv ..`
- moves the files `file.csv` and `file1.csv` from the current working directory up one level to its parent directory. 