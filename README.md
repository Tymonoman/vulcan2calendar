# Vulcan2Calendar

Vulcan2Calendar is a Python application that fetches exam data from the Vulcan API and creates events in Google Calendar. This tool helps students keep track of their exams by automatically adding them to their Google Calendar.

## Features

- **Fetch Exams**: Retrieves exam data using the Vulcan API.
- **Google Calendar Integration**: Automatically creates events in Google Calendar for each exam.
- **Error Handling**: Handles various exceptions and provides informative error messages.

## Prerequisites

- Python 3.7+
- Google Calendar API credentials
- Vulcan API credentials

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Tymonoman/vulcan2calendar.git
    cd Vulcan2Calendar
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up Google Calendar API credentials**:
    - Follow the instructions [here](https://developers.google.com/calendar/quickstart/python) to create `credentials.json`.

5. **Set up Vulcan API credentials**:
    - Place your `keystore.json` and `account.json` files in the project directory.

## Usage

1. **Run the application**:
    ```sh
    python vulcan2calendar.py
    ```

2. **Authenticate**:
    - The first time you run the application, it will prompt you to authenticate with your Google account.

3. **Check your Google Calendar**:
    - After successful execution, check your Google Calendar for the newly created exam events.

## Project Structure

- `vulcan2calendar.py`: Main script to fetch exams and create calendar events.
- `get_exams.py`: Contains functions to fetch exams from the Vulcan API.
- `refactor_strings.py`: Contains functions to parse and format exam data.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.