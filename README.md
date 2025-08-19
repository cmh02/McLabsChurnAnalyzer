# MCLabs Churn Analyzer

##### 🚧 Work in Progress: This project is currently under active development!

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

## Feature Selection

There are a variety of features, either directly or indirectly derived from player metrics, that may have some effect on the probability of player churn. However, the largest constraint for this project is the availability of these features. In order to properly have data for the model, we must only consider data sources which are pre-existing to the model. For this, we must turn to metrics that are already being tracked in some manner. There are three main types of data sources that can present these metrics for the model:

1. Pre-existing databases that store a variety of player data
2. Java-based [Paper](https://papermc.io/software/paper) or [Velocity](https://papermc.io/software/velocity) Plugins currently on the server that track player data internally and offer access through developer API's
3. Custom systems that have been built in [Skript](https://github.com/SkriptLang/Skript), a popular scripting language for minecraft servers, and are actively developed by server developers

Unfortunately, even among these types of data sources, the access for each individual data metric may differ from source to source. However, the approach among all three will generally be the same: connect with the given data source, extract the desired features, and save features to an external storage of some type. For more information on how this is done, see [Data Collection and Preparation](#Data Collection and Preparation).

Based on all of the available data sources, the following raw features for each player are being selected for use in the model's predictions:

|    Name    | Description                                                     |
| :---------: | --------------------------------------------------------------- |
|   balance   | The player's economy balance                                    |
| onlinetime | The amount of time the player has spent on the server, in total |
|    joins    | The number of times the player has joined the server            |
| leaderboard | The general leaderboard score of the player                     |
|  chemrank  | The player's chem rank                                          |
|  donorrank  | The player's donor rank                                         |
|    votes    | The number of times the player has voted                        |

These features will later be analyzed to identify which features are more important to predicting churn and which features are less important. It may be revealed that certain features have no effect at all, whereas other features have a much larger effect than expected. This is a secondary goal of this project.

Beyond the collection of these raw features, other features will be derived for further model analysis. Because most of these derived metrics cannot be directly gathered from the server, there will be a big reliance in the data preparation and pre-processing phases of the model to create them. For instance, since the specific onlinetime of a player during a duration is not tracked, we must track it by regularly calculating the difference between two observations of the player's onlinetime. Ideally, this will be automatically calculated with respect to time for each model run, allowing for non-regular intervals to be used while necessary.

## Data Collection and Preparation

As previously mentioned, one of the largest challenges for this project is properly collecting player metrics from several sources on the server. To simplify collection as much as possible, Skript will be utilized to collect as much data as possible. This method is being chosen for a few reasons:

1. Skript provides fast development
2. Skript will allow for data to be collected from all three types of data sources: databases, Java plugins, and other Skript systems
3. Skript makes it relatively easy to export data via a variety of methods

To gather data for the model using Skript, several data-gathering skripts have been created. Some of these skripts are provided in [gathering-skripts](), although many will not be published due to the amount of customization, architecture, and credentials that would be released.

Once the data has been gathered from the various sources into Skript (via some method), it can then be saved to some data storage so that it can be moved off of the server and prepared for the model.
