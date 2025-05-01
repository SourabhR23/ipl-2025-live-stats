import pandas as pd

def style_table(df: pd.DataFrame):
    return (
        df.style
        .set_properties(**{
            'background-color': '#121212',   # deep dark gray
            'color': 'white',
            'border-color': '#333',
            'font-size': '12px',
            'text-align': 'center'
        })
        .set_table_styles([{
            'selector': 'th',
            'props': [('background-color', '#1f1f1f'),
                      ('color', 'white'),
                      ('font-weight', 'bold'),
                      ('text-align', 'center')]
        }])
        .format(na_rep="-", formatter={col: '{:,.0f}' for col in df.select_dtypes(include=['float', 'int']).columns})
    )
