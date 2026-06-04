# HR Analytics Homelab Platform

## Overview

This is a homelab project to produce:

- A comprehensive HR analytics platform designed to provide HR teams with actionable insights into
  - employee retention,
  - performance management,
  - training compliance,
  - and workforce planning.

This project demonstrates a modern data stack combining Python data engineering, PostgreSQL, workflow automation, and business intelligence dashboards.

## Problem Statement (hypothetical)

HR departments face significant challenges in managing and analyzing workforce data:

- **Limited Visibility**: Lack of real-time insights into employee lifecycle events, turnover patterns, and performance trends
- **Manual Processes**: Time-consuming manual report generation and data consolidation across multiple systems
- **Data Silos**: Employee data scattered across different systems making cross-functional analysis difficult
- **Compliance Gaps**: Difficulty tracking training completion and compliance requirements
- **Retention Issues**: Inability to identify flight risks or understand turnover drivers
- **Performance Blind Spots**: Lack of comprehensive performance tracking and review history

## Solution

A fully integrated HR Analytics platform built on a modern, scalable tech stack.

### Technology Stack

- **PostgreSQL** - Centralized data warehouse for employee, performance, and training data
- **Python** - ETL scripts for data generation, transformation, and loading
- **Metabase** - Business intelligence and dashboard visualization tool
- **n8n** - Workflow automation and data pipeline orchestration
- **Docker** - Containerization for easy deployment and environment consistency

### Core Features

#### 1. Employee Lifecycle Tracking

- Complete employee records including demographics, hire dates, departments, and contact information
- Historical tracking of employee movements and department changes
- Integration with manager relationships and reporting structures

#### 2. Turnover Analysis

- Comprehensive turnover tracking with termination dates and separation reasons
- Cohort analysis to identify turnover patterns by department, tenure, and other factors
- Predictive insights to identify flight risks and retention opportunities

#### 3. Performance Management

- Multi-year performance review history with ratings and comments
- Comprehensive performance metrics tracking employee development and growth
- Trend analysis to identify high performers and performance improvement areas

#### 4. Training & Compliance

- Training record tracking with completion dates and assessment scores
- Compliance monitoring for mandatory training courses by department
- Course effectiveness analysis and certification tracking

#### 5. KPI Dashboards

- Real-time executive dashboards with key HR metrics
- Department-level performance indicators
- Turnover rates, average tenure, training completion rates
- Interactive visualizations and drill-down capabilities

#### 6. Automated Reporting

- Scheduled report generation and distribution
- Workflow automation using n8n for ETL and alerting
- Custom report creation based on business requirements

## Project Structure

```
HR-Analytics-Homelab/
├── docker-compose.yml          # Docker Compose configuration for services
├── Dockerfile                  # Container image definition
├── Python/
│   ├── generate_data.py        # Dummy data generation script
│   └── python.txt              # Python dependencies and docs
├── SQL/
│   └── sql.txt                 # Database schema and setup scripts
├── Data/
│   ├── Raw/                    # Raw input data files (five .CSV files)
│   └── Processed/              # Processed and cleaned data
├── Dashboards/
│   └── dashboards.txt          # Metabase dashboard configurations
├── n8n/
│   └── n8n.txt                 # n8n workflow definitions
├── Docs/
│   ├── architecture.txt        # System architecture documentation
│   ├── data_dictionary.txt     # Data schema and field definitions
│   ├── Evolution.txt           # Project evolution and iterations
│   ├── project_journal.txt     # Development journal and notes
└── Readme.md                   # This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- PostgreSQL client tools (optional, for direct database access)

### Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/younusk1/HR-Analytics-Homelab
   cd HR-Analytics-Homelab
   ```

2. **Generate test data**

   ```bash
   python Python/generate_data.py
   ```

   This creates CSV files with dummy employee, manager, performance, training, and turnover data.

3. **Start services with Docker Compose**

   ```bash
   docker-compose up -d
   ```

   This launches:
   - PostgreSQL database (port 5432)
   - Metabase BI tool (port 3000)
   - n8n workflow automation (port 5678)

4. **Load data into PostgreSQL**

   ```bash
   psql -h localhost -U postgres < SQL/schema.sql
   # Then import CSV files into respective tables
   ```

5. **Access dashboards**
   - Metabase: http://localhost:3000
   - n8n: http://localhost:5678
   - PostgreSQL: http://localhost:5432

## Usage

### Running Dashboards

1. Open Metabase at http://localhost:3000
2. Connect to PostgreSQL database
3. View pre-built dashboards showing:
   - Employee count and department distribution
   - Turnover trends and reasons
   - Performance rating distributions
   - Training completion rates

### Automating Workflows

1. Open n8n at http://localhost:5678
2. Configure workflows for:
   - Scheduled data refresh from source systems
   - Automated email alerts for compliance issues
   - Report generation and distribution

### Direct Database Access

```bash
psql -h localhost -U postgres -d hr_analytics
SELECT * FROM employees;
SELECT * FROM performance_reviews WHERE rating < 3;
SELECT COUNT(*) FROM training_records WHERE score IS NULL;
```

## Key Metrics & KPIs

- **Employee Count by Department**
- **Turnover Rate (Annual)**
- **Average Tenure**
- **Performance Rating Distribution**
- **Training Completion Rate**
- **Attrition by Reason**
- **Manager-to-Employee Ratio**

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL container is running: `docker-compose ps`
- Check credentials in connection strings
- Verify network connectivity between containers

### Data Import Failures

- Verify CSV file format matches schema expectations
- Check for encoding issues (use UTF-8)
- Review foreign key constraints

### Dashboard Not Loading

- Ensure Metabase service is fully started (may take 30 seconds)
- Clear browser cache and refresh
- Check Metabase logs: `docker-compose logs metabase`

## Documentation

See the `Docs/` folder for detailed documentation:

- **architecture.txt** - System design and component interactions
- **data_dictionary.docx** - Complete field descriptions and data types
- **dockerfile.txt** - Docker configuration details
- **project_journal.txt** - Development notes and evolution

## Potential Future Enhancements

- Integration with active directory for real-time employee sync
- Predictive analytics for turnover and performance
- Mobile app for manager access to dashboards
- Advanced permission and role-based access control
- Historical data retention and archival policies

## Support & Contributions

For questions, issues, or contributions, please refer to the project documentation in the `Docs/` folder.
