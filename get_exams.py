from vulcan import Account
from vulcan import Keystore
from vulcan import Vulcan


async def get_exams():
    client = None  # Initialize client variable
    exams_list = []  # Initialize a list to store exams

    try:
        with open("account.json") as f:
            account = Account.load(f)

        with open("keystore.json") as f:
            keystore = Keystore.load(f)

        # Initialize Vulcan client
        client = Vulcan(keystore, account)
        await client.select_student()
        students = await client.get_students()

        if len(students) > 1:
            client.student = students[1]

        # Example of fetching exams
        print("Fetching exams...")
        exams = await client.data.get_exams()

        # Iterate over exams and add them to the list
        async for exam in exams:
            print(exam)
            exams_list.append(exam)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if client:
            await client.close()  # Ensure the client is closed properly

    return exams_list  # Return the list of exams
