import matplotlib.pyplot as plt

def apply_modern_style():
    plt.style.use("dark_background")
    plt.rcParams.update({
        "axes.facecolor": "#2E2E2E",
        "axes.edgecolor": "#FFFFFF",
        "axes.labelcolor": "#FFFFFF",
        "text.color": "#FFFFFF",
        "xtick.color": "#FFFFFF",
        "ytick.color": "#FFFFFF",
        "font.family": "sans-serif",
        "font.size": 12,
        "figure.facecolor": "#2E2E2E",
        "figure.edgecolor": "#2E2E2E",
    })