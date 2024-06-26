import plotly.express as px
import plotly.io as pio
import pandas as pd
import os
import imageio
from selenium import webdriver
import time

data = pd.read_csv('Inequality in Education.csv')

for year in range(2010, 2022):
    column_name = f'Inequality in Education ({year})'
    data[column_name].fillna(-1, inplace=True)

images_dir = './Frames'
os.makedirs(images_dir, exist_ok=True)

for year in range(2010, 2022):
    column_name = f'Inequality in Education ({year})'
    year_data = data[['ISO3', 'Country', column_name]].dropna()

    max_value = 100
    min_value = -1
   
    custom_color_scale = [
        [0, "#CCCCCC"], 
        [(0.0001 - min_value) / (max_value - min_value), "#CCCCCC"],
    ]
    
    plasma_scale_normalized = px.colors.get_colorscale('Plasma')
    for val, color in plasma_scale_normalized:
        custom_color_scale.append([(val * (max_value - 0.0001) + 0.0001 - min_value) / (max_value - min_value), color])
    
    fig = px.choropleth(year_data, locations='ISO3',
                        color=column_name,
                        hover_name='Country', 
                        hover_data={column_name: True, 'ISO3': False},
                        color_continuous_scale=custom_color_scale,
                        range_color=[min_value, max_value],
                        projection='natural earth',
                        title=f'Global Inequality in Education, {year}',
                        labels={column_name: 'Inequality Index'})

    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=30, color="RebeccaPurple"),
        geo=dict(showframe=False, showcoastlines=True, showland=True, landcolor="#CCCCCC"),
        title={
            'text': f'Global Inequality in Education, {year}',
            'y':0.95,
            'x':0.3,
            'xanchor': 'left',
            'yanchor': 'top'},
        coloraxis_colorbar=dict(
            title="Inequality Index",
            tickvals=[min_value, max_value // 2, max_value],
            ticktext=["Small", "Medium", "High"]
        )
    )

    html_path = f'{images_dir}/inequality_{year}.html'

    pio.write_html(fig, html_path)

    png_path = f'{images_dir}/inequality'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(options=options)

    html_path = os.path.abspath(html_path)

    driver.get(f'file:///{html_path}')

    time.sleep(4)

    driver.save_screenshot(f'{png_path}_{year}.png')

    driver.quit()

images = []
for year in range(2010, 2022):
    images.append(imageio.imread(f'{png_path}_{year}.png'))

imageio.mimsave(f'{images_dir}/inequality_education.gif', images, fps=1, loop=0)