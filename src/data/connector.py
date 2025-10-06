# Data connector - integrates Google Drive and local file access
import pandas as pd
import os
from src.utils.cx_helpers import load_environment_variables

# Google Drive integration (adapted from google-drive-web-app)
try:
    import google.oauth2.credentials
    import google_auth_oauthlib.flow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    import io
    DRIVE_AVAILABLE = True
except ImportError:
    DRIVE_AVAILABLE = False

class DataConnector:
    def __init__(self):
        self.drive_service = None
        self.env = load_environment_variables()

    def authenticate_google_drive(self):
        """Authenticate with Google Drive API"""
        if not DRIVE_AVAILABLE:
            return "Google API libraries not available. Install required packages."

        try:
            # Check if credentials.json exists
            if not os.path.exists('credentials.json'):
                return "credentials.json not found. Download from Google Cloud Console."

            # Create flow
            SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
                      'https://www.googleapis.com/auth/drive.file']

            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                'credentials.json', scopes=SCOPES)

            # For embedded use, we need a redirect URI
            # This would typically come from a web interface
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'  # For desktop apps

            authorization_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true')

            return {
                'auth_url': authorization_url,
                'message': 'Open the URL in a browser and enter the authorization code'
            }

        except Exception as e:
            return f"Authentication setup failed: {str(e)}"

    def set_credentials(self, authorization_code):
        """Set credentials from authorization code"""
        if not DRIVE_AVAILABLE:
            return "Drive API not available"

        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
                  'https://www.googleapis.com/auth/drive.file']

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'credentials.json', scopes=SCOPES)

        flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        flow.fetch_token(code=authorization_code)

        credentials = flow.credentials
        self.drive_service = build('drive', 'v3', credentials=credentials)

        return "Google Drive authenticated successfully"

    def download_drive_file(self, file_id):
        """Download file from Google Drive"""
        if not self.drive_service:
            return None, "Not authenticated with Google Drive"

        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            file_data = io.BytesIO()
            downloader = MediaIoBaseDownload(file_data, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            file_data.seek(0)
            return file_data, None
        except Exception as e:
            return None, f"Download failed: {str(e)}"

    def load_csv_from_drive(self, sharing_url, file_name=None):
        """Load CSV from Google Drive sharing URL"""
        import gdown
        try:
            # Extract file ID from sharing URL
            file_id = None
            if 'drive.google.com/file/d/' in sharing_url:
                file_id = sharing_url.split('/file/d/')[1].split('/')[0]
            elif 'docs.google.com/spreadsheets/d/' in sharing_url:
                file_id = sharing_url.split('/spreadsheets/d/')[1].split('/')[0]
            elif 'id=' in sharing_url:
                file_id = sharing_url.split('id=')[1].split('&')[0]

            if not file_id:
                return pd.DataFrame(), "Invalid Google Drive sharing URL"

            if file_name is None:
                file_name = f"drive_{file_id}"

            # Download using gdown
            download_url = f"https://drive.google.com/uc?id={file_id}"
            downloaded = gdown.download(download_url, quiet=True)

            if not downloaded:
                return pd.DataFrame(), "Failed to download from Google Drive"

            # Load the downloaded file
            if downloaded.endswith('.csv'):
                df = pd.read_csv(downloaded)
            elif downloaded.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(downloaded)
            else:
                return pd.DataFrame(), "Unsupported file type"

            # Clean up
            os.remove(downloaded)

            return df, "Successfully loaded from Google Drive"

        except Exception as e:
            return pd.DataFrame(), f"Error downloading from Drive: {str(e)}"

    def fetch_data(self, query):
        # Placeholder for database/API connections
        return pd.DataFrame({
            'company_name': ['Sample Company A', 'Sample Company B'],
            'revenue': [100000, 150000],
            'sector': ['Retail', 'Manufacturing']
        })

    def save_data(self, data):
        # Placeholder for data saving
        if isinstance(data, pd.DataFrame):
            print(f"Saving {len(data)} records to data store")
        else:
            print("Invalid data format")

    def close(self):
        # Clean up connections
        if self.drive_service:
            self.drive_service = None
