# MCLabs Churn Analyzer: Environmental Variables

**NOTE: This directory is no longer used. No hashing is being performed in this stage of the project. However, this directory and environmental files within it are being kept for future structure.**

Our project does include some environmental variables that need to be configured. Within our project structure, we have created a `.env` file that resides inside this directory. The template of this `.env` file can be seen in [.env.example](.env.example), where all keys are defined to some placeholder value.

### Hashing Pepper Key: `MCA_PEPPERKEY`

The pepper key is used when hashing player UUID's to anonymous identifiers. This prevents UUID's from being reverse-hashed via some dictionary. It is suggested that this key simply be a 32-128 character string which will then be added to each UUID.
