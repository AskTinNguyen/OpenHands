import os
import pytest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
# Track schedulers for cleanup
_schedulers = []

# Mock function for testing
def mock_task():
    return "Task executed"

@pytest.fixture
def scheduler():
    """Create a test scheduler instance"""
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor(1)
    }
    scheduler = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        timezone=ZoneInfo('UTC')
    )
    scheduler.start()
    _schedulers.append(scheduler)
    return scheduler

def test_cron_schedule(scheduler):
    """Test cron-based scheduling"""
    job = scheduler.add_job(
        mock_task,
        'cron',
        hour='9',
        minute='0',
        id='test_cron'
    )
    
    assert job.id == 'test_cron'
    # Find hour and minute fields
    hour_field = next(f for f in job.trigger.fields if f.name == 'hour')
    minute_field = next(f for f in job.trigger.fields if f.name == 'minute')
    
    # Convert expressions to their values
    hour_values = {expr.first for expr in hour_field.expressions}
    minute_values = {expr.first for expr in minute_field.expressions}
    
    assert hour_values == {9}
    assert minute_values == {0}

def test_interval_schedule(scheduler):
    """Test interval-based scheduling"""
    job = scheduler.add_job(
        mock_task,
        'interval',
        hours=6,
        id='test_interval'
    )
    
    assert job.id == 'test_interval'
    assert job.trigger.interval == timedelta(hours=6)

def test_date_schedule(scheduler):
    """Test date-based scheduling"""
    future_date = datetime.now(ZoneInfo('UTC')) + timedelta(days=1)
    job = scheduler.add_job(
        mock_task,
        'date',
        run_date=future_date,
        id='test_date'
    )
    
    assert job.id == 'test_date'
    assert abs(job.trigger.run_date - future_date) < timedelta(seconds=1)

def test_job_modification(scheduler):
    """Test job modification capabilities"""
    job = scheduler.add_job(
        mock_task,
        'interval',
        hours=1,
        id='test_modify'
    )
    
    # Modify the job using reschedule
    scheduler.reschedule_job(
        'test_modify',
        trigger='interval',
        hours=2
    )
    
    modified_job = scheduler.get_job('test_modify')
    assert modified_job.trigger.interval == timedelta(hours=2)

def test_job_pause_resume(scheduler):
    """Test job pause and resume functionality"""
    job = scheduler.add_job(
        mock_task,
        'interval',
        hours=1,
        id='test_pause'
    )
    
    # Pause the job
    scheduler.pause_job('test_pause')
    assert scheduler.get_job('test_pause').next_run_time is None
    
    # Resume the job
    scheduler.resume_job('test_pause')
    assert scheduler.get_job('test_pause').next_run_time is not None

def test_job_removal(scheduler):
    """Test job removal"""
    scheduler.add_job(
        mock_task,
        'interval',
        hours=1,
        id='test_remove'
    )
    
    # Remove the job
    scheduler.remove_job('test_remove')
    assert scheduler.get_job('test_remove') is None

def test_multiple_jobs(scheduler):
    """Test handling multiple jobs"""
    jobs = [
        ('job1', 'interval', {'hours': 1}),
        ('job2', 'interval', {'hours': 2}),
        ('job3', 'interval', {'hours': 3})
    ]
    
    for job_id, trigger, params in jobs:
        scheduler.add_job(
            mock_task,
            trigger,
            id=job_id,
            **params
        )
    
    all_jobs = scheduler.get_jobs()
    assert len(all_jobs) == 3
    
    job_intervals = {
        job.id: job.trigger.interval
        for job in all_jobs
    }
    
    assert job_intervals['job1'] == timedelta(hours=1)
    assert job_intervals['job2'] == timedelta(hours=2)
    assert job_intervals['job3'] == timedelta(hours=3)

def test_invalid_schedule(scheduler):
    """Test handling of invalid schedule parameters"""
    with pytest.raises(TypeError):
        scheduler.add_job(
            mock_task,
            'interval',
            hours='invalid',
            id='test_invalid'
        )

def test_timezone_handling(scheduler):
    """Test timezone handling in schedules"""
    est = ZoneInfo('America/New_York')
    
    # Schedule a job with explicit timezone
    job = scheduler.add_job(
        mock_task,
        'cron',
        hour='9',
        minute='0',
        timezone=est,
        id='test_tz'
    )
    
    # The job's timezone should match what we set
    assert job.trigger.timezone == est
    
    # The next run time should be in EST
    next_run = job.next_run_time
    assert next_run.tzinfo.key == 'America/New_York'