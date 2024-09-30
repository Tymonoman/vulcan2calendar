from vulcan import Account, Keystore, Vulcan

async def get_exams():
    """
    Fetches exams using the Vulcan API and returns a list of exams.

    Returns:
        list: A list of exams fetched from the Vulcan API.
    """
    exams_list = []
    client = None

    try:
        client = Vulcan(load_keystore("keystore.json"), load_account("account.json"))
        await client.select_student()
        students = await client.get_students()
        if len(students) > 1:
            client.student = students[1]

        async for exam in await client.data.get_exams():
            exams_list.append(exam)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client:
            await client.close()

    return exams_list

def load_account(file_path):
    """
    Loads the account from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the account information.

    Returns:
        Account: The loaded account object.
    """
    with open(file_path) as f:
        return Account.load(f)

def load_keystore(file_path):
    """
    Loads the keystore from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the keystore information.

    Returns:
        Keystore: The loaded keystore object.
    """
    with open(file_path) as f:
        return Keystore.load(f)