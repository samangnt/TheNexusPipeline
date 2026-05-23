from datetime import datetime

class StudioAsset:
    def __init__(self, name:str, path:str):
        self.name = name
        self.path = path
        self.status ="UNPROCESSED"
        self.tags=[]
        self.critique = ""
        self.discovered_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def mark_processed(self, tags:list, critique:str):
        self.tags = tags
        self.critique=critique
        self.status="PROCESSED"
    
    def to_dict(self) -> dict:
        return{
            "name":self.name,
            "path": self.path,
            "status": self.status,
            "tags": str(self.tags),
            "critique": self.critique,
            "discovered_at": self.discovered_at
        }