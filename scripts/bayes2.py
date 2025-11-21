import arviz as az
import matplotlib.pyplot as plt
import pymc as pm
import numpy as np

np.random.seed(42)
x = np.linspace(0, 10, 50)
true_intercept = 1
true_slope = 2
y = true_intercept + true_slope * x + np.random.normal(0, 1, size=len(x))


with pm.Model() as model:
    # Sample posterior lines
    intercept = pm.Normal("Intercept", mu=0, sigma=10)
    slope = pm.Normal("Slope", mu=0, sigma=10)
    sigma = pm.HalfNormal("Sigma", sigma=1)

    mu = intercept + slope * x
    y_obs = pm.Normal("Y_obs", mu=mu, sigma=sigma, observed=y)

    trace = pm.sample(1000, return_inferencedata=True, progressbar=False)
    posterior_samples = az.extract(trace, var_names=["Intercept", "Slope"]).to_dataframe()
    plt.figure(figsize=[6,3.3])
    plt.scatter(x, y, label="Observed data")

    for i in range(100):
        sample = posterior_samples.sample(1)
        plt.plot(
            x, sample["Intercept"].values + sample["Slope"].values * x,
            color="red", alpha=0.1
        )

    plt.plot(x, true_intercept + true_slope*x, "k--", label="True line")
    plt.legend()
    plt.title("Posterior Regression Lines")
    plt.show()
