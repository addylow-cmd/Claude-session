# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Contents

This repository contains a small HR dataset and a derived visualization:

- `toy_hr_data.csv` — 55 synthetic employee records with fields: `employee_id`, `department`, `tenure_years`, `salary`, `satisfaction_score`, `performance_rating`. Departments: Engineering, Sales, Marketing, HR, Finance.
- `salary_distribution.png` — A chart generated from the CSV data showing salary distributions.

## Data Schema

| Field | Type | Notes |
|---|---|---|
| `employee_id` | int | 1001–1055 |
| `department` | string | Engineering, Sales, Marketing, HR, Finance |
| `tenure_years` | float | Years at company |
| `salary` | int | Annual salary in USD |
| `satisfaction_score` | float | 1–10 scale |
| `performance_rating` | int | 1–5 scale |
