import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# clean dataset
obesity_data_clean = pd.read_csv("obesity_data_clean.csv")

scatter_vars = ['age', 'height', 'weight'] # here i'm specifying which values I want to show as options for users to make scatterplots as not all variables will make sense when plot as as scatter plot
def plot_correlation(var1, var2):
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
    return path

def plot_heatmap(cols):
    forbidden_vars = ['gender','obesity_group','transport'] # also excluding variables I don't want to appear in heatmap because they are non-numeric

    forbidden_selected = [col for col in cols if col in forbidden_vars]
    if forbidden_selected:
        return None, f"Error: You selected categorical variables: {', '.join(forbidden_selected)}. Please select only continuous variables."

    
    if not cols or len(cols) < 2:
        return None

    corr = obesity_data_clean[cols].corr(method='spearman') #computes correlation using spearman (which is better for larger observations and doesn't assume normality) - good for our ordinal, non-normal datatypes
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1) # annot will include the p-values, which will look a bit bad when there are lots of variables
    plt.title("Spearman Correlation Heatmap")
    plt.tight_layout()
    path = "heatmap.png"
    plt.savefig(path)
    plt.close()
    return path, ""

numerical_variables = ['time_technology','age','height','weight','freq_veggie','amt_daily_meals','freq_snacking','amt_water','exercise_per_week','freq_alcohol'] # variables appropraite for line plot


def plot_lineplot(y_var):
    if y_var is None:
        return None
    grouped_data = obesity_data_clean.groupby(['obesity_group'])
    var_mean = grouped_data[y_var].mean()
    var_sem = grouped_data[y_var].sem()

    order = ['insufficient_weight', 
         'normal_weight',
         'overweight_level_i', 
         'overweight_level_ii',
         'obesity_type_i', 
         'obesity_type_ii', 
         'obesity_type_iii']
    
    obesity_var_mean = var_mean.reindex(order)
    obesity_var_sem = var_sem.reindex(order)
    plt.figure(figsize=(8,6))
    plt.errorbar(x=obesity_var_mean.index, y=obesity_var_mean, yerr=obesity_var_sem, fmt='-o', capsize=5)
    plt.xlabel('Obesity Category')
    plt.ylabel(f'Mean {y_var}')
    plt.title(f'Obesity and {y_var}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = "lineplot.png"
    plt.savefig(path)
    plt.close()
    return path


with gr.Blocks(theme = gr.themes.Soft()) as demo:
    gr.Markdown("# 🧪 Obesity Dataset Explorer")

    with gr.Tab("Scatterplot"): #this is for the tab on the web app for people to choose from 
        gr.Markdown("Explore correlation between two variables. Pick from the drop-downs below.")
        var1 = gr.Dropdown(label="X-axis Variable", choices=scatter_vars) #dropdowns
        var2 = gr.Dropdown(label="Y-axis Variable", choices=scatter_vars)
        scatter_btn = gr.Button("Generate Scatterplot") #button to generate scatterplot
        scatter_output = gr.Image()
        scatter_btn.click(fn=plot_correlation, inputs=[var1, var2], outputs=scatter_output)

    with gr.Tab("Lineplot"):
        gr.Markdown("Explore how different features vary across the obesity groups.")
        y_var = gr.Dropdown(label="Y-axis Variable", choices = numerical_variables)
        line_btn = gr.Button("Generate Lineplot")
        line_output = gr.Image()
        line_btn.click(fn=plot_lineplot, inputs=[y_var], outputs=line_output)
        

    with gr.Tab("Heatmap"):
        gr.Markdown("Create a heatmap from selected variables. Select more than 2 variables to correlate, and make sure you do not select any categorical variables or an error will arise. Use obesity_group_cont (the continuous version of the obesity groups)")
        columns = gr.CheckboxGroup(label="Select Variables", choices=obesity_data_clean.columns.tolist())
        heatmap_btn = gr.Button("Generate Heatmap")
        heatmap_output = gr.Image()
        heatmap_error = gr.Textbox(label="Error Message", interactive=False)
        heatmap_btn.click(fn=plot_heatmap, inputs=columns, outputs=[heatmap_output, heatmap_error])

if __name__ == "__main__":
    demo.launch(share = True)

#asked chat gpt to help with initial structuring of code using this prompt: how would I make a gradio app that let's people explore the cleaned dataset I've made and do things like make basic plots showing the correlation between variables, specify what they want to include in a correlation heatmap... etc