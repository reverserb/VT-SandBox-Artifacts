import sys
import os
import requests
import threading
import time
import zipfile

GUEST_USERNAME = os.getlogin()
ANALYZER_URL = (
    'https://sandbox-dispatcher-dot-virustotalcloud.appspot.com/get_bundle')
HEADERS = {'User-Agent': 'jujubox'}
ANALYSIS_ZIP_FILENAME = 'analysis.zip'
DROP_FOLDER = 'C:\\Users\\%s\\Downloads' % GUEST_USERNAME
SETTINGS_FILE = 'settings.py'


def update_settings(token):
  with open(SETTINGS_FILE, 'r') as settings_file:
    settings_content = settings_file.read().replace('<TOKEN-ID>', token)

  with open(SETTINGS_FILE, 'w') as settings_file:
    settings_file.write(settings_content)


def main():
  """Download agent from the remote server and execute it."""
  token = sys.argv[1]
  HEADERS.update({'Token': token})

  while True:
    try:
      response = requests.get(ANALYZER_URL, stream=True, headers=HEADERS)
      if response.status_code == requests.codes.ok:  # pylint: disable=no-member
        break
      time.sleep(3)
    except requests.exceptions.RequestException:
      time.sleep(3)
      continue

  zipfile_path = os.path.join(DROP_FOLDER, ANALYSIS_ZIP_FILENAME)

  with open(zipfile_path, 'wb') as analysis_zip:
    for chunk in response.iter_content(chunk_size=100 * 1024):
      if chunk:
        analysis_zip.write(chunk)

  os.chdir(DROP_FOLDER)

  with zipfile.ZipFile(ANALYSIS_ZIP_FILENAME, 'r') as analysis_zip:
    analysis_zip.extractall('.')
    analysis_zip.close()

  update_settings(token)

  sys.path.append(DROP_FOLDER)
  import vm_init
  vm_main_thread = threading.Thread(target=vm_init.main)
  vm_main_thread.start()

  # Remove *.py, *.pyc, *.pyw files
  os.remove(ANALYSIS_ZIP_FILENAME)

  vm_main_thread.join()


if __name__ == '__main__':
  main()

