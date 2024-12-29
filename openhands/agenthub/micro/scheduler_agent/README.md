# Scheduler Agent

The Scheduler Agent is a specialized micro-agent in OpenHands that manages task scheduling using APScheduler. It provides a flexible and powerful interface for scheduling tasks with various timing patterns.

## Capabilities

1. **Schedule Types**
   - Cron-based scheduling
   - Interval-based scheduling
   - Date-based scheduling
   - Combined triggers
   - Persistent scheduling

2. **Job Management**
   - Create new scheduled tasks
   - Modify existing schedules
   - Remove scheduled tasks
   - Pause/Resume tasks
   - List active schedules

3. **Advanced Features**
   - Job persistence
   - Multiple executors
   - Job coalescing
   - Misfire handling
   - Timezone support

## Trigger Words

The agent activates when it detects these keywords:
- `schedule`
- `scheduler`
- `cron`
- `interval`
- `apscheduler`

## Usage Examples

1. Cron Schedule:
```python
# Daily task at 9 AM
{
    "task": "Run daily report",
    "schedule_type": "cron",
    "schedule_params": {
        "hour": "9",
        "minute": "0"
    },
    "job_id": "daily_report",
    "action": "add"
}
```

2. Interval Schedule:
```python
# Every 6 hours
{
    "task": "Database backup",
    "schedule_type": "interval",
    "schedule_params": {
        "hours": 6
    },
    "job_id": "db_backup",
    "action": "add"
}
```

3. Date Schedule:
```python
# One-time future event
{
    "task": "System upgrade",
    "schedule_type": "date",
    "schedule_params": {
        "run_date": "2025-01-01 00:00:00"
    },
    "job_id": "upgrade_task",
    "action": "add"
}
```

## Job Operations

1. **Add Job**
```python
action: "add"
```

2. **Modify Job**
```python
action: "modify"
```

3. **Remove Job**
```python
action: "remove"
```

4. **Pause Job**
```python
action: "pause"
```

5. **Resume Job**
```python
action: "resume"
```

## Best Practices

1. **Job IDs**
   - Use unique, descriptive IDs
   - Include version or date if needed
   - Follow consistent naming pattern

2. **Schedule Parameters**
   - Validate all inputs
   - Use appropriate timezone
   - Set reasonable intervals
   - Consider resource impact

3. **Error Handling**
   - Set appropriate grace times
   - Configure misfire policies
   - Implement job coalescing
   - Monitor job execution

4. **Persistence**
   - Use appropriate job store
   - Configure backup strategy
   - Handle migration scenarios
   - Maintain job history

## Input/Output

### Inputs
- `task`: Description of the task to schedule
- `schedule_type`: Type of schedule (cron/interval/date)
- `schedule_params`: Schedule configuration parameters
- `job_id`: Unique identifier for the job
- `action`: Operation to perform (add/modify/remove/pause/resume)

### Outputs
- `result`: Operation result message
- `job_info`: Detailed job information including next run time

## Dependencies

The agent requires:
- APScheduler >= 3.10.4
- pytz >= 2023.3
- SQLAlchemy (for persistent storage)

## Configuration

The agent supports various configuration options:
```python
{
    "job_defaults": {
        "coalesce": True,
        "max_instances": 1,
        "misfire_grace_time": 3600
    },
    "jobstores": {
        "default": "SQLAlchemyJobStore"
    },
    "executors": {
        "default": "ThreadPoolExecutor",
        "processpool": "ProcessPoolExecutor"
    }
}
```