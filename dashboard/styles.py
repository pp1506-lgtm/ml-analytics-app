def load_css():
    css = """
    <style>

    /* GLOBAL DARK THEME */
    body {
        background-color: #0e0e10;
    }

    .main {
        background-color: #0e0e10;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0e0e10;
    }

    /* NICE GLASS CARD */
    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }

    /* GRADIENT TITLE TEXT */
    .gradient-text {
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* GRADIENT BUTTON */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #6a5cff, #b14cff);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        font-size: 1rem;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 22px rgba(123, 52, 255, 0.6);
    }

    </style>
    """
    return css
