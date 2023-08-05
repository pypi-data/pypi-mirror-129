# Drive List Paths

This small script application when run will create a json file of paths in a Google Drive to their associated identifiers.  This was primarily created to serve a small set of conference websites with a fair number of PDF files.  These conferences use a static site generator, and it was easier to reference links to their paths within the Google drive than by their identifiers.

## Installation

This script can be installed via pip: `python -m pip install pydrivelist`.

The script requires `PyDrive2`.  The Drive API must be enabled in order for this to work with instructutions located at the [PyDrive2 documentation](https://docs.iterative.ai/PyDrive2/quickstart/#authentication).  Quoting from the current documentation (as of November 2021):

1. Go to APIs Console and make your own project.

2. Search for ‘Google Drive API’, select the entry, and click ‘Enable’.

3. Select ‘Credentials’ from the left menu, click ‘Create Credentials’, select ‘OAuth client ID’.

4. Now, the product name and consent screen need to be set -> click ‘Configure consent screen’ and follow the instructions. Once finished:

5. Select ‘Application type’ to be Web application.

6. Enter an appropriate name.

7. Input http://localhost:8080/ for ‘Authorized redirect URIs’.

8. Click ‘Create’.

9. Click ‘Download JSON’ on the right side of Client ID to download client_secret_<really long ID>.json.

10. The downloaded file has all authentication information of your application. Rename the file to “client_secrets.json” and place it in your working directory.

