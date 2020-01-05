from flask import Flask,render_template
from pyecharts.charts import Map
from pyecharts.charts import Bar, Page, Pie, Timeline
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
import csv


app = Flask(__name__)

# 首页
@app.route('/')
def entry_page() -> 'html':
    """Display this webapp's HTML form."""
    return render_template('entry.html')

# 2010-2017年世界空气污染程度
@app.route('/')
@app.route('/index1')
def timeline_map() -> Timeline:
    df = pd.read_csv("data/API_worldap2shijianzhou.csv")
    tl = Timeline()
    for i in range(2010, 2018):
        map0 = (
            Map()
                .add(
                "pm2.5浓度", list(zip(list(df.CountryName), list(df["{}".format(i)]))), "world", is_map_symbol_show=False
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="2010-2017年世界空气污染程度".format(i),
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=10,
                                                                                     font_style="italic")),

                visualmap_opts=opts.VisualMapOpts(series_index=0, max_=99.73437372),

            )
        )
        tl.add(map0, "{}".format(i))
        map0.render("templates/世界空气污染.html")
        with open("templates/世界空气污染.html", encoding="utf8", mode="r") as f:
            sym = "".join(f.readlines())
            return render_template('result1.html',
                                   the_sym=sym,
                                   )

@app.route('/index2')
def geo_heatmap() -> Geo:
    df = pd.read_csv("data/chinafensheng.csv")
    dfc = df.fillna(0)
    d = (
        Geo()
        .add_schema(maptype="china")
        .add(
            "二氧化硫排放量",
            [list(z) for z in zip(list(df.地区),list(df['2010']))],
            type_=ChartType.HEATMAP,
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=1537818),
            title_opts=opts.TitleOpts(title="2010中国各省空气污染程度"),
        )
    )
    d.render("templates/2010provinceheatmap.html")
    with open("templates/2010provinceheatmap.html", encoding="utf8", mode="r") as f:
        sym = "".join(f.readlines())
        return render_template('result2.html',
                               the_sym2=sym,
                               )

@app.route('/')
@app.route('/index3')
def geo_map2017() -> Geo:
    df = pd.read_csv("data/chinafensheng.csv")
    dfc = df.fillna(0)
    dfc
    e = (
        Geo()
        .add_schema(maptype="china")
        .add(
            "二氧化硫排放量",
            [list(z) for z in zip(list(df.地区),list(df['2017']))],
            type_=ChartType.HEATMAP,
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=1537818),
            title_opts=opts.TitleOpts(title="2017中国各省空气污染程度"),
        )
    )
    e.render("templates/2017provinceheatmap.html")
    with open("templates/2017provinceheatmap.html", encoding="utf8", mode="r") as f:
        sym = "".join(f.readlines())
        return render_template('result3.html',
                               the_sym=sym,
                               )


@app.route('/')
@app.route('/index4')
def bar_base() -> Bar:
    df = pd.read_csv("data/API_worldap2shijianzhou.csv", index_col="CountryName")
    x轴 = [int(x) for x in df.columns.values[-8:]]
    中国 = list(df.loc['China'].values)[-8:]
    中国
    澳大利亚 = list(df.loc['Australia'].values)[-8:]
    澳大利亚
    za = (
        Bar()
        .add_xaxis(x轴)
        .add_yaxis("中", 中国)
        .add_yaxis("澳", 澳大利亚)
        .set_global_opts(title_opts=opts.TitleOpts(title="空气污染程度中澳对比", subtitle="pm2.5历年对比图"))
    )
    za.render("templates/comparison.html")
    with open("templates/comparison.html", encoding="utf8", mode="r") as f:
        sym = "".join(f.readlines())
        return render_template('result4.html',
                               the_sym=sym,
                               )



if __name__ == '__main__':
    app.run()

