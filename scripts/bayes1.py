import numpy as np
import pymc as pm
import arviz as az
import plotly.express as px

#Simulate data

np.random.seed(42)
x = np.linspace(0, 10, 50)
true_intercept = 1
true_slope = 2
y = true_intercept + true_slope * x + np.random.normal(0, 1, size=len(x))

#Bayesian linear regression model

with pm.Model() as model:
    intercept = pm.Normal("Intercept", mu=0, sigma=10)
    slope = pm.Normal("Slope", mu=0, sigma=10)
    sigma = pm.HalfNormal("Sigma", sigma=1)

    mu = intercept + slope * x
    y_obs = pm.Normal("Y_obs", mu=mu, sigma=sigma, observed=y)

    trace = pm.sample(1000, return_inferencedata=True, progressbar=False)
    #Convert to dataframe for Plotly

    posterior_df = az.extract(trace, var_names=["Intercept", "Slope"]).to_dataframe()

    #Interactive density plot

    fig = px.histogram(
    posterior_df.melt(var_name="Parameter", value_name="Value"),
    x="Value", color="Parameter", marginal="box", opacity=0.6,
    nbins=40, barmode="overlay", title="Posterior Distributions")
    fig.update_layout(template="plotly_white",width=550,height=300)
    fig.show()