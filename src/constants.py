from pathlib import Path
from urllib.parse import urljoin

# URLs for parsing
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_MAIN_URL = 'https://peps.python.org/'
PEPS_NUMERICAL_URL = 'https://peps.python.org/numerical/'
DOWLOADS_URL = urljoin(MAIN_DOC_URL, 'download.html')
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')

# Directories
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
DOWLOADS_DIR = 'downloads'
RESULTS_DIR = 'results'

# Encodings
RESPONSE_ENCODING = 'utf-8'
# Logs settings
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_SEPARATOR = '\n' + '-' * 40 + '\n'

# DateTime format for outputs
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Expected statuses for PEPs
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

PRETTY = 'pretty'
FILE = 'file'
