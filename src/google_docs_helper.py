from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_doc(access_token: str, title: str, markdown_content: str):
    """
    Creates a new Google Doc and populates it with text.
    """
    # 1. Build credentials object from the access token
    creds = Credentials(token=access_token)
    service = build('docs', 'v1', credentials=creds)

    # 2. Create a blank document
    doc_body = {'title': title}
    doc = service.documents().create(body=doc_body).execute()
    document_id = doc.get('documentId')

    # 3. Prepare content insertion
    # Note: A simple text insertion.
    # (Future TODO: Parse Markdown headers to real Google Docs styles)
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,  # Index 1 is the start of the body
                },
                'text': markdown_content
            }
        }
    ]

    # 4. Execute the update
    service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    return f"https://docs.google.com/document/d/{document_id}"