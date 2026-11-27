
# SnowHeightTracker - Data Logic

Python-based data processing, validation, snow condition
analysis, and route scoring for the SnowHeightTracker project.

## Project Overview

SnowHeightTracker is a project designed to help users
compare winter travel routes in Montréal based on
available snow and street-clearing information.

This repository focuses on the Python data logic
component of the project.

## My Responsibilities

- Design route and street segment data models.
- Process and validate route information.
- Interpret snow removal status data.
- Develop snow condition analysis.
- Implement route scoring and comparison.
- Write automated tests.

## Technologies

- Python
- Git and GitHub
- pytest
- FastAPI (planned integration)

## Project Structure

- app/models.py: Route and StreetSegment data models.
- app/sample_data.py: Fictional routes for development.
- tests/test_models.py: Automated unit tests.

## Data Flow

### Input
Route information and street segment data.

Currently, the project uses fictional data for testing.

### Process
Python organizes route data using the Route and
StreetSegment classes.

### Output
Structured route objects for future snow analysis
and route comparison algorithms.

## Planned Data Sources

- Google Maps Routes API
- Montréal Planif-Neige public API
- Environment and Climate Change Canada GeoMET

## Current Progress

- [x] Initial Python project setup
- [x] GitHub repository and development branch
- [x] Route and StreetSegment models
- [x] Four fictional routes
- [x] Three passing unit tests
- [ ] Data validation
- [ ] Snow condition analysis
- [ ] Route scoring and comparison
- [ ] Real API integration

## Important Note

Current route information is fictional and used only
for development and testing.

Snow removal statuses do not directly indicate
road safety or measured snow depth.
