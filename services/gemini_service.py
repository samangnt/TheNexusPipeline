from google import genai
import json

MODELS = [
    'gemini-2.5-flash',
    'gemini-2.5-flash-lite'
]

DEV_MODE = True

def analyze_asset(asset_name: str, asset_path: str, client) -> dict:
    
    prompt = f"""You are a 3D asset analyst for a game studio.
    Analyze this 3D asset based on its filename and path only.
    
    Filename: {asset_name}
    Path: {asset_path}
    
    Respond in JSON only with exactly these keys:
    {{
        "tags": ["tag1", "tag2", "tag3"],
        "critique": "one sentence about this asset",
        "priority": "High, Medium or Low"
    }}"""
    
    models_to_try = [MODELS[0]] if DEV_MODE else MODELS
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            raw = response.text.replace("```json","").replace("```","").strip()
            return json.loads(raw)
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                continue
            else:
                raise e
    
    return {"tags": [], "critique": "API limit reached", "priority": "Low"}