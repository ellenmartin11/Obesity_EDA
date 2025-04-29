import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your clean dataset
obesity_data_clean = pd.read_csv("obesity_data_clean.csv")

def plot_correlation(var1, var2):

    forbidden_vars = ['gender','obesity_group','transport']

    if var1 in forbidden_vars or var2 in forbidden_vars:
        return None, f"Error: You selected a categorical variable ({var1} or {var2}). Please select continuous variables."
    if var1 is None or var2 is None:
        return None
    plt.figure(figsize=(6, 6))
    sns.scatterplot(data=obesity_data_clean, x=var1, y=var2)
    plt.title(f"{var1} vs {var2}")
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.tight_layout()
    path = "scatter.png"
    plt.savefig(path)
    plt.close()
    return path, ""

def plot_heatmap(cols):
    forbidden_vars = ['gender','obesity_group','transport']

    forbidden_selected = [col for col in cols if col in forbidden_vars]
    if forbidden_selected:
        return None, f"Error: You selected categorical variables: {', '.join(forbidden_selected)}. Please select only continuous variables."

    
    if not cols or len(cols) < 2:
        return None

    corr = obesity_data_clean[cols].corr(method='spearman')
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Spearman Correlation Heatmap")
    plt.tight_layout()
    path = "heatmap.png"
    plt.savefig(path)
    plt.close()
    return path, ""

with gr.Blocks(theme = gr.themes.Soft()) as demo:
    gr.Markdown("# 🧪 Obesity Dataset Explorer")

    with gr.Tab("Scatterplot"):
        gr.Markdown("Explore correlation between two variables. Pick from the drop-downs below.")
        var1 = gr.Dropdown(label="X-axis Variable", choices=obesity_data_clean.columns.tolist())
        var2 = gr.Dropdown(label="Y-axis Variable", choices=obesity_data_clean.columns.tolist())
        scatter_btn = gr.Button("Generate Scatterplot")
        scatter_output = gr.Image()
        scatter_error = gr.Textbox(label="Error Message", interactive=False)
        scatter_btn.click(fn=plot_correlation, inputs=[var1, var2], outputs=[scatter_output,scatter_error])
        

    with gr.Tab("Heatmap"):
        gr.Markdown("Create a heatmap from selected variables. Select more than 2 variables to correlate, and make sure you do not select any categorical variables or an error will arise. Use obesity_group_cont (the continuous version of the obesity groups)")
        columns = gr.CheckboxGroup(label="Select Variables", choices=obesity_data_clean.columns.tolist())
        heatmap_btn = gr.Button("Generate Heatmap")
        heatmap_output = gr.Image()
        heatmap_error = gr.Textbox(label="Error Message", interactive=False)
        heatmap_btn.click(fn=plot_heatmap, inputs=columns, outputs=[heatmap_output, heatmap_error])

if __name__ == "__main__":
    demo.launch(share = True)

