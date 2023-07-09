from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE

app = Flask(__name__)

@app.route('/')
def home():
    plot = figure()
    plot.circle([1,2], [3,4])

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(plot)

    return render_template(
        "index.html",
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )

if __name__ == "__main__":
    app.run(debug=True)

    
