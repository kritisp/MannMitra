import os
import urllib.request
import urllib.error
import json

def load_env():
    env_vars = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env_vars[key.strip()] = val.strip()
    return env_vars

def test_supabase(url, key):
    if not url or not key:
        return False, "Missing Supabase URL or Key in .env file."
    
    # Strip any surrounding quotes
    url = url.strip('"\'')
    key = key.strip('"\'')
    
    # Query counsellors table which should exist and be readable by anon
    api_url = f"{url.rstrip('/')}/rest/v1/counsellors?select=*"
    req = urllib.request.Request(api_url)
    req.add_header("apikey", key)
    req.add_header("Authorization", f"Bearer {key}")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status in (200, 204):
                return True, "Supabase connection is working! Successfully queried 'counsellors' table."
            else:
                return False, f"Supabase API returned status: {response.status}"
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        try:
            err_json = json.loads(body)
            err_msg = err_json.get("message", body)
        except Exception:
            err_msg = body
        return False, f"Supabase check failed: HTTP {e.code} - {err_msg}"
    except Exception as e:
        return False, f"Supabase connection failed: {e}"

def test_gemini(api_key):
    if not api_key:
        return False, "Missing GEMINI_API_KEY in .env file."
    
    api_key = api_key.strip('"\'')
    
    # Let's try listing the models first to see if the API key is valid at all
    list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
    req_list = urllib.request.Request(list_url)
    
    try:
        with urllib.request.urlopen(req_list, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            available_models = [m.get("name") for m in res_data.get("models", [])]
            print(f"DEBUG: API Key works! Available models: {available_models}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        try:
            err_json = json.loads(body)
            err_msg = err_json.get("error", {}).get("message", body)
        except Exception:
            err_msg = body
        return False, f"Gemini API key is invalid or unauthorized (ListModels failed): HTTP {e.code} - {err_msg}"
    except Exception as e:
        return False, f"Gemini API list connection failed: {e}"
        
    # Test endpoint for Gemini models using v1 (stable) and v1beta (fallback)
    versions = ["v1", "v1beta"]
    models = ["gemini-2.0-flash", "gemini-2.5-flash"]
    errors = []
    
    for version in versions:
        for model in models:
            url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={api_key}"
            data = json.dumps({
                "contents": [{"parts": [{"text": "Respond with the word 'OK'."}]}]
            }).encode("utf-8")
            
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return True, f"Gemini API key is working with model {model} (version {version})! Test response: '{text}'"
            except urllib.error.HTTPError as e:
                body = e.read().decode('utf-8', errors='ignore')
                try:
                    err_json = json.loads(body)
                    err_msg = err_json.get("error", {}).get("message", body)
                except Exception:
                    err_msg = body
                errors.append(f"{version}/{model}: HTTP {e.code} - {err_msg}")
            except Exception as e:
                errors.append(f"{version}/{model}: {e}")
                
    return False, f"Gemini API check failed on all models/versions: {'; '.join(errors)}"

def main():
    print("=" * 60)
    print("MANNMUTRA CREDENTIAL VALIDATION UTILITY")
    print("=" * 60)
    
    env_vars = load_env()
    
    supabase_url = env_vars.get("SUPABASE_URL")
    supabase_key = env_vars.get("SUPABASE_KEY")
    gemini_key = env_vars.get("GEMINI_API_KEY")
    
    print("\n--- 1. SUPABASE DATABASE CONNECTION CHECK ---")
    print(f"URL: {supabase_url if supabase_url else '<Not Set>'}")
    if supabase_url and supabase_key:
        success, msg = test_supabase(supabase_url, supabase_key)
        if success:
            print(f"[SUCCESS] {msg}")
        else:
            print(f"[FAILED] {msg}")
    else:
        print("[FAILED] Supabase credentials not found in .env file.")
        
    print("\n--- 2. GEMINI AI API CHECK ---")
    if gemini_key:
        success, msg = test_gemini(gemini_key)
        if success:
            print(f"[SUCCESS] {msg}")
        else:
            print(f"[FAILED] {msg}")
    else:
        print("[FAILED] Gemini API key not found in .env file.")
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
