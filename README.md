# Automated Email Responder for Collaboration Requests

## Overview

This project presents an Automated Email Responder script, tailored for professionals like Max Grabel, a DJ and Music Creator. It streamlines the process of responding to collaboration requests by utilizing Natural Language Processing (NLP) to analyze incoming emails and automatically generating personalized replies based on predefined profiles and rate cards.

## Features

- **NLP Analysis**: Breaks down incoming emails to understand context and intent using spaCy.
- **Personalized Responses**: Crafts responses based on the analysis, reflecting individual preferences and professional rates.
- **Customizable Profiles**: Offers flexibility to modify user profiles and response templates to better align with personal branding and response strategies.

## Setup

### Prerequisites

Ensure you have the following before setting up the project:
- Python 3.8 or newer.
- spaCy library, for NLP functions.
- TextBlob library, for sentiment analysis and additional NLP features.
- Access to a Gmail account for integration (optional for automation).

### Installation

To set up the script on your local machine:

1. Clone this repository.
2. Install the required Python libraries:

    Windows:
    ```bash
    pip install spacy textblob google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
    Mac:
   ```bash
    pip3 install spacy textblob google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

4. Download the spaCy English core model:
   
    Windows:
    ```bash
    python -m spacy download en_core_web_sm
    ```
    Mac:
   ```bash
    python3 -m spacy download en_core_web_sm
    ```

    

6. (Optional) Set up Gmail API by following Google's Gmail API Python Quickstart guide.

## Run

When running the Test and Automation, there is a difference in functionality:

- **TestEmailResponder**: This command is used for testing the functionality of the script. It does not involve sending actual emails but simulates the processing of emails and generates responses based on predefined scenarios.

    - **Windows**: Execute the following command:
        ```bash
        python TestEmailResponder
        ```

    - **Mac**: Execute the following command:
        ```bash
        python3 TestEmailResponder
        ```

- **Automation**: This command is used to run the script in automation mode, where it actively monitors incoming emails and sends out responses automatically.

    - **Windows**: Execute the following command:
        ```bash
        python EmailAutomation
        ```

    - **Mac**: Execute the following command:
        ```bash
        python3 EmailAutomation
        ```

Ensure to use the appropriate command based on your operating system and the desired functionality.

## Usage

1. Update the `max_profile` dictionary in the script with your information, preferences, and rates.
2. Run the script.
   - For manual email sending:
     - Use Gmail labels: Ensure to use Labels within Gmail and drag the incoming collaboration request emails into the specified label to trigger the script to process and send responses.
   - For automated email processing:
     - Update Gmail labels: Modify the label with the provided "Automate" script to enable automated processing of incoming emails.
3. Customize the email response templates and conditions within the script as needed to accommodate different types of collaboration queries and offers.

Ensure to follow the appropriate steps for manual or automated email processing based on your workflow requirements.

## Development Considerations

This project is currently in the prototype stage and has been developed up to the implementation of the Python script and integration with the Gmail API. As of now, it is not a fully automated solution running 24/7. Users must manually run the script each time they want to process incoming emails and drag the emails into the specified label within Gmail to trigger the script.

Further development is needed to achieve seamless automation, including continuous monitoring of emails and automatic response generation without user intervention. Future enhancements may involve implementing scheduling mechanisms, improving email categorization accuracy, and enhancing integration with email platforms for smoother operation.

Please be aware that this prototype is intended for demonstration and testing purposes, and additional refinement is required for practical deployment in real-world scenarios.


## Challenges and Resolutions

- **NLP Adaptability**: Enhanced the model and refined algorithms for broader email context comprehension.
- **Response Applicability**: Expanded user profile settings and response conditions for greater relevancy.
- **Integration Simplicity**: Provided clearer setup instructions and streamlined Gmail API integration process.

