'''

  This is for interacting with Google Docs
  The DOCUMENT_ID is pulled from the URL of a Google Doc manually
  Credentials are kept in token.json. If they don't work, for instance HTTP ERROR 403, just delete token.json and it will generate a new one upon prompting
  GDoc_Text_Block is just formatted text
  GDoc_List initialized an empty list of GDoc_Text_Block with list formatting applied every time you add a Text Block
  GDoc_Setlist_Header follows a format for a centered header.

  All of these have a write_to_doc which gets the GDOCS API requests together and then sends them based on the doc.
  The doc is a document object as defined by the google api documentation
  There are methods here to dump the object into a json and to just get the raw text of a document.
  TODO: fix the raw text function so it pulls lists more nicely

  The reason the doc needs to be passed to the write function is due to the indexing requirements

  TODO: allow multiple documents to be edited dynamically, as opposed to one global DOCUMENT_ID declaration

'''


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
import re

class GDoc_Text_Block:
  def __init__(self, text: str = ""):
    self.format = {
      "is_bold": False,
      "is_italic": False,
      "is_underline": False,
      "alignment": "START", #START, CENTER, END
      "list_type": None #None, "bullets", "numbers"
    }
    self.text = "\n" + text
  @property
  def length(self):
    return len(self.text)
  def generate_requests(self, doc, index_offset = 0):
      start_index = int( doc['body']['content'][-1]['endIndex'] ) - 1 + index_offset #END OF DOC
      range = {
            'startIndex': start_index,
            'endIndex': start_index + self.length
          }
      requests = []
      #INSERT TEXT
      requests.append({
          'insertText': {
            'location': {
              'index': start_index,  # Position in the document where you want to insert the text (1 is after the title)
            },
            'text': self.text
          }
      })
      #ALIGNMENT
      requests.append({
        'updateParagraphStyle': {
          'fields': 'alignment',
          'range': range,
          'paragraphStyle' : {
            'alignment': self.format['alignment']
          }
        }
      })
      #BOLD UNDERLINE ITALIC
      requests.append({
        'updateTextStyle': {
          'fields': 'bold,italic,underline',
          'range': range,
          'textStyle': {
            'bold': self.format['is_bold'],
            'italic': self.format['is_italic'],
            'underline': self.format['is_underline']
          }
        }
      })
      #BULLETS
      if self.format['list_type'] == "bullets":
        requests.append({
          'createParagraphBullets': {
            'range': {
                'startIndex': start_index+1,
                'endIndex': start_index + self.length
              },
            'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
          }
        })
      elif self.format['list_type'] == "numbers":
        requests.append({
          'createParagraphBullets': {
            'range': {
              'startIndex': start_index + 1,
              'endIndex': start_index + self.length
            },
            'bulletPreset': 'NUMBERED_DECIMAL_ALPHA_ROMAN'
          }
        })
      return requests
  def write_to_doc(self,doc):
    requests = self.generate_requests(doc)
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("docs", "v1", credentials=creds)
    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
    print("Write to Doc Returned:", result)


class GDoc_List:
  text_block_list = []
  def __init__(self, text_list = None):
    if type(text_list) == list:
      for text in text_list:
        self.append(
          GDoc_Text_Block(text)
        )
  def append(self, other):
    if type(other) == GDoc_Text_Block:
      self.text_block_list.append(other)
      for block in self.text_block_list:
        block.format['list_type'] = 'numbers'
      return self
    elif type(other) == str:
      self.text_block_list.append(
        GDoc_Text_Block(other)
      )
      for block in self.text_block_list:
        block.format['list_type'] = 'numbers'
      return self
    else: raise TypeError("Expected type GDoc_Text_Block or str")


  def write_to_doc(self,doc):
    requests = []
    iter_offset = 0
    for block in self.text_block_list:
      requests += block.generate_requests(doc, iter_offset )
      iter_offset += block.length
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("docs", "v1", credentials=creds)
    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
    print("Write to Doc Returned:", result)

class GDoc_Setlist_Header(GDoc_List):
  def __init__(self,event: str, date: str, time: str):
    header = GDoc_Text_Block(event)
    header.format['is_bold'] = True
    header.format['alignment'] = "CENTER"
    subheader = GDoc_Text_Block(f"{date} | {time}")
    subheader.format['alignment'] = "CENTER"
    self.text_block_list += [header, subheader]
  def __add__(self): pass


def clean_filename(filename):
  # Define a pattern to match characters that are not allowed in file names
  # For Windows: \/:*?"<>| and any non-printable characters
  # For Unix-like systems, you might want to add more rules if needed
  cleaned_filename = re.sub(r'[\/:*?"<>|]', '', filename)

  # Optionally, strip leading/trailing whitespace
  cleaned_filename = cleaned_filename.strip()

  return cleaned_filename

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/documents",
          'https://www.googleapis.com/auth/drive.file']

# The ID of a sample document.
DOCUMENT_ID = "1XjibFaYHGxfWsdPYWiprb2hB0omSjNgNjTCBdHMwdk4"


def get_live_doc(ID = DOCUMENT_ID):
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "client_secret_352248898064-8q9a4ggk8u99o2oe0m1sltqrh2i2li67.apps.googleusercontent.com.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("docs", "v1", credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    print(f"The title of the document is: {document.get('title')}")

    return document

  except HttpError as err:
    print(err)

def get_document_text(doc):
  text = ""
  #for key in doc.keys(): print(key)
  body = doc['body']
  #print()
  #for key in body.keys(): print(key)
  content = body['content']
  for item in content:
    #print(item)
    if 'paragraph' in item.keys():
      #print( "ELEMENTS: ",
      #  item['paragraph']['elements'][0]
      #)
      if 'textRun' in item['paragraph']['elements'][0]:
        text += item['paragraph']['elements'][0]['textRun']['content']
  return text

def document_to_json(doc):
  fp = "GDOC PULL " + doc['title'] + ".json"
  fp = clean_filename(fp)

  with open(fp,'w', encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=4)
def document_to_txt(doc):
  fp = "GDOC PULL "  + doc['title'] + ".txt"
  fp = clean_filename(fp)
  with open(fp, 'w') as f:
    f.write(get_document_text(doc))


def write_to_doc(doc, string: str, index: int = -1):
  if index < 0: # insert at end
    index = int( doc['body']['content'][-1]['endIndex'] ) + index
    print(index)

  requests = [
    {
      'insertText': {
        'location': {
          'index': index,  # Position in the document where you want to insert the text (1 is after the title)
        },
        'text': string
      }
    }
  ]
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  service = build("docs", "v1", credentials=creds)
  result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
  print("Write to Doc Returned:", result)


if __name__ == "__main__":
  doc = get_live_doc()
  print(
    get_document_text(doc)
  )
  document_to_json(doc)
  document_to_txt(doc)

  head = GDoc_Setlist_Header("Some Event", "10/11/12", "Afternoon")
  head.write_to_doc(doc)









