# Welcome to Kanbanize SDK


Kanbanize-sdk is a python library built on top of the Kanbanize platform API V2.
In addition to providing interaction with the platform's resources, we make objects available through dataclasses that
they facilitate the composition of parameters used in research and payloads for updating and inserting data into the platform.

### Installation

To install the library in your project, you can do it through the pip package manager

```
pip install kanbanize-sdk
```


### How to use?

Once installed, you can import the class responsible for creating the resource instance, passing the authentication data,
and other dataclasses that helped you set up queries and interactions with the desired resources. For example:

```
from kanbanize_sdk import Kanbanize, UserListParams

if __name__ == '__main__':
	service = Kanbanize({'subdomain': <subdomain_string>, 'api_key': <apikey_string>})
	params = UserListParams(is_enabled=0, users_id=[1,5,20])
	response = service.users().list(params=params)
```

Every output response will follow the examples listed on the Kanbanize platform, except for making a small adjustment to the response the application will give you.
Example from:

```
{
    "data": [
        {
            "user_id": 0,
            "email": "string",
            "username": "string",
            "realname": "string",
            "avatar": "string",
            "is_enabled": 0,
            "is_confirmed": 0,
            "is_tfa_enabled": 0,
            "registration_date": "2023-10-30"
        }
    ]
}
```
To:

```
[
    {
        "user_id": 0,
        "email": "string",
        "username": "string",
        "realname": "string",
        "avatar": "string",
        "is_enabled": 0,
        "is_confirmed": 0,
        "is_tfa_enabled": 0,
        "registration_date": "2023-10-30"
    }
]
```