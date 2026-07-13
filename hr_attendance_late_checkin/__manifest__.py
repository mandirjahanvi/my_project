{
    'name': 'HR Attendance Late Check-in',
    'summary':'HR Attendance Late',
    'depends': ['hr','hr_attendance'],
    'data': [
        "security/ir.model.access.csv",
        "views/hr_attendance_views.xml",
        "views/hr_attendance_late_report_views.xml",
        "views/menu.xml",
    ],
    'installable': True,
}