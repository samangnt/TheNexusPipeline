import os
from models.studio_asset import StudioAsset

def crawl_directory(path: str) -> list:
    assets = []
    
    # Loop through everything in the folder
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        
        # If it's a folder — go INSIDE it (recursion!)
        if os.path.isdir(full_path):
            assets.extend(crawl_directory(full_path))
        
        # If it's a .fbx or .blend file — create an asset
        elif item.endswith(('.fbx', '.blend')):
            asset = StudioAsset(name=item, path=full_path)
            assets.append(asset)
    
    return assets