import streamlit as st
import requests
import json
import plotly.graph_objects as go

st.set_page_config(
    page_title="ImpactLens AI",
    page_icon="🔎"
)

st.title("🔎 ImpactLens AI")
st.subheader("AI-Powered Decision Impact & Risk Analyser")

st.write(
    "Compare two decisions and understand their risks, benefits "
    "and longer-term consequences."
)

option_a = st.text_area(
    "Option A",
    placeholder="Enter the first decision..."
)

option_b = st.text_area(
    "Option B",
    placeholder="Enter the second decision..."
)


def mean_score(scores):
    return sum(scores.values()) / len(scores)


def show_items(items):
    for item in items:
        st.write("•", item)


def format_text(value):
    if isinstance(value, dict):
        text = []

        for category, explanation in value.items():
            text.append(
                f"**{category.title()}:** {explanation}"
            )

        return "\n\n".join(text)

    return str(value)


def show_tradeoffs(scores_a, scores_b):
    categories = [
        "financial",
        "operational",
        "customer",
        "reputation",
        "privacy",
        "ethical"
    ]

    tradeoffs = []

    for category in categories:

        difference = abs(
            scores_a[category] - scores_b[category]
        )

        if difference >= 3:

            if scores_a[category] > scores_b[category]:

                tradeoffs.append(
                    f"**{category.title()}:** "
                    f"Option A has a significantly higher risk "
                    f"({scores_a[category]}/10) than Option B "
                    f"({scores_b[category]}/10)."
                )

            else:

                tradeoffs.append(
                    f"**{category.title()}:** "
                    f"Option B has a significantly higher risk "
                    f"({scores_b[category]}/10) than Option A "
                    f"({scores_a[category]}/10)."
                )

    if tradeoffs:

        for tradeoff in tradeoffs:
            st.warning(tradeoff)

    else:

        st.success(
            "No major risk trade-offs were identified between "
            "the two options."
        )


if st.button("🔍 Compare Decisions") and option_a and option_b:

    prompt = f"""
You are ImpactLens AI, a decision-support system.

Compare these two decisions fairly:

OPTION A:
{option_a}

OPTION B:
{option_b}

Return ONLY valid JSON.
Do not include markdown outside the JSON.

Use EXACTLY this structure:

{{
  "a": {{
    "scores": {{
      "financial": 1,
      "operational": 1,
      "customer": 1,
      "reputation": 1,
      "privacy": 1,
      "ethical": 1
    }},
    "advantages": [
      "Advantage",
      "Advantage"
    ],
    "disadvantages": [
      "Disadvantage",
      "Disadvantage"
    ],
    "hidden": [
      "Hidden consequence",
      "Hidden consequence"
    ]
  }},

  "b": {{
    "scores": {{
      "financial": 1,
      "operational": 1,
      "customer": 1,
      "reputation": 1,
      "privacy": 1,
      "ethical": 1
    }},
    "advantages": [
      "Advantage",
      "Advantage"
    ],
    "disadvantages": [
      "Disadvantage",
      "Disadvantage"
    ],
    "hidden": [
      "Hidden consequence",
      "Hidden consequence"
    ]
  }},

  "comparison": "Write one clear paragraph comparing the two options.",

  "recommendation": "Write one clear paragraph recommending the stronger option."
}}

IMPORTANT:

All six scores must be integers from 1 to 10.

1 = very low impact or risk.
10 = very high impact or risk.

Give 2 useful advantages, 2 useful disadvantages,
and 2 useful hidden consequences for each option.

Hidden consequences must be different from disadvantages.

Focus hidden consequences on:
- second-order effects
- unintended consequences
- long-term effects
- effects that may not be immediately obvious

The comparison MUST be a single text paragraph.

The recommendation MUST be a single text paragraph.

Do not return the comparison or recommendation as an object,
list or dictionary.

Compare both options fairly.

Be specific to the decisions provided.

Every field must contain an answer.
"""

    with st.spinner(
        "🔎 Analysing and comparing both decisions..."
    ):

        try:

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3.2:latest",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "format": "json"
                },
                timeout=120
            )

            response.raise_for_status()

            raw_response = response.json()["message"]["content"]

            result = json.loads(raw_response)

            scores_a = result["a"]["scores"]
            scores_b = result["b"]["scores"]

            risk_a = mean_score(scores_a)
            risk_b = mean_score(scores_b)

            st.divider()

            # -------------------------
            # Overall Risk
            # -------------------------

            st.subheader("🎯 Overall Risk Comparison")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Option A",
                    f"{risk_a:.1f}/10"
                )

            with col2:

                st.metric(
                    "Option B",
                    f"{risk_b:.1f}/10"
                )

            if risk_a < risk_b:

                st.success(
                    f"🟢 Option A has the lower overall risk "
                    f"({risk_a:.1f}/10 compared with "
                    f"{risk_b:.1f}/10)."
                )

            elif risk_b < risk_a:

                st.success(
                    f"🟢 Option B has the lower overall risk "
                    f"({risk_b:.1f}/10 compared with "
                    f"{risk_a:.1f}/10)."
                )

            else:

                st.warning(
                    "🟠 Both options have the same overall risk score."
                )

            # -------------------------
            # Key Trade-offs
            # -------------------------

            st.subheader("⚠️ Key Trade-offs")

            st.write(
                "These are impact areas where the two options "
                "differ substantially."
            )

            show_tradeoffs(
                scores_a,
                scores_b
            )

            # -------------------------
            # Impact Chart
            # -------------------------

            st.subheader("📊 Impact Comparison")

            categories = [
                "Financial",
                "Operational",
                "Customer",
                "Reputation",
                "Privacy",
                "Ethical"
            ]

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    name="Option A",
                    x=categories,
                    y=[
                        scores_a["financial"],
                        scores_a["operational"],
                        scores_a["customer"],
                        scores_a["reputation"],
                        scores_a["privacy"],
                        scores_a["ethical"]
                    ]
                )
            )

            fig.add_trace(
                go.Bar(
                    name="Option B",
                    x=categories,
                    y=[
                        scores_b["financial"],
                        scores_b["operational"],
                        scores_b["customer"],
                        scores_b["reputation"],
                        scores_b["privacy"],
                        scores_b["ethical"]
                    ]
                )
            )

            fig.update_layout(
                title="Risk / Impact by Category",
                xaxis_title="Impact Category",
                yaxis_title="Score",
                yaxis=dict(range=[0, 10]),
                barmode="group",
                height=430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # -------------------------
            # Detailed Scores
            # -------------------------

            st.subheader("📋 Detailed Scores")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### Option A")

                for category, score in scores_a.items():

                    st.write(
                        f"**{category.title()}:** {score}/10"
                    )

            with col2:

                st.markdown("### Option B")

                for category, score in scores_b.items():

                    st.write(
                        f"**{category.title()}:** {score}/10"
                    )

            # -------------------------
            # Advantages
            # -------------------------

            st.subheader("✅ Advantages")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### Option A")

                show_items(
                    result["a"]["advantages"]
                )

            with col2:

                st.markdown("### Option B")

                show_items(
                    result["b"]["advantages"]
                )

            # -------------------------
            # Disadvantages
            # -------------------------

            st.subheader("⚠️ Disadvantages")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### Option A")

                show_items(
                    result["a"]["disadvantages"]
                )

            with col2:

                st.markdown("### Option B")

                show_items(
                    result["b"]["disadvantages"]
                )

            # -------------------------
            # Hidden Consequences
            # -------------------------

            st.subheader("🔎 Hidden Consequences")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### Option A")

                show_items(
                    result["a"]["hidden"]
                )

            with col2:

                st.markdown("### Option B")

                show_items(
                    result["b"]["hidden"]
                )

            # -------------------------
            # AI Comparison
            # -------------------------

            st.subheader("⚖️ AI Comparison")

            comparison = result.get(
                "comparison",
                "No comparison was returned."
            )

            st.info(
                format_text(comparison)
            )

            # -------------------------
            # Recommendation
            # -------------------------

            st.subheader("💡 Recommendation")

            recommendation = result.get(
                "recommendation",
                "No recommendation was returned."
            )

            st.success(
                format_text(recommendation)
            )

        except json.JSONDecodeError:

            st.error(
                "The AI returned an unexpected format. "
                "Please run the comparison again."
            )

        except KeyError as e:

            st.error(
                f"The AI response was missing information: {e}"
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to Ollama. "
                "Make sure Ollama is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The AI took too long to respond. "
                "Please try again."
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )