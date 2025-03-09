async def register_user(client, user_data):
    registration_data = {
        "email": user_data[0],
        "password": user_data[1],
    }
    response = await client.post("/api/v1/auth/register", json=registration_data)
    return response


async def login_user(client, user_data):
    login_data = {
        "username": user_data[0],
        "password": user_data[1],
    }
    return await client.post("/api/v1/auth/login", data=login_data)


