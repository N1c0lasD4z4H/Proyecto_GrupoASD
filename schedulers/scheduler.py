from apscheduler.schedulers.background import BackgroundScheduler
from schedulers.collect_prs import job_index_prs

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_index_prs, 'interval', hours=1)  # ejecuta cada hora
    scheduler.start()
    print("[🟢] Scheduler iniciado - Tarea programada activada")
