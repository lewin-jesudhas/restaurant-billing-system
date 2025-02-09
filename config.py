from supabase import create_client

# Replace with your Supabase details
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your-anon-key"
# Initialize Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

