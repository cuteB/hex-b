# Getting started

> Because even I forget how to do it

[X](../README.md)

## Install Dependencies

```bash
pip install -r requirements.txt
```

Then just [run](#run) the rest

## Run

Check to see if it works

```bash
$ python main.py --mock
```

The `-mock` is for running the game without logging to a database. 

```bash
$ python main.py --help
```

Look at all of the flags that can be ran

## Test

Run all of the tests.

```bash
$ python -m pytest
```

## Database 

Initialize the sqlite database and tables

```bash
$ python xQuery.py init_db
```


