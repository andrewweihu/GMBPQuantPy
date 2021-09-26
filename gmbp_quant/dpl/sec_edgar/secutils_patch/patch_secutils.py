import secutils
import shutil
from pathlib import Path


if __name__ == '__main__':
    secutils_dir = Path(secutils.__file__).parent
    patch_filename = 'edgar.py'
    orig_edgar_path = secutils_dir / patch_filename
    patch_edgar_path = Path(__file__).parent / patch_filename
    shutil.copyfile(patch_edgar_path, orig_edgar_path)
