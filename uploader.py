from __future__ import print_function
import httplib2
import os
from sys import argv
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_known_args(None)
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive Upload'
httplib2.debuglevel = 4


def get_credentials():
    credential_path = 'credentials.json'
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    chunksize= 50 * 1024 * 1024
    files = [f for f in os.listdir('.') if os.path.isfile(f)]

    for path, subdirs, files in os.walk('.'):
        for filename in files:
            filepath = os.path.join(path, filename);
            extension = os.path.splitext(filename)[1]
            mimetype = ""
            if extension == '.srt':
                mimetype = "text/plain"
            elif extension == '.avi':
                mimetype = "video/avi"
            elif extension == '.mp4':
                mimetype = "video/mp4"
            elif extension == '.mkv':
                mimetype = "video/webm"
            else :
                continue
            print(filename)
            media = MediaFileUpload(filepath, mimetype=mimetype, chunksize=chunksize,resumable=True)
            file_metadata = {
                'name': filename
            }
            request = service.files().create(media_body=media, body=file_metadata, fields='id')
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print("Uploaded %d%%." % int(status.progress() * 100))
            print("Upload Complete! -  ",response.get('id'))
            try:
                os.remove(filepath)
                print("File removed -",filename)
            except OSError:
                pass

if __name__ == '__main__':
    main()
