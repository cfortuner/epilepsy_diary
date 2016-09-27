import plotly.plotly as py
import plotly.graph_objs as go
from diary_app.utils import id_generator
from diary_app.clients import s3
from diary_app.config import config


def create_chart(input_data):
    # Replace the username, and API key with your credentials.
    py.sign_in('hapibot', 'ix1yikrn67')
    seizures = go.Scatter(
        x=input_data["x"]["data"],
        y=input_data["y"]["data"],
        fill='tozeroy'
    )
    chart_data = [seizures]
    chart_layout = dict(title='Seizures (Last 7 Days)',
                        xaxis=dict(title=input_data["x"]["label"]),
                        yaxis=dict(title=input_data["y"]["label"]),
                        width=800,
                        height=640)
    chart = go.Figure(data=chart_data, layout=chart_layout)
    filename = id_generator.generate_chart_image_filename()
    py.image.save_as(chart, filename=config.LOCAL_CHARTS_DIR_PATH + filename)

    s3.upload_file(filename, config.LOCAL_CHARTS_DIR_PATH +
                   filename, config.S3_USER_CHARTS_BUCKET)
    download_url = s3.get_download_url(
        bucket=config.S3_USER_CHARTS_BUCKET,
        path=filename,
        expiry=603148)

    return download_url


# Test

data = {
    "x": {
        'label': "Date",
        'data': ["Sep 22", "Sep 23", "Sep 24",
                 "Sep 25", "Sep 26", "Sep 27", "Sep 28"]
    },
    "y": {
        'label': "Count",
        'data': [1, 3, 2, 6, 3, 2, 7]
    }
}

if __name__ == "__main__":
    print create_chart(data)
