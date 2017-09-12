#########################################################IMPORTS#########################################################
import os
import discord
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import logging
#########################################################################################################################
logger = logging.getLogger(__name__)
DROPAPI = os.environ['DROPBOXAPI']
dbx = dropbox.Dropbox(DROPAPI)
LOCALFILE = 'USER.db'
BACKUPPATH = '/USER.db'

def file_len(fname):
    with open(fname,encoding='utf-8') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def restore():
    # Download the specific revision of the file at BACKUPPATH to LOCALFILE
    try:
        os.remove(LOCALFILE)
        logging.info("[USER.db] Detected Removing.....Done")
    except OSError:
        logging.warning("OSError")
        pass
    try:
        logging.info("Downloading current " + BACKUPPATH + " from Dropbox, overwriting " + LOCALFILE + "...")
        dbx.files_download_to_file(LOCALFILE, BACKUPPATH)
    except:
        logging.warning("RESTORE FAILED NO DATABASE!!")
        logging.warning("Ignoring and continuing ..")

def backup():
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        logging.info("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            try:
                dbx.files_delete(BACKUPPATH)
            except:
                pass
            dbx.files_upload(f.read(), BACKUPPATH, mode=dropbox.files.WriteMode.overwrite)
            logging.info("Uploaded!")
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                logging.warning(err.user_message_text)
                sys.exit()
            else:
                logging.warning(err)
                sys.exit()