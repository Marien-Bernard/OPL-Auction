import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Player Analytics",
    layout="wide"
)

header1, header2, header3 = st.columns([1, 3, 1])

with header1:
    st.image("assets/occ_logo.png", width=150)

with header2:
    st.markdown(
        """
        <h1 style='text-align:center;'>
        OPL SEASON 6 AUCTION
        </h1>
        """,
        unsafe_allow_html=True
    )

with header3:
    st.image("assets/season6_logo.png", width=150)


st.title("📊 OPL Player Analytics")

# ------------------------------------
# LOAD DATA
# ------------------------------------

df = pd.read_excel(
    "data/players.xlsx"
)

# ------------------------------------
# SIDEBAR FILTERS
# ------------------------------------

st.sidebar.header("Filters")

player_search = st.sidebar.selectbox(
    "Search Player",
    ["All Players"] +
    sorted(
        df["Name of the Player"]
        .dropna()
        .unique()
        .tolist()
    )
)

role_filter = st.sidebar.multiselect(
    "Playing Role",
    sorted(
        df["Playing Role"]
        .dropna()
        .unique()
        .tolist()
    )
)

# ------------------------------------
# APPLY FILTERS
# ------------------------------------

filtered_df = df.copy()

if player_search != "All Players":

    filtered_df = filtered_df[
        filtered_df["Name of the Player"]
        == player_search
    ]

if role_filter:

    filtered_df = filtered_df[
        filtered_df["Playing Role"]
        .isin(role_filter)
    ]

# ------------------------------------
# KPI CARDS
# ------------------------------------

st.subheader("Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Players",
        len(filtered_df)
    )

with c2:
    st.metric(
        "Average Age",
        round(
            filtered_df["Age"].mean()
        )
    )

with c3:
    st.metric(
        "Youngest",
        int(filtered_df["Age"].min())
    )

with c4:
    st.metric(
        "Oldest",
        int(filtered_df["Age"].max())
    )

# ------------------------------------
# TABS
# ------------------------------------

tab1, tab2 = st.tabs(
    [
        "📊 Analytics",
        "👤 Player Explorer"
    ]
)

# ====================================
# ANALYTICS TAB
# ====================================

with tab1:

    # -------------------------------
    # AGE DISTRIBUTION
    # -------------------------------

    st.subheader("Age Distribution")

    fig = px.histogram(
        filtered_df,
        x="Age",
        nbins=10,
        title="Age Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------------
    # PLAYING ROLE
    # -------------------------------

    st.subheader("Playing Role Breakdown")

    role_counts = (
        filtered_df["Playing Role"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    role_counts.columns = [
        "Role",
        "Count"
    ]

    fig = px.pie(
        role_counts,
        names="Role",
        values="Count",
        title="Role Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    selected_role = st.selectbox(
        "View Players By Role",
        sorted(
            filtered_df["Playing Role"]
            .dropna()
            .unique()
        ),
        key="role_view"
    )

    role_players = filtered_df[
        filtered_df["Playing Role"]
        == selected_role
    ]

    st.dataframe(
        role_players[
            [
                "Name of the Player",
                "Age",
                "Playing Role",
                "Self Rating"
            ]
        ],
        use_container_width=True
    )

    # -------------------------------
    # BATTING POSITION
    # -------------------------------

    st.subheader(
        "Preferred Batting Position"
    )

    batting_counts = (
        filtered_df[
            "Preferred Batting Position"
        ]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    batting_counts.columns = [
        "Position",
        "Count"
    ]

    fig = px.bar(
        batting_counts,
        x="Position",
        y="Count",
        title="Batting Positions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    selected_position = st.selectbox(
        "View Players By Batting Position",
        sorted(
            filtered_df[
                "Preferred Batting Position"
            ]
            .dropna()
            .unique()
        ),
        key="batting_position"
    )

    batting_players = filtered_df[
        filtered_df[
            "Preferred Batting Position"
        ]
        == selected_position
    ]

    st.dataframe(
        batting_players[
            [
                "Name of the Player",
                "Age",
                "Playing Role"
            ]
        ],
        use_container_width=True
    )

    # -------------------------------
    # BOWLING TYPE
    # -------------------------------

    st.subheader("Bowling Types")

    bowling_counts = (
        filtered_df[
            "Preferred Bowling Type"
        ]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    bowling_counts.columns = [
        "Bowling Type",
        "Count"
    ]

    fig = px.pie(
        bowling_counts,
        names="Bowling Type",
        values="Count",
        hole=0.5,
        title="Bowling Type Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    selected_bowling = st.selectbox(
        "View Players By Bowling Type",
        sorted(
            filtered_df[
                "Preferred Bowling Type"
            ]
            .dropna()
            .unique()
        ),
        key="bowling_type"
    )

    bowling_players = filtered_df[
        filtered_df[
            "Preferred Bowling Type"
        ]
        == selected_bowling
    ]

    st.dataframe(
        bowling_players[
            [
                "Name of the Player",
                "Age",
                "Playing Role"
            ]
        ],
        use_container_width=True
    )

    # -------------------------------
    # SELF RATING
    # -------------------------------

    st.subheader(
        "Self Rating Distribution"
    )

    fig = px.histogram(
        filtered_df,
        x="Self Rating",
        title="Self Ratings"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ====================================
# PLAYER EXPLORER
# ====================================

with tab2:

    selected_player = st.selectbox(
        "Select Player",
        sorted(
            df["Name of the Player"]
            .dropna()
        ),
        key="player_profile"
    )

    player = df[
        df["Name of the Player"]
        == selected_player
    ].iloc[0]

    st.subheader(
        player["Name of the Player"]
    )

    c1, c2 = st.columns(2)

    with c1:

        st.write(
            "**Age:**",
            player["Age"]
        )

        st.write(
            "**Role:**",
            player["Playing Role"]
        )

        st.write(
            "**Batting Position:**",
            player[
                "Preferred Batting Position"
            ]
        )

        st.write(
            "**Bowling Type:**",
            player[
                "Preferred Bowling Type"
            ]
        )

    with c2:

        st.write(
            "**Skills:**",
            player["Strong Skills"]
        )

        st.write(
            "**Experience:**",
            player[
                "Previous Tournament Experience"
            ]
        )

        st.write(
            "**Fitness:**",
            player[
                "How would you rate your fitness level?"
            ]
        )

        st.write(
            "**Self Rating:**",
            player["Self Rating"]
        )

    st.divider()

    st.subheader("Complete Player Record")

    st.dataframe(
        player.to_frame(),
        use_container_width=True
    )

# ------------------------------------
# RAW DATA
# ------------------------------------

st.divider()

st.subheader("Player Database")

st.dataframe(
    filtered_df,
    use_container_width=True
)