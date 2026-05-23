from pathlib import Path
from models.studio_asset import StudioAsset

def crawl_directory(path: str) -> list:
    assets = []
    
    # Convert string path to Path object — handles Windows/Mac automatically
    folder = Path(path)
    
    for item in folder.iterdir():
        
        # If it's a folder — go INSIDE it (recursion!)
        if item.is_dir():
            assets.extend(crawl_directory(str(item)))
        
        # If it's a .fbx or .blend file — create an asset
        elif item.suffix in ('.fbx', '.blend'):
            asset = StudioAsset(name=item.name, path=str(item))
            assets.append(asset)
    
    return assets