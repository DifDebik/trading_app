from fastapi import APIRouter, BackgroundTasks, Depends

from auth.base_config import current_user

from tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report(user=Depends(current_user)):
    # background_tasks.add_task(send_email_report_dashboard, user.username)  #BGTASKS FROM FASTAPI
    # send_email_report_dashboard(user.username)  #NO BGTASKS
    send_email_report_dashboard.delay(user.username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }