# term7sds
## Guide
1. to clone reposiotry
   1. in terminal, go to project directory, ```git clone {url}```
2. to make minor edits in same branch,
   1. ```git pull```
   2. (make edits)
   3. ```git add .```
   4. ```git commit -m'{a_useful_message}'```
   5. ```git push```
3. to add new feature by creating a new branch,
   1. go to branch A
   2. create new branch B ```git branch {B}```
   3. go to branch: ```git checkout {B}```
   4. follow step 3
4. merge {B} to {A} then to main
   1. ```git checkout {B}```
   2. ```git pull```, fix conflicts then commit and push
   3. ```git checkout {A}```
   4. ```git pull```, fix conflicts then commit and push
   5. ```git merge --no-ff --no-commit {B}```
   6. ```git push```
