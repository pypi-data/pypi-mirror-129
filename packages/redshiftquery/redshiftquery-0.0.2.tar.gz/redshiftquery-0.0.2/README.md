# Amazon Connect Tools

These tools are intended to be used to connect and query **one** redshift instance and **one** database.  

## Requirements:

This package is dependant upon [keyring](https://pypi.org/project/keyring/) for keeping credentials secure for connecting to your desired Redshift instance. 

## Instructions:

1. Installation:

```
pip install redshiftquery
```

2. Setup:

Next you will need to setup the [keyring](https://pypi.org/project/keyring/) Login information unique to your redshift database.

You will need to store a 'Host', 'Database', 'Username', and 'Password' by running the following in python once:

```py
import keyring
keyring.set_password('Redshift', 'Host', 'Your Host Server')
keyring.set_password('Redshift', 'Database', 'Your Database')
keyring.set_password('Redshift', 'Username', 'Your Username')
keyring.set_password('Redshift', 'Password', 'Your Password')
```

*note that the strings used here are case sensitive*

Copy this exactly but replace Your Host Server, Your Databas, Your Username, and Your Password with your actual login credentials. This will be stored in your OS. 

You can check that it was set up properly by executing keyring's get_password function, for example to check your Username was set up correctly:

```py
keyring.get_password('RedShift', 'Username')
```

