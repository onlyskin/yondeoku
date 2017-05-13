If the testing database gets corrupted or deleted, make sure /private/tmp/fake.db is not anything important, then reinstantiate the db from yondeoku_3.0 top level directory by running:
```
PYTHONPATH=. python backup/createDbForTestUserMe.py
```
