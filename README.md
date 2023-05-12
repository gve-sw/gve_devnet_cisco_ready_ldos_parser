# gve_devnet_cisco_ready_ldos_parser

Django application that takes in an Excel file from Cisco Ready, parses it and outputs another Excel file in the format that the requester wanted.
It deals with a lot of the manual clean up that would have been required with a raw Cisco Ready file. However, it's not perfect due to not everything
having generic tags. This means that there might still be some manual clean up to be done after parsing the file.
As an example, there is no specific tag for management software in the Cisco Ready files, so this will need to be filtered out manually from the output file.

## Contacts

- Martin Jensen and Sarah Schön

## Solution Components

- Django
- Python
- Cisco Ready
- Pandas

## Installation/Configuration

For this project we have been using pipenv for the virtual environment. So first step is to make sure it is installed with the command "pip3 install pipenv". After that you would run through the following:

- Activate the virtual environment with; "pipenv shell"
- Install the libraries in the requirements.txt file; "pipenv install -r requirements.txt"
- Verify that pipenv install libraries; "pipenv graph". If there is output then you should be good.
- Go into the Cisco_Ready_Parser folder and run; "python3 manage.py runserver"

## Usage

To run the project

- First activate the virtual environment with; "pipenv shell"
- If all libraries are installed as per the "Installation/Configuration" then go into the Cisco_Ready_Parser folder and run; "python3 manage.py runserver"

# Screenshots

![/IMAGES/site.png](/IMAGES/site.png)
![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:

<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
