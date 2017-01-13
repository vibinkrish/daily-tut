#!/usr/bin/env python

import dropbox

def main():
	client = dropbox.client.DropboxClient('hCBker0RJnoAAAAAAAAALAFL8BkpF9IhH3dEHzm_q5eNbV_j--vyFiQbSZ44sBQn')
	print 'linked account: ', client.account_info()
	movie = 'AandavanKattalai.mkv'
	f = open(movie, 'rb')
	response = client.put_file('/'+movie, f)
	print 'uploaded: ', response

	folder_metadata = client.metadata('/')
	print 'metadata: ', folder_metadata

	f, metadata = client.get_file_and_metadata('/'+movie)
	out = open('/'+movie, 'wb')
	out.write(f.read())
	out.close()
	print metadata


if __name__ == '__main__':
    main()