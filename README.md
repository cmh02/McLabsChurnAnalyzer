# MCLabs Churn Analyzer

Welcome to the [MCLabs](https://labs-mc.com/) (often shortened to MCL) Churn Analyzer!

This tool will implement a machine learning model to predict the churn of players based on player metrics. Initially, we will use a simple logistic regression model, but may move to a more advanced model at a later point in time.

## Project Introduction

The goal of this project is to be able to accurately predict player churn (whether a player has stopped playing on the server or not). The premise is that, based on player metrics captured on the server, a specific player can be identified as churned (no longer playing) or active (still playing).

Being able to predict the churn status for a player based on player metrics can be used in a variety of ways:

* General prediction of churn rate at any time, indicative of player base changes
* Specialized marketing / bonuses etc to keep the player engaged with the server if churn likely
* Observe effects of specific events or updates on the server
* Identify when specific events or updates on the server are ideal
* Find certain flaws in player progression

One of the main goals with this project is to simply test the hypothesis that some subset of features selected from a player's metrics will reveal the probability of churn. An exact combination or pattern is not known in advance, so several phases of testing will need to be completed. This goal is the main driving factor behind the use of machine learning to solve these problems.
