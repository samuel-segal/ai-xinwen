import boto3


client_id = ''

def user_sign_up(username, email, password):
    cognitoidp = boto3.client('cognito-idp')
    kwargs = {
        'ClientId': client_id,
        'Username': username,
        'Password': password,
        'UserAttributes': [{'Name': 'email', 'Value': email}]
    }

    response = cognitoidp.sign_up(**kwargs)
    confirmed = response['UserConfirmed']
    print(response)


if __name__ == '__main__':
    user_sign_up('bgq9ar@virginia.edu', 'password123')