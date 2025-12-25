# Installation

## Frappe Cloud
1. Push this repository to GitHub/GitLab.
2. In Frappe Cloud, add it as a Private App.
3. Install the app on your site.

## Bench (self-hosted)
```bash
bench get-app https://github.com/<org>/hr_accrual_engine
bench --site <site-name> install-app hr_accrual_engine
bench restart
```
