from collections import namedtuple
import altair as alt
import math
import pandas as pd
import random
import streamlit as st
# from gsheetsdb import connect
# from shillelagh.backends.apsw.db import connect
from gsheetsdb import connect

"""
# Welcome to Streamlit by Eclipss!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query():
    result = conn.execute("""
        SELECT
            country
          , SUM(cnt)
        FROM
            "https://docs.google.com/spreadsheets/d/1_rN3lm0R_bU3NemO0s9pbFkY5LQPcuy1pscv8ZXPtg8/"
        GROUP BY
            country
    """, headers=1)
    rows = result.fetchall()
    return rows

rows = run_query()

# Print results.
for row in rows:
    st.write(f"{row.country} has a :{row.cnt}:")

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
    point_radius = st.slider("Radius of each point", 0.1, 1.0, 0.3)

    Point = namedtuple('Point', 'x y z')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = (curr_point_num / total_points) * point_radius
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = random.random()
        data.append(Point(x, y, z))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(opacity=0.5)
        .encode(x='x:Q', y='y:Q', color='z:Q'))
