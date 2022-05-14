import streamlit as st
from utils.utils import get_all_tvl, hide_streamlit_style
import plotly.express as px

st.set_page_config(page_title="Polygon x Sushi", page_icon="🍣", layout="wide")
st.markdown("# [Polygon x Sushi]()", unsafe_allow_html=True)


st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(
    """On May 7th, 2021 there was a joint liquidity incentive program that was launched by Polygon on Sushi  [\[1\]](https://twitter.com/sushiswap/status/1390451638977007620?lang=en).
    This as well as other liquidity incentive programs [\[2\]](https://cryptobriefing.com/polygon-launches-40m-liquidity-mining-program-with-aave/) that  launched on Polygon brought a lot of TVL on the chain.
    In order to differenetiate from what TVL comes from what program, we will show the TVL of the entire chain vs the specific TVL of sushi (on Polygon) at the time. The data source for both is [DeFiLlama](https://defillama.com/)
    """
)
st.markdown(
    """
    **NOTE**: There are some datapoints missing for the Sushi TVL around Feb-April 2022, this will cause the weekly view to look slightly odd.
    """
)

st.markdown(
    """
   ## Polygon TVL x Sushi TVL on Polygon
   """
)
st.markdown(
    """
   Let's first look at the TVL on the Polygon chain for Sushi compared to the overall TVL on Polygon over time both in linear terms and then in log terms and more specifically around the launch of the incentives, in order to get a better understanding of the correlation of how the incentives helped Sushi on Polygon.
   """
)

option = "daily"
option = st.selectbox("View:", ("daily", "weekly", "monthly"), index=0)


@st.cache(suppress_st_warning=True)
def load_data():
    data = get_all_tvl(trunc_date=option)
    data.rename({"TVL": "Total Value Locked ($)"}, axis=1, inplace=True)
    return data


(tvl_data) = load_data()
st.markdown(f"### TVL comparisson/correlation by {option}")

fig_cols = st.columns(2)
with fig_cols[0]:
    # st.markdown("### Second Chart Title")
    fig = px.line(
        tvl_data,
        x="Date",
        y="Total Value Locked ($)",
        title=f"Polygon vs Sushi TVL | {option.capitalize()}",
        color="Context",
    )
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

with fig_cols[1]:
    # st.markdown("### Third Chart Title")
    fig2 = px.line(
        tvl_data[tvl_data.Date > "2021-05-15"],
        x="Date",
        y="Total Value Locked ($)",
        title=f"Polygon vs Sushi TVL | {option.capitalize()} | Log | From 2021-05-15",
        color="Context",
        log_y=True,
    )
    fig2.update_layout(autosize=True, width=800, height=600)
    st.write(fig2)

st.markdown(
    """
  What we can see here is that there's a massive spike for both Polygons and Sushis TVL on the 15th of June, 2021. This coincides very clearly with potentially the actual launch of the incentive rewards and not the announcement that they'll be coming to Sushi, which was on May 7th 2021.
  When looking at the `log` version of the chart, we can see that that the spikes coincide very clearly as well as the subsequent profile of the TVL graphs (approximately), but decouple more and more around the August of 15h 2021. 
  """
)

st.markdown(
    """
   ### Top performing Contracts around that period
  """
)
st.markdown(
    "Let's now look at the top 50 performing contracts that launched (on Polygon) before the launch of the liquidity incentive program, in terms of their Transaction Volume in Counts from when they were first invoked until + 2 months."
)
fig_cols2 = st.columns(2)
with fig_cols2[0]:
    st.markdown(
        """
    <iframe 
    loading="lazy" src="https://velocity-app.flipsidecrypto.com/velocity/visuals/e44e1268-1dce-4013-b784-58c701bb9677/5e3018d2-fb79-483a-b7e3-8cc815abca78" width="100%" height="600"></iframe>
    """,
        unsafe_allow_html=True,
    )

with fig_cols2[1]:
    st.markdown(
        """
    <iframe loading="lazy" src="https://velocity-app.flipsidecrypto.com/velocity/visuals/8b50724d-4f8f-4256-9d15-20e70a228c17/fcdccdcd-05f1-4a37-85e1-9d170ac2fcf2" width="100%" height="600"></iframe>
    """,
        unsafe_allow_html=True,
    )
st.markdown(
    """
    Sadly the top performing contracts are coming from [Iron Finance](https://iron.finance/) that turns out [rug pulled](https://ciphertrace.com/analysis-of-the-titan-token-collapse-iron-finance-rugpull-or-defi-bank-run/) and
    `YELD` which I cannot find that much info about, [Coin to Fish or `FISH`](https://coinmarketcap.com/currencies/coin-to-fish/) which also appears to not have worked out as expected and
    [`OMEN`](https://coinmarketcap.com/currencies/omencoin/) whish also does not seem to have worked as expected, all of the other pools that are listed in the data are blue chips or protocols that to my knowledge still exist.
    """
)
st.markdown(
    """
    When looking at the filtered version of the top performing pools in that time, we can see some familiar faces such as `SUSHI/WETH`, `USDC/Other`, `WBTC/WETH`, `WETH/USDT` and `WETH/AAVE` in the top 5. 
    Which had a significant amount of transaction (in count) volume around the launch of the liquidity incentive program.
    """
)
st.markdown(
    """
    ### Summary
    """
)
st.markdown(
    """
    In summary what we can gauge from the following is that the [success](https://twitter.com/sushiswap/status/1400247900538429444) of the launch of Sushi on Polygon is directly related to the success of the liquidity incentive program launched by Polygon.
    This is not to take any credit from the amazing Sushi team, but just to note that there is a high degree of correlation with the launch of the incentives and the total TVL that came into Sushi on Polygon. This happens in all chains as yield farmers
    are looking for different opportunities to earn yield and the incentives on the given dex and chain and then move onto the next one. In this case it seems that even if the TVL of Sushi is currently not looking to be on any increasing trend,
    the Polygon TVL in general is on sustained slowly decreasing trend thats oscillating around the same or similar levels. This is impressive given the current conditions of the market (as of 14th May 2022) but it also means that there may still be a lot that
    Polygon itself can do to improve the overall performance of Sushi and the rest of the ecosystem. An example could be to provide further incentive rewards to help onboard more yield farmers and as such to incentivise higher TVL on Sushi and maybe the currently 
    [top performing dexs](https://defillama.com/chain/Polygon) on the ecosystem. In the atmosphere of the cryptosphere it seems that people love to jump on the shinniest and fanciest new thing. With the launch of such L2s such as Optimism, Arbitrum and others
    extra liquidity incentive programs would remind users of how cheap, secure and fast the Polygon chain is as well as draw the "hype" away from the competition!
    """
)
