import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt

def main():
    # Simulate data
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    true_intercept = 1
    true_slope = 2
    y = true_intercept + true_slope * x + np.random.normal(0, 1, size=len(x))

    # Bayesian linear regression model
    with pm.Model() as model:
        intercept = pm.Normal("Intercept", mu=0, sigma=10)
        slope = pm.Normal("Slope", mu=0, sigma=10)
        sigma = pm.HalfNormal("Sigma", sigma=1)

        mu = intercept + slope * x
        y_obs = pm.Normal("Y_obs", mu=mu, sigma=sigma, observed=y)

        trace = pm.sample(1000, return_inferencedata=True, progressbar=False)

    # Extract posterior samples
    posterior = az.extract(trace, var_names=["Intercept", "Slope"]).to_dataframe()

    # Matplotlib density plots
    fig, ax = plt.subplots(1, 2, figsize=[6,3.3])

    ax[0].hist(posterior["Intercept"], bins=40, color="skyblue", edgecolor="black", alpha=0.7)
    ax[0].set_title("Posterior of Intercept")
    ax[0].set_xlabel("Value")
    ax[0].set_ylabel("Density")

    ax[1].hist(posterior["Slope"], bins=40, color="salmon", edgecolor="black", alpha=0.7)
    ax[1].set_title("Posterior of Slope")
    ax[1].set_xlabel("Value")

    fig.suptitle("Posterior Distributions")
    fig.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()
